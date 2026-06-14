# encoding utf-8
"""テスト用のインメモリ・ストア。FirestoreStore と同じインターフェースを持ち、
実 Firestore / エミュレータ無しで bot のロジックを検証するために使う。"""


class InMemoryStore:
    def __init__(self):
        self.cursors = {}
        self.baseline_done = set()
        # community_id -> {user_id: {"display_name":..., "name":..., "greeted":bool}}
        self.members = {}

    # ---- カーソル ---------------------------------------------------------
    def load_cursor(self, community_id):
        return self.cursors.get(community_id)

    def save_cursor(self, community_id, post_id):
        self.cursors[community_id] = post_id

    # ---- メンバー記録 -----------------------------------------------------
    def is_members_baseline_done(self, community_id):
        return community_id in self.baseline_done

    def seed_members_baseline(self, community_id, members):
        col = self.members.setdefault(community_id, {})
        for user in members:
            col[user.user_id] = {
                "display_name": user.display_name,
                "name": user.name,
                "greeted": True,
            }
        self.baseline_done.add(community_id)

    def known_member_ids(self, community_id):
        return set(self.members.get(community_id, {}).keys())

    def record_greeted_member(self, community_id, user):
        col = self.members.setdefault(community_id, {})
        col[user.user_id] = {
            "display_name": user.display_name,
            "name": user.name,
            "greeted": True,
        }
