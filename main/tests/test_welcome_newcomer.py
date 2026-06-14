import pytest

from src import mixi2_client  # noqa: F401  (生成スタブの path を通す)
from src import welcome_newcomer
from tests.fakes import InMemoryStore

from social.mixi.application.model.v1 import user_pb2


def user(uid, name="h", display="n", disabled=False):
    return user_pb2.User(
        user_id=uid, name=name, display_name=display, is_disabled=disabled
    )


@pytest.fixture
def store():
    return InMemoryStore()


@pytest.fixture
def bot(mocker, monkeypatch, store):
    monkeypatch.setenv("MIXI2_DRY_RUN", "1")
    monkeypatch.setenv("MAX_GREETS_PER_RUN", "2")
    monkeypatch.setenv("POLL_MIN_SLEEP", "0")
    monkeypatch.setenv("POLL_MAX_SLEEP", "0")
    monkeypatch.setenv("COMMUNITY_ID", "c1")
    monkeypatch.setenv("BOT_USER_ID", "bot1")
    mocker.patch("src.welcome_newcomer.time.sleep")
    client = mocker.Mock()
    b = welcome_newcomer.WelcomeNewcomer(client=client, store=store)
    b.manuscript = mocker.Mock()
    b.manuscript.welcome = ["ようこそだもん"]
    b.manuscript.welcome_guide = "ここで「ほめて」ってかくとほめるもん"
    return b


class Test_fetch_members:
    def test_excludes_bot_self_and_disabled(self, bot):
        bot.client.get_community_member_list.return_value = [
            user("u1"),
            user("bot1"),  # bot自身
            user("u2", disabled=True),  # 無効化
            user("u3"),
        ]
        ids = [u.user_id for u in bot.fetch_members()]
        assert ids == ["u1", "u3"]


class Test_run_baseline:
    def test_first_run_seeds_and_greets_nobody(self, bot, store):
        bot.client.get_community_member_list.return_value = [user("u1"), user("u2")]
        bot.run()
        assert bot.counts["greeted"] == 0
        assert bot.counts["baseline"] == 2
        assert store.is_members_baseline_done("c1")
        assert store.known_member_ids("c1") == {"u1", "u2"}
        bot.client.create_post.assert_not_called()


class Test_run_newcomers:
    def test_greets_only_unknown_members(self, bot, store):
        store.seed_members_baseline("c1", [user("u1")])
        bot.client.get_community_member_list.return_value = [user("u1"), user("u2")]
        bot.run()
        assert bot.counts["greeted"] == 1  # u2 のみ
        assert "u2" in store.known_member_ids("c1")

    def test_caps_and_leaves_overflow_for_next_run(self, bot, store):
        store.seed_members_baseline("c1", [user("u0")])
        # 既知u0 + 新規3人。cap=2 なので2人だけ挨拶し、残り1人は記録せず据え置く
        bot.client.get_community_member_list.return_value = [
            user("u0"),
            user("u1"),
            user("u2"),
            user("u3"),
        ]
        bot.run()
        assert bot.counts["greeted"] == 2
        assert bot.counts["capped"] == 1
        greeted_new = store.known_member_ids("c1") - {"u0"}
        assert len(greeted_new) == 2  # 挨拶した2人だけ記録、残り1人は次回へ

    def test_no_newcomers_does_nothing(self, bot, store):
        store.seed_members_baseline("c1", [user("u1"), user("u2")])
        bot.client.get_community_member_list.return_value = [user("u1"), user("u2")]
        bot.run()
        assert bot.counts["greeted"] == 0
        assert bot.counts["capped"] == 0


class Test_build_welcome_text:
    def test_format_and_truncation(self, bot):
        text = bot.build_welcome_text(user("u1", name="taro", display="太郎＠多忙"))
        assert text.startswith("@taro\n太郎")  # @以降が落ち正規化される
        assert "ようこそだもん" in text  # あいさつ
        assert "ほめて" in text  # 使い方案内（何をすれば良いか）も含む

    def test_truncated_to_max(self, bot):
        bot.max_post_len = 5
        assert len(bot.build_welcome_text(user("u1"))) == 5


class Test_greet_writes:
    def test_non_dry_run_creates_post(self, bot, monkeypatch, store):
        monkeypatch.setenv("MIXI2_DRY_RUN", "0")
        bot.dry_run = False
        store.seed_members_baseline("c1", [])
        bot.client.get_community_member_list.return_value = [user("u1")]
        bot.run()
        bot.client.create_post.assert_called_once()
        _, kwargs = bot.client.create_post.call_args
        assert kwargs["community_id"] == "c1"
