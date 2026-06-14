# encoding utf-8
"""bot の永続状態を Firestore に集約するストア層。

褒めbotの差分カーソルと、歓迎botのメンバー記録（誰に挨拶済みか）を 1 つの
バックエンドにまとめる。ローカル/CI は Firestore エミュレータ（環境変数
`FIRESTORE_EMULATOR_HOST` を指す）に向け、本番 Cloud Run Jobs は ADC で実
Firestore に繋ぐ。接続先が違うだけで実装はこのクラス 1 つに統一する。

将来 BigQuery へ流す（Firestore→BigQuery 連携）ことを見据え、ドキュメントは
1 メンバー = 1 ドキュメントの素直な形にし、first_seen_at / greeted_at を残す。

データモデル:
    communities/{community_id}
        cursor:                 str    褒めbotが最後に読んだ post_id
        members_baseline_done:  bool   初回ベースライン投入済みか
        members/{user_id}
            display_name, name
            first_seen_at:  timestamp  初めてメンバー一覧で観測した時刻
            greeted:        bool       歓迎ポスト済みか
            greeted_at:     timestamp  歓迎した時刻（未挨拶なら未設定）

env:
    GOOGLE_CLOUD_PROJECT    Firestore のプロジェクトID（エミュレータでは任意の文字列）
    FIRESTORE_EMULATOR_HOST 任意。設定するとエミュレータに接続（ローカル/CI用）
"""

import os

_COMMUNITIES = "communities"
_MEMBERS = "members"


class FirestoreStore:
    def __init__(self, project=None, client=None):
        """Firestore クライアントを用意する（client 注入時はそれを使う＝テスト用）。"""
        if client is not None:
            self._db = client
            self._firestore = None
        else:
            from google.cloud import firestore  # 遅延importでテストの依存を避ける

            self._firestore = firestore
            self._db = firestore.Client(
                project=project or os.environ.get("GOOGLE_CLOUD_PROJECT")
            )

    def _server_timestamp(self):
        # 注入クライアント（テスト）では firestore モジュールを持たないため、
        # その場合はナイーブなセンチネル文字列で代替する。
        if self._firestore is not None:
            return self._firestore.SERVER_TIMESTAMP
        return "SERVER_TIMESTAMP"

    def _community_ref(self, community_id):
        """コミュニティのドキュメント参照を返す。"""
        return self._db.collection(_COMMUNITIES).document(community_id)

    def _members_col(self, community_id):
        """コミュニティ配下のメンバー・サブコレクション参照を返す。"""
        return self._community_ref(community_id).collection(_MEMBERS)

    def _greeted_member_payload(self, user):
        """「挨拶済みメンバー」ドキュメントの内容を組み立てる（書き込み共通）。"""
        return {
            "display_name": user.display_name,
            "name": user.name,
            "first_seen_at": self._server_timestamp(),
            "greeted": True,
            "greeted_at": self._server_timestamp(),
        }

    # ---- 褒めbotのカーソル ------------------------------------------------
    def load_cursor(self, community_id):
        """最後に読んだ post_id（カーソル）を返す。未保存なら None。"""
        snap = self._community_ref(community_id).get()
        if getattr(snap, "exists", False):
            return (snap.to_dict() or {}).get("cursor")
        return None

    def save_cursor(self, community_id, post_id):
        """カーソル（最新 post_id）を保存する。"""
        self._community_ref(community_id).set({"cursor": post_id}, merge=True)

    # ---- 歓迎botのメンバー記録 --------------------------------------------
    def is_members_baseline_done(self, community_id):
        """初回ベースライン投入が済んでいるかを返す。"""
        snap = self._community_ref(community_id).get()
        if getattr(snap, "exists", False):
            return bool((snap.to_dict() or {}).get("members_baseline_done"))
        return False

    def seed_members_baseline(self, community_id, members):
        """初回のベースライン投入。既存メンバー全員を greeted=True で焼き込み、
        以降は一覧に居ない user_id だけが新規参加者として検知される。"""
        for user in members:
            self._members_col(community_id).document(user.user_id).set(
                self._greeted_member_payload(user), merge=True
            )
        self._community_ref(community_id).set(
            {"members_baseline_done": True}, merge=True
        )

    def known_member_ids(self, community_id):
        """記録済み（＝既知）メンバーの user_id 集合を返す。"""
        return {doc.id for doc in self._members_col(community_id).stream()}

    def record_greeted_member(self, community_id, user):
        """挨拶した新規参加者を greeted=True で記録する。"""
        self._members_col(community_id).document(user.user_id).set(
            self._greeted_member_payload(user), merge=True
        )
