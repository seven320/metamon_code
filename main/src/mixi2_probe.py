# encoding utf-8
"""mixi2 接続の疎通確認とスタンプ列挙ヘルパー（読み取りのみ・書き込みしない）。

資格情報と COMMUNITY_ID が揃ったら、本番投入前にこれを実行して
  (1) 認証・gRPC接続が通るか
  (2) GetCommunityTimeline が取れるか（巡回対象の確認）
  (3) 使えるスタンプID一覧（PRAISE_STAMP_ID の選定用）
を確認する。

使い方:
    cd main && uv run python -m src.mixi2_probe
    # コンテナ内: docker exec hometamon python3 -m src.mixi2_probe
"""

import os
import sys

from dotenv import load_dotenv

pardir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if pardir not in sys.path:
    sys.path.append(pardir)

from src import mixi2_client  # noqa: E402
from src.mixi2_client import Mixi2Client  # noqa: E402


def _load_env():
    if os.path.exists("/env/.env"):
        load_dotenv("/env/.env")
    elif os.path.exists("env/.env"):
        load_dotenv("env/.env")


def probe_installed_communities(client, community_id):
    cua = client.get_communities_using_application()
    print("== 導入済みコミュニティ: {} 件 ==".format(len(cua)))
    found = False
    for c in cua:
        is_target = c.community.community_id == community_id
        found = found or is_target
        mark = "★" if is_target else "  "
        print(
            "  {}{} {} (v={})".format(
                mark,
                c.community.community_id,
                c.community.name,
                c.application_version_id,
            )
        )
    if found:
        print("→ 対象コミュニティに導入済み OK")
    else:
        print("→ ⚠️ 対象 COMMUNITY_ID が導入一覧に無い（IDか導入状況を確認）")
    return found


def probe_timeline(client, community_id, limit=5):
    posts = client.get_community_timeline(community_id, since_cursor=None)
    print("== GetCommunityTimeline: {} 件取得 ==".format(len(posts)))
    for p in posts[:limit]:
        text = p.text.replace("\n", " ")
        print("  {} by {}: {}".format(p.post_id, p.creator_id, text[:40]))
    return posts


def probe_stamps(client, community_id):
    resp = client.get_stamps(
        official_language=mixi2_client.LanguageCode.LANGUAGE_CODE_JP,
        community_ids=[community_id] if community_id else None,
    )
    print("== 公式スタンプ ==")
    for s_set in resp.official_stamp_sets:
        ids = ", ".join(s.stamp_id for s in s_set.stamps[:10])
        print("  [{}] {}".format(s_set.name, ids))
    print("== コミュニティスタンプ ==")
    for s_set in resp.community_stamp_sets:
        ids = ", ".join(s.stamp_id for s in s_set.stamps[:10])
        print("  (community {}) {}".format(s_set.community_id, ids))
    print("\n→ 上記から1つ選んで .env の PRAISE_STAMP_ID に設定してください。")


def main():
    _load_env()
    community_id = os.environ.get("COMMUNITY_ID")
    if not community_id:
        print("COMMUNITY_ID が未設定です（.env を確認）")
        return
    client = Mixi2Client.from_env()
    try:
        probe_installed_communities(client, community_id)
        print()
        probe_timeline(client, community_id)
        print()
        probe_stamps(client, community_id)
    finally:
        client.close()


if __name__ == "__main__":
    main()
