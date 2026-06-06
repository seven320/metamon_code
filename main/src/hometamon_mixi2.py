# encoding utf-8
"""褒めたもん mixi2版。

専用コミュニティを巡回し、褒めトリガー語を含むポストに返信＋スタンプを付与する。
X版 (hometamon.py) の褒め機能だけを移植したもの。挨拶・お菓子・スタンプ宣伝・
フォロー管理はスコープ外。

実行は cron による定期ポーリングを想定。差分取得のため最新 post_id を state/ に永続化する。

env:
    （接続系は mixi2_client.Mixi2Client.from_env を参照）
    COMMUNITY_ID         巡回対象コミュニティID
    ADMIN_USER_ID        実行レポートのDM送信先ユーザーID
    BOT_USER_ID          bot自身のユーザーID（自分の投稿を除外するため／任意）
    PRAISE_STAMP_ID      褒めた際に付与するスタンプID（GetStampsで選定／任意）
    MAX_REPLIES_PER_RUN  1起動あたりの返信上限（既定5）
    POLL_MIN_SLEEP       返信前ランダム待機の下限秒（既定3）
    POLL_MAX_SLEEP       返信前ランダム待機の上限秒（既定12）
    MAX_POST_LEN         返信本文の最大文字数（既定150）
    MIXI2_DRY_RUN        "1" で書き込みRPCを実行せずログのみ（疎通/動作確認用）
"""

import os
import sys
import random
import time
import datetime as dt

from dotenv import load_dotenv

# スクリプトとして直接実行されても `from src import ...` が解決できるようにする
pardir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if pardir not in sys.path:
    sys.path.append(pardir)

from src import meta_manuscript  # noqa: E402
from src import filters  # noqa: E402
from src import mixi2_adapter  # noqa: E402
from src.mixi2_client import Mixi2Client  # noqa: E402

CURSOR_FILENAME = "mixi2_cursor.txt"

# 運用チューニングの既定値。秘密ではないので .env には置かず、ここを真実源とする。
# 変えたい場合のみ同名の環境変数（docker-compose の environment 等）で上書きできる。
# 注: mixi2は全RPCで 20 req/min 制限。MAX_REPLIES=5 なら1run約13コールで安全圏。
DEFAULT_MAX_REPLIES_PER_RUN = 5
DEFAULT_POLL_MIN_SLEEP = 3.0
DEFAULT_POLL_MAX_SLEEP = 12.0
DEFAULT_MAX_POST_LEN = 150


