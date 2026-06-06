import sys

# mixi2_client の import で生成スタブの path が通る
from src import mixi2_client  # noqa: F401
from src import mixi2_adapter

from social.mixi.application.model.v1 import post_pb2, user_pb2


def make_post(post_id, creator_id, text, **kw):
    return post_pb2.Post(post_id=post_id, creator_id=creator_id, text=text, **kw)


def make_user(user_id, name, display_name, profile="", is_disabled=False):
    return user_pb2.User(
        user_id=user_id,
        name=name,
        display_name=display_name,
        profile=profile,
        is_disabled=is_disabled,
    )


class Test_adapt_posts:
    def test_maps_fields(self):
        posts = [make_post("p1", "u1", "ばおわ")]
        users = {"u1": make_user("u1", "handle1", "ひょうじ名", "プロフ")}
        tweets = mixi2_adapter.adapt_posts(posts, users)
        assert len(tweets) == 1
        t = tweets[0]
        assert t.id == "p1"
        assert t.text == "ばおわ"
        assert t.favorited is False  # reader_stamp_id 未設定
        assert t.user.id == "u1"
        assert t.user.screen_name == "handle1"  # User.name
        assert t.user.name == "ひょうじ名"  # User.display_name
        assert t.user.description == "プロフ"  # User.profile

    def test_favorited_from_reader_stamp_id(self):
        posts = [make_post("p1", "u1", "x", reader_stamp_id="s9")]
        users = {"u1": make_user("u1", "h", "n")}
        assert mixi2_adapter.adapt_posts(posts, users)[0].favorited is True

    def test_reply_and_community_fields(self):
        posts = [
            make_post("p1", "u1", "x", in_reply_to_post_id="p0", community_id="c1")
        ]
        users = {"u1": make_user("u1", "h", "n")}
        t = mixi2_adapter.adapt_posts(posts, users)[0]
        assert t.in_reply_to_post_id == "p0"
        assert t.community_id == "c1"

    def test_skips_deleted_post(self):
        posts = [make_post("p1", "u1", "x", is_deleted=True)]
        users = {"u1": make_user("u1", "h", "n")}
        assert mixi2_adapter.adapt_posts(posts, users) == []

    def test_skips_unresolvable_or_disabled_user(self):
        posts = [
            make_post("p1", "u_missing", "x"),
            make_post("p2", "u_disabled", "x"),
        ]
        users = {"u_disabled": make_user("u_disabled", "h", "n", is_disabled=True)}
        assert mixi2_adapter.adapt_posts(posts, users) == []


class Test_build_tweets:
    def test_dedups_creator_ids_and_resolves(self, mocker):
        posts = [
            make_post("p1", "u1", "a"),
            make_post("p2", "u1", "b"),  # 同一作成者
            make_post("p3", "u2", "c"),
            make_post("p4", "u3", "d", is_deleted=True),  # 削除→ID収集しない
        ]
        client = mocker.Mock()
        client.get_users.return_value = [
            make_user("u1", "h1", "n1"),
            make_user("u2", "h2", "n2"),
        ]
        tweets = mixi2_adapter.build_tweets(client, posts)
        # 重複排除して u1,u2 のみ問い合わせ（順序保持）
        client.get_users.assert_called_once_with(["u1", "u2"])
        assert [t.id for t in tweets] == ["p1", "p2", "p3"]
