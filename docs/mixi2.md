# mixi2版 詳細

現在の稼働対象。mixi2 のコミュニティを巡回し、褒めトリガー語を含む投稿に返信＋スタンプを付ける。
概要・実行方法は [../README.md](../README.md) を参照。本書は設計の詳細。

## 設計方針

| 項目 | 決定 | 理由 |
|---|---|---|
| 取得モデル | **コミュニティ巡回型** | mixi2 にはグローバル/ホーム TL を丸ごと取得する API が無い。取得は `GetCommunityTimeline`（コミュニティ単位）が中心 |
| 実行方式 | **cron 定期ポーリング** | 常駐 gRPC ストリーム/Webhook は使わない（運用をシンプルに） |
| bot 感対策 | 返信前ランダム待機・1 起動あたり返信件数上限 | スパム的挙動の回避 |
| 言語 | Python 継続 | 既存資産活用。公式 SDK は Go のみ・Python 版が無いため proto から自前生成 |

## データフロー

```
1. token   = OAuth2 client credentials (CLIENT_ID/SECRET → TOKEN_URL)
2. posts   = GetCommunityTimeline(community_id, since_cursor=<保存した最新post_id>)
3. users   = GetUsers([p.creator_id for p in posts])      # Postに作者が埋め込まれないため解決
4. tweets  = adapter(posts, users)                        # 旧tweet風オブジェクトへ変換
5. for tweet: classify → check_exclude / check_reply
6. praise  = CreatePost(返信) + AddStampToPost(スタンプ)
7. 最新 post_id を state/ に保存（次回の since_cursor）
8. report  = SendDirectMessageToCommunityMember(admin)    # ADMIN_USER_ID 未設定なら print のみ
```

## コンポーネント

| ファイル | 役割 |
|---|---|
| `main/src/hometamon_mixi2.py` | エントリポイント。設定読込・巡回・分類・褒め・カーソル・レポート |
| `main/src/mixi2_client.py` | OAuth2 認証＋gRPC 接続ラッパ。bot が使う RPC を高レベル公開 |
| `main/src/mixi2_adapter.py` | mixi2 `Post`/`User` → 旧 tweet 風 `TweetLike` へ変換 |
| `main/src/filters.py` | NG ワード・褒めトリガー語・返信文組み立て（X 版と共用） |
| `main/src/mixi2_probe.py` | 疎通確認・導入確認・スタンプ列挙（セットアップ補助・読み取りのみ） |
| `main/src/mixi2_gen/` | proto から自動生成した gRPC スタブ（手で触らない） |
| `main/proto/` | mixi2 公式 proto の vendor（生成元） |

各ファイル冒頭の docstring にも詳細あり。

## 認証

OAuth2 **client credentials** grant。`CLIENT_ID`/`CLIENT_SECRET` を **HTTP Basic（RFC6749 §2.3.1 に従い URL エンコード）** で `TOKEN_URL` に投げてアクセストークンを取得し、gRPC メタデータ `authorization: Bearer <token>` で各呼び出しに付与する。トークンは有効期限の 1 分前で先回り再取得。

> `CLIENT_SECRET` に `+ / =` 等が含まれるため、URL エンコードしない生 Basic だと `invalid_client` になる（実際にハマった点）。`API_ADDRESS` はポート未指定なら TLS 既定の `:443` を補完。

## アダプタ（フィールド対応）

mixi2 の `Post` には作者ユーザーが埋め込まれず `creator_id` のみ。よって `GetUsers` でバッチ解決して join する。

| 旧 tweepy | mixi2 |
|---|---|
| `tweet.id` | `Post.post_id` |
| `tweet.text` | `Post.text` |
| `tweet.user.id` | `Post.creator_id` |
| `tweet.user.screen_name` | `User.name`（ハンドル相当） |
| `tweet.user.name` | `User.display_name`（表示名） |
| `tweet.user.description` | `User.profile` |
| `tweet.favorited` | `Post.reader_stamp_id` が設定済みか（自アプリがスタンプ済み） |
| `in_reply_to_status_id` | `Post.in_reply_to_post_id` |

## 分類と除外ロジック

`check_reply`: `filters.PRAISE_WORDS`（`ばおわ`/`疲れた`/`退勤`/`帰宅` 等）を本文が含めば褒める。

`check_exclude`（いずれかに該当で除外）:
- 自分の投稿（`BOT_USER_ID` と一致）
- 既にスタンプ済み（`favorited`＝`reader_stamp_id` あり）
- 返信ポスト（`in_reply_to_post_id` あり）
- 本文 80 字以上
- NG ワードを含む（`filters.EXCLUSION_WORDS`）
- NG ユーザー（名前/プロフィールに NG 語、`filters.is_excluded_user`）

NG ワード群（性的/スパム/投資/医療/副業など）は X 版から流用し `filters.py` に集約。

## 差分取得とカーソル

`GetCommunityTimeline` の `since_cursor` に **前回取得した最新 post_id** を渡すと、それより新しい投稿だけ返る。レスポンスに next_cursor は無いので、取得結果のうち `created_at` 最新の `post_id` を `main/state/mixi2_cursor.txt` に永続化する。

> **ステートレス運用も可能**: カーソルが無くても、褒めた投稿には毎回スタンプが付く → 次回 `reader_stamp_id` 検出で除外され二重褒めしない。Cloud Run 等の揮発環境ではこの性質で成立する。

## スタンプ（旧ファボの代替）

`AddStampToPost(post_id, stamp_id)`。`stamp_id` は `GetStamps` で取得（`mixi2_probe` が列挙）。公式スタンプ ID（例 `o_hearts`＝💕）はどのポストにも使える。コミュニティ固有スタンプはそのコミュニティの投稿にのみ。

## bot 感対策・運用パラメータ

返信前に `POLL_MIN_SLEEP`〜`POLL_MAX_SLEEP` 秒のランダム待機。1 起動あたり `MAX_REPLIES_PER_RUN` 件まで。これらの既定値は `hometamon_mixi2.py` の `DEFAULT_*` 定数（秘密ではないので `.env` には置かず、環境変数で上書き可）。

## 制約・既知事項

- **レート制限: 全 RPC 1 分 20 リクエスト**。`MAX_REPLIES_PER_RUN=5` なら 1 起動約 13 コールで安全圏。
- **必要なプラグイン権限（Requirement）4 つ**: `Community.Post.Read` / `Community.Post.Create` / `Community.Post.Stamp.Create` / `Community.Member.DirectMessage.Create`。
- **編集された既処理ポストは再取得されない**（カーソルは作成順ベース＝編集で位置が変わらないため）。本番運用＝新規投稿に反応、なので実害なし。
- `BOT_USER_ID` は本来 user_id(UUID)。現状ハンドルでも返信除外でカバーされる。

## proto / 生成コード

公式 proto（[mixigroup/mixi2-api](https://github.com/mixigroup/mixi2-api)）を `main/proto/` に vendor し、`make gen-proto`（`grpc_tools.protoc`）で `main/src/mixi2_gen/` に Python スタブを生成。生成物はコミット対象（ランタイムは grpcio+protobuf のみで動く）。`.gitattributes` で生成物/vendor を `linguist-generated`/`vendored` 指定し、GitHub の diff/統計から除外している。mixi2 が API を更新したら proto を取り込み直して再生成する。
