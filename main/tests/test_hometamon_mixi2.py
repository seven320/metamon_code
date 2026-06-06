import pytest

from src import mixi2_client  # noqa: F401  (生成スタブの path を通す)
from src import hometamon_mixi2
from src.mixi2_adapter import TweetLike, UserLike

from social.mixi.application.model.v1 import post_pb2, user_pb2


def tweet(text="ばおわ", uid="u1", screen="handle", name="なまえ", desc="", **kw):
    return TweetLike(
        id=kw.get("id", "p1"),
        text=text,
        favorited=kw.get("favorited", False),
        user=UserLike(id=uid, screen_name=screen, name=name, description=desc),
        in_reply_to_post_id=kw.get("in_reply_to_post_id"),
        community_id=kw.get("community_id", "c1"),
    )


def make_post(post_id, creator_id, text, created_seconds, **kw):
    p = post_pb2.Post(post_id=post_id, creator_id=creator_id, text=text, **kw)
    p.created_at.seconds = created_seconds
    return p


@pytest.fixture
def bot(mocker, tmp_path, monkeypatch):
    monkeypatch.setenv("MIXI2_DRY_RUN", "1")
    monkeypatch.setenv("MAX_REPLIES_PER_RUN", "2")
    monkeypatch.setenv("POLL_MIN_SLEEP", "0")
    monkeypatch.setenv("POLL_MAX_SLEEP", "0")
    monkeypatch.setenv("COMMUNITY_ID", "c1")
    monkeypatch.setenv("BOT_USER_ID", "bot1")
    mocker.patch("src.hometamon_mixi2.time.sleep")
    client = mocker.Mock()
    b = hometamon_mixi2.HometamonMixi2(client=client)
    b.state_dir = str(tmp_path)
    b.manuscript = mocker.Mock()
    b.manuscript.reply = ["お疲れ様だもん"]
    return b


class Test_check_exclude:
    def test_normal_trigger_not_excluded(self, bot):
        assert bot.check_exclude(tweet(text="ばおわ")) is False

    def test_own_post(self, bot):
        assert bot.check_exclude(tweet(uid="bot1")) is True

    def test_already_stamped(self, bot):
        assert bot.check_exclude(tweet(favorited=True)) is True

    def test_reply_post(self, bot):
        assert bot.check_exclude(tweet(in_reply_to_post_id="p0")) is True

    def test_long_text(self, bot):
        assert bot.check_exclude(tweet(text="あ" * 80)) is True

    def test_ng_word_in_text(self, bot):
        assert bot.check_exclude(tweet(text="http://spam ばおわ")) is True

    def test_ng_user(self, bot):
        assert bot.check_exclude(tweet(name="副業で稼ぐ", desc="")) is True


class Test_check_reply:
    def test_trigger(self, bot):
        assert bot.check_reply(tweet(text="疲れた")) is True

    def test_no_trigger(self, bot):
        assert bot.check_reply(tweet(text="こんにちは")) is False


class Test_praise:
    def test_dry_run_builds_text_and_counts(self, bot):
        result = bot.praise(tweet(screen="taro", name="太郎＠多忙"))
        assert result.startswith("@taro\n太郎")  # @以降が落ち正規化される
        assert "お疲れ様だもん" in result
        assert bot.counts["praise"] == 1
        assert bot._replies_done == 1
        bot.client.create_post.assert_not_called()  # dry-run

    def test_reply_text_truncated_to_max(self, bot):
        bot.max_post_len = 10
        assert len(bot.praise(tweet())) == 10


class Test_run:
    def test_classifies_caps_and_saves_cursor(self, bot):
        # 3件のトリガー投稿（cap=2）+ 1件の無反応
        posts = [
            make_post("p1", "u1", "ばおわ", 100),
            make_post("p2", "u2", "疲れた", 300),  # 最新
            make_post("p3", "u3", "退勤", 200),
            make_post("p4", "u4", "ただの雑談", 150),
        ]
        bot.client.get_community_timeline.return_value = posts
        bot.client.get_users.return_value = [
            user_pb2.User(user_id="u%d" % i, name="h%d" % i, display_name="n%d" % i)
            for i in range(1, 5)
        ]
        bot.run()
        assert bot.counts["praise"] == 2  # cap=2
        assert bot.counts["capped"] == 1
        assert bot.counts["pass"] == 1
        # since_cursor は今回未指定で呼ばれる（初回）
        bot.client.get_community_timeline.assert_called_once_with(
            "c1", since_cursor=None
        )
        # 最新 created_at の p2 がカーソルに保存される
        assert bot.load_cursor() == "p2"

    def test_second_run_uses_saved_cursor(self, bot):
        bot.save_cursor("p2")
        bot.client.get_community_timeline.return_value = []
        bot.client.get_users.return_value = []
        bot.run()
        bot.client.get_community_timeline.assert_called_once_with(
            "c1", since_cursor="p2"
        )


class Test_newest_post_id:
    def test_picks_max_created_at(self):
        posts = [
            make_post("a", "u", "x", 10),
            make_post("b", "u", "x", 99),
            make_post("c", "u", "x", 50),
        ]
        assert hometamon_mixi2.HometamonMixi2.newest_post_id(posts) == "b"

    def test_empty(self):
        assert hometamon_mixi2.HometamonMixi2.newest_post_id([]) is None
