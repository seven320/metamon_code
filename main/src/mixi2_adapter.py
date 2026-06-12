# encoding utf-8
"""mixi2 の Post / User を、既存 Hometamon ロジックが期待する tweet 風オブジェクトに
変換するアダプタ層。

mixi2 の Post には作成者ユーザーが埋め込まれず `creator_id` のみを持つため、
タイムライン取得後に GetUsers でまとめてユーザーを解決して join する必要がある。
この層がその解決と変換を担い、既存の除外ロジック・褒めロジックを無改修で使えるようにする。

旧 tweepy 属性との対応:
    tweet.id                 -> Post.post_id
    tweet.text               -> Post.text
    tweet.favorited          -> Post.reader_stamp_id が設定済みか（自アプリがスタンプ済み）
    tweet.user.id            -> User.user_id
    tweet.user.screen_name   -> User.name        （ハンドル相当）
    tweet.user.name          -> User.display_name（表示名）
    tweet.user.description   -> User.profile
"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class UserLike:
    id: str
    screen_name: str  # ハンドル（User.name）
    name: str  # 表示名（User.display_name）
    description: str  # プロフィール（User.profile）


@dataclass
class TweetLike:
    id: str
    text: str
    favorited: bool
    user: UserLike
    in_reply_to_post_id: Optional[str] = None
    community_id: Optional[str] = None


def _user_like(user) -> UserLike:
    return UserLike(
        id=user.user_id,
        screen_name=user.name,
        name=user.display_name,
        description=user.profile or "",
    )


def adapt_posts(posts, users_by_id) -> List[TweetLike]:
    """Post 一覧と user_id->User の辞書から TweetLike 一覧を作る。

    削除済みポスト、作成者を解決できないポスト、無効化ユーザーのポストは除外する。
    """
    tweets = []
    for post in posts:
        if post.is_deleted:
            continue
        user = users_by_id.get(post.creator_id)
        if user is None or user.is_disabled:
            continue
        tweets.append(
            TweetLike(
                id=post.post_id,
                text=post.text,
                favorited=bool(post.reader_stamp_id),
                user=_user_like(user),
                in_reply_to_post_id=post.in_reply_to_post_id or None,
                community_id=post.community_id or None,
            )
        )
    return tweets


def build_tweets(client, posts) -> List[TweetLike]:
    """client.get_users で作成者をバッチ解決し、TweetLike 一覧に変換する。"""
    creator_ids = []
    seen = set()
    for post in posts:
        if post.is_deleted:
            continue
        cid = post.creator_id
        if cid and cid not in seen:
            seen.add(cid)
            creator_ids.append(cid)
    users = client.get_users(creator_ids)
    users_by_id = {u.user_id: u for u in users}
    return adapt_posts(posts, users_by_id)
