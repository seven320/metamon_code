# encoding utf-8
"""褒めたもん mixi2版：コミュニティ新規参加者への歓迎機能。

専用コミュニティのメンバー一覧を取得し、前回までに観測していなかった
ユーザー（＝新しく入ってきた人）を検知して、コミュニティへ歓迎の公開
ポストを投稿する。

mixi2 の Application API はメンバーの「参加日時」を返さず、cron ポーリング
では参加イベントも受け取れないため、メンバー一覧のスナップショット差分で
新規参加者を検知する。状態（既知メンバー集合）は Firestore に永続化する。

初回（ベースライン未投入）は既存メンバー全員を「挨拶済み」として焼き込む
だけで、誰にも挨拶しない（コールドスタートで全員に挨拶する事故を防ぐ）。

実行は cron による定期ポーリングを想定（褒めbotとは別頻度でよい）。

env:
    （接続系は mixi2_client.Mixi2Client.from_env を参照）
    （状態保存は firestore_store.FirestoreStore を参照）
    COMMUNITY_ID         巡回対象コミュニティID
    ADMIN_USER_ID        実行レポートのDM送信先ユーザーID（任意）
    BOT_USER_ID          bot自身のユーザーID（メンバー一覧から除外／任意）
    MAX_GREETS_PER_RUN   1起動あたりの挨拶上限（既定5）
    POLL_MIN_SLEEP       挨拶前ランダム待機の下限秒（既定3）
    POLL_MAX_SLEEP       挨拶前ランダム待機の上限秒（既定12）
    MAX_POST_LEN         挨拶本文の最大文字数（既定150）
    MIXI2_DRY_RUN        "1" で書き込みRPCを実行せずログのみ（疎通/動作確認用）
"""

import os
import sys
import random
import time
import datetime as dt

# スクリプトとして直接実行されても `from src import ...` が解決できるようにする
pardir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if pardir not in sys.path:
    sys.path.append(pardir)

from src import meta_manuscript  # noqa: E402
from src import filters  # noqa: E402
from src import env_loader  # noqa: E402
from src.mixi2_client import Mixi2Client  # noqa: E402

# 運用チューニングの既定値。秘密ではないので .env には置かず、ここを真実源とする。
# 注: mixi2は全RPCで 20 req/min 制限。メンバー一覧の取得とポストでRPCを使う。
DEFAULT_MAX_GREETS_PER_RUN = 5
DEFAULT_POLL_MIN_SLEEP = 3.0
DEFAULT_POLL_MAX_SLEEP = 12.0
DEFAULT_MAX_POST_LEN = 150


class WelcomeNewcomer:
    def __init__(self, client=None, store=None):
        """env を読み込み、クライアント・ストア・運用パラメータを初期化する。"""
        env_loader.load_env()

        self.client = client if client is not None else Mixi2Client.from_env()
        if store is not None:
            self.store = store
        else:
            from src.firestore_store import FirestoreStore

            self.store = FirestoreStore()
        self.manuscript = meta_manuscript.Manuscript()

        self.community_id = os.environ.get("COMMUNITY_ID")
        self.admin_user_id = os.environ.get("ADMIN_USER_ID")
        self.bot_user_id = os.environ.get("BOT_USER_ID")
        self.max_greets = int(
            os.environ.get("MAX_GREETS_PER_RUN", DEFAULT_MAX_GREETS_PER_RUN)
        )
        self.min_sleep = float(os.environ.get("POLL_MIN_SLEEP", DEFAULT_POLL_MIN_SLEEP))
        self.max_sleep = float(os.environ.get("POLL_MAX_SLEEP", DEFAULT_POLL_MAX_SLEEP))
        self.max_post_len = int(os.environ.get("MAX_POST_LEN", DEFAULT_MAX_POST_LEN))
        self.dry_run = os.environ.get("MIXI2_DRY_RUN") == "1"

        JST = dt.timezone(dt.timedelta(hours=+9), "JST")
        self.JST = dt.datetime.now(JST)
        self.counts = {"greeted": 0, "capped": 0, "baseline": 0}

    # ---- 取得 -------------------------------------------------------------
    def fetch_members(self):
        """除外対象（無効化ユーザー・bot自身）を除いたメンバー一覧を返す。"""
        members = self.client.get_community_member_list(self.community_id)
        result = []
        for user in members:
            if user.is_disabled:
                continue
            if self.bot_user_id and user.user_id == self.bot_user_id:
                continue
            result.append(user)
        return result

    # ---- 挨拶 -------------------------------------------------------------
    def build_welcome_text(self, user):
        """歓迎ポスト本文を組み立てる（あいさつ＋使い方案内、上限で切り詰め）。"""
        body = (
            random.choice(self.manuscript.welcome)
            + "\n"
            + self.manuscript.welcome_guide
        )
        text = filters.build_welcome_message(user.name, user.display_name, body)
        return text[: self.max_post_len]

    def greet(self, user):
        """1人の新規参加者へ歓迎ポストを投稿する（dry-runならログのみ）。"""
        text = self.build_welcome_text(user)
        time.sleep(random.uniform(self.min_sleep, self.max_sleep))  # bot感対策
        if self.dry_run:
            print("[dry-run] welcome {}: {}".format(user.user_id, text))
        else:
            self.client.create_post(text, community_id=self.community_id)
        self.counts["greeted"] += 1
        return text

    # ---- レポート ---------------------------------------------------------
    def report(self):
        """今回の挨拶結果を管理者へDM（dry-runならログのみ）し、本文を返す。"""
        if self.counts["baseline"]:
            body = "新規メンバー基準を{}人で初期化しただもん（今回は挨拶なし）".format(
                self.counts["baseline"]
            )
        else:
            body = "挨拶した数:{}\n上限見送り:{}".format(
                self.counts["greeted"], self.counts["capped"]
            )
        result = "time:{}\n{}\n(mixi2/welcome)".format(
            self.JST.strftime("%Y/%m/%d %H:%M:%S"), body
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
        """メンバー差分で新規参加者を検知し、上限内で挨拶してレポートする。"""
        members = self.fetch_members()

        # 初回はベースラインだけ作って終了（既存メンバーには挨拶しない）
        if not self.store.is_members_baseline_done(self.community_id):
            self.store.seed_members_baseline(self.community_id, members)
            self.counts["baseline"] = len(members)
            self.report()
            return

        known = self.store.known_member_ids(self.community_id)
        newcomers = [u for u in members if u.user_id not in known]
        for user in newcomers:
            if self.counts["greeted"] >= self.max_greets:
                # 上限超過分は記録せず据え置き、次回起動で挨拶する
                self.counts["capped"] += 1
                continue
            self.greet(user)
            self.store.record_greeted_member(self.community_id, user)
        self.report()


def main():
    WelcomeNewcomer().run()


if __name__ == "__main__":
    main()