class HometamonMixi2:
    def __init__(self, client=None):
        if os.path.exists("/env/.env"):
            load_dotenv("/env/.env")
        elif os.path.exists("env/.env"):
            load_dotenv("env/.env")
        else:
            print("error doesn't exist .env path")

        self.image_dir = "/images" if os.path.isdir("/images") else "images"
        self.state_dir = "/state" if os.path.isdir("/state") else "state"

        self.client = client if client is not None else Mixi2Client.from_env()
        self.manuscript = meta_manuscript.Manuscript()

        self.community_id = os.environ.get("COMMUNITY_ID")
        self.admin_user_id = os.environ.get("ADMIN_USER_ID")
        self.bot_user_id = os.environ.get("BOT_USER_ID")
        self.praise_stamp_id = os.environ.get("PRAISE_STAMP_ID")
        self.max_replies = int(
            os.environ.get("MAX_REPLIES_PER_RUN", DEFAULT_MAX_REPLIES_PER_RUN)
        )
        self.min_sleep = float(os.environ.get("POLL_MIN_SLEEP", DEFAULT_POLL_MIN_SLEEP))
        self.max_sleep = float(os.environ.get("POLL_MAX_SLEEP", DEFAULT_POLL_MAX_SLEEP))
        self.max_post_len = int(os.environ.get("MAX_POST_LEN", DEFAULT_MAX_POST_LEN))
        self.dry_run = os.environ.get("MIXI2_DRY_RUN") == "1"

        JST = dt.timezone(dt.timedelta(hours=+9), "JST")
        self.JST = dt.datetime.now(JST)
        self.counts = {"ignore": 0, "praise": 0, "pass": 0, "capped": 0}
        self._replies_done = 0

    # ---- カーソル永続化 ---------------------------------------------------
    def _cursor_path(self):
        return os.path.join(self.state_dir, CURSOR_FILENAME)

    def load_cursor(self):
        try:
            with open(self._cursor_path(), encoding="utf-8") as f:
                return f.read().strip() or None
        except FileNotFoundError:
            return None

    def save_cursor(self, post_id):
        os.makedirs(self.state_dir, exist_ok=True)
        with open(self._cursor_path(), "w", encoding="utf-8") as f:
            f.write(post_id)

    @staticmethod
    def newest_post_id(posts):
        """fetchしたポスト群のうち created_at が最新のものの post_id を返す。"""
        newest = None
        newest_key = None
        for p in posts:
            key = (p.created_at.seconds, p.created_at.nanos)
            if newest_key is None or key > newest_key:
                newest_key = key
                newest = p.post_id
        return newest

    # ---- 取得 -------------------------------------------------------------
    def get_posts(self):
        return self.client.get_community_timeline(
            self.community_id, since_cursor=self.load_cursor()
        )

    # ---- 判定 -------------------------------------------------------------
    def check_exclude(self, tweet):
        if self.bot_user_id and tweet.user.id == self.bot_user_id:
            return True  # 自分の投稿
        if tweet.favorited:
            return True  # 既にスタンプ済み（反応済み）
        if tweet.in_reply_to_post_id:
            return True  # 返信ポストには割り込まない
        if len(tweet.text) >= 80:
            return True
        if filters.has_excluded_word(tweet.text):
            return True
        if filters.is_excluded_user(tweet.user.name, tweet.user.description):
            return True
        return False

    def check_reply(self, tweet):
        return filters.is_praise_trigger(tweet.text)

    # ---- 褒める -----------------------------------------------------------
    def build_reply_text(self, tweet):
        reply = filters.build_praise_reply(
            tweet.user.screen_name,
            tweet.user.name,
            random.choice(self.manuscript.reply),
        )
        return reply[: self.max_post_len]

    def praise(self, tweet):
        reply = self.build_reply_text(tweet)
        time.sleep(random.uniform(self.min_sleep, self.max_sleep))  # bot感対策
        if self.dry_run:
            print("[dry-run] reply to {}: {}".format(tweet.id, reply))
        else:
            self.client.create_post(
                reply,
                in_reply_to_post_id=tweet.id,
                community_id=self.community_id,
            )
            if self.praise_stamp_id:
                self.client.add_stamp_to_post(tweet.id, self.praise_stamp_id)
        self.counts["praise"] += 1
        self._replies_done += 1
        return reply

    def classify(self, tweet):
        if self.check_exclude(tweet):
            self.counts["ignore"] += 1
        elif self.check_reply(tweet):
            if self._replies_done >= self.max_replies:
                self.counts["capped"] += 1  # 上限に達したので今回は見送り
            else:
                self.praise(tweet)
        else:
            self.counts["pass"] += 1

    # ---- レポート ---------------------------------------------------------
    def report(self):
        result = (
            "time:{}\n褒めた数:{}\n除外した数:{}\n反応しなかった数:{}\n"
            "上限見送り:{}\n合計:{}だもん！(mixi2)"
        ).format(
            self.JST.strftime("%Y/%m/%d %H:%M:%S"),
            self.counts["praise"],
            self.counts["ignore"],
            self.counts["pass"],
            self.counts["capped"],
            sum(self.counts.values()),
        )
        if self.dry_run:
            print("[dry-run] report:\n" + result)
        elif self.admin_user_id:
            self.client.send_direct_message(
                self.admin_user_id, self.community_id, result
            )
        print(result)
        return result

    # ---- 実行 -------------------------------------------------------------
    def run(self):
        posts = self.get_posts()
        tweets = mixi2_adapter.build_tweets(self.client, posts)
        for tweet in tweets:
            self.classify(tweet)
        newest = self.newest_post_id(posts)
        if newest:
            self.save_cursor(newest)
        self.report()


def main():
    HometamonMixi2().run()


if __name__ == "__main__":
    main()
