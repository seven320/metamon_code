# mixi2版 詳細

現在の稼働対象。mixi2 のコミュニティを巡回し、(1) 褒めトリガー語を含む投稿に返信＋スタンプを付け、(2) 新規参加者に歓迎ポストを投稿する。
概要・実行方法は [../README.md](../README.md) を参照。本書は設計の詳細。

## 設計方針

| 項目 | 決定 | 理由 |
|---|---|---|
| 取得モデル | **コミュニティ巡回型** | mixi2 にはグローバル/ホーム TL を丸ごと取得する API が無い。取得は `GetCommunityTimeline`（コミュニティ単位）が中心 |
| 実行方式 | **cron 定期ポーリング** | 常駐 gRPC ストリーム/Webhook は使わない（運用をシンプルに） |
| 新規参加の検知 | **メンバー一覧のスナップショット差分** | mixi2 は参加日時を返さず、参加イベントは Stream API（常駐）専用。cron では一覧差分でしか検知できない |
| 状態保存 | **Firestore に一本化** | Cloud Run Jobs はファイルが揮発。カーソルと既知メンバーを Firestore に保存（ローカルはエミュレータ） |
| prod/dev 切替 | **`APP_ENV` で `.env` を選択** | dev は別テストコミュニティ。状態は `COMMUNITY_ID` 単位で分離され prod を汚さない |
| bot 感対策 | 返信前ランダム待機・1 起動あたり件数上限 | スパム的挙動の回避 |
| 言語 | Python 継続 | 既存資産活用。公式 SDK は Go のみ・Python 版が無いため proto から自前生成 |

## データフロー（褒め: `hometamon_mixi2.py`）

```
1. token   = OAuth2 client credentials (CLIENT_ID/SECRET → TOKEN_URL)
2. posts   = GetCommunityTimeline(community_id, since_cursor=<Firestoreの最新post_id>)
3. users   = GetUsers([p.creator_id for p in posts])      # Postに作者が埋め込まれないため解決
4. tweets  = adapter(posts, users)                        # 旧tweet風オブジェクトへ変換
5. for tweet: classify → check_exclude / check_reply
6. praise  = CreatePost(返信) + AddStampToPost(スタンプ)
7. 最新 post_id を Firestore に保存（次回の since_cursor）
8. report  = SendDirectMessageToCommunityMember(admin)    # ADMIN_USER_ID 未設定なら print のみ
```

## データフロー（歓迎: `welcome_newcomer.py`）

```
1. members = GetCommunityMemberList(community_id)          # 全メンバー（ページング）。is_disabled / bot自身は除外
2. 初回（ベースライン未投入）: 全員を greeted=True で Firestore に焼き込み終了（挨拶しない）
3. known   = Firestore の既知メンバー集合
4. newcomers = [m for m in members if m.user_id not in known]
5. for user in newcomers（1起動 MAX_GREETS_PER_RUN 件まで・ランダム待機）:
       CreatePost(あいさつ＋使い方案内, community_id)        # @メンション付き公開ポスト
       Firestore に greeted=True で記録
6. report  = SendDirectMessageToCommunityMember(admin)
```

## コンポーネント

| ファイル | 役割 |
|---|---|
| `main/src/hometamon_mixi2.py` | エントリポイント（褒め）。設定読込・巡回・分類・褒め・カーソル・レポート |
| `main/src/welcome_newcomer.py` | エントリポイント（歓迎）。メンバー差分で新規参加者を検知し歓迎ポスト |
| `main/src/mixi2_client.py` | OAuth2 認証＋gRPC 接続ラッパ。bot が使う RPC を高レベル公開 |
| `main/src/mixi2_adapter.py` | mixi2 `Post`/`User` → 旧 tweet 風 `TweetLike` へ変換 |
| `main/src/firestore_store.py` | 状態ストア。カーソル＋既知メンバーを Firestore に保存（ローカルはエミュレータ） |
| `main/src/env_loader.py` | `APP_ENV` に応じて `.env`/`.env.dev` を切替（prod/dev コミュニティ） |
| `main/src/filters.py` | NG ワード・褒めトリガー語・返信/歓迎文の組み立て（X 版と共用） |
| `main/src/meta_manuscript.py` | 褒め文・歓迎文などの定型文リスト |
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

`GetCommunityTimeline` の `since_cursor` に **前回取得した最新 post_id** を渡すと、それより新しい投稿だけ返る。レスポンスに next_cursor は無いので、取得結果のうち `created_at` 最新の `post_id` を **Firestore** に永続化する（`FirestoreStore`、後述）。

> 二重褒めはカーソルに加え `reader_stamp_id` でも防がれる: 褒めた投稿には毎回スタンプが付く → 次回 `reader_stamp_id` 検出で除外される。カーソルが万一飛んでも実害が出にくい二重の安全。

## 状態保存（Firestore）

褒めのカーソルと歓迎の既知メンバーは `FirestoreStore`（`firestore_store.py`）に集約する。

```
communities/{community_id}
  ├─ cursor:                 最後に読んだ post_id（褒め）
  ├─ members_baseline_done:  歓迎のベースライン投入済みか
  └─ members/{user_id}
       ├─ display_name, name
       ├─ first_seen_at:  初めてメンバー一覧で観測した時刻
       ├─ greeted:        歓迎済みか
       └─ greeted_at
```

- ローカル/CI は Firestore エミュレータ（`FIRESTORE_EMULATOR_HOST`、docker-compose の `firestore` サービス）。本番 Cloud Run は ADC で実 Firestore。実装クラスは 1 つで接続先だけ変わる。
- 1 メンバー = 1 ドキュメントの素直な形にし `first_seen_at`/`greeted_at` を残すことで、将来の Firestore→BigQuery 連携にも素直に流せる。
- 単一 writer（cron）前提なのでトランザクションは使わない。

## 歓迎機能（新規参加者の検知）

mixi2 は「いつ参加したか」を返さず、参加イベントは Stream API（常駐）専用。cron 運用では `GetCommunityMemberList` の**スナップショット差分**でしか新規参加を検知できない。

- 既知メンバー集合を Firestore に保持し、一覧に居て集合に無い `user_id` を新規とみなす。
- **初回はベースラインのみ**: 既存メンバー全員を `greeted=True` で焼き込み、誰にも挨拶しない（コールドスタートで全員に挨拶する事故を防ぐ）。
- 1 起動 `MAX_GREETS_PER_RUN` 件まで。超過分は記録せず次回に持ち越す。
- 退会→再入会は再び新規扱いになる（軽微・許容）。
- 挨拶文は `filters.build_welcome_message`（あいさつ＋使い方案内、@メンション付き）で組み立て、`meta_manuscript.welcome` / `welcome_guide` を文面源とする。

## prod/dev 環境切替（APP_ENV）

実行時の環境変数 `APP_ENV` で読み込む `.env` を切り替える（`env_loader.load_env`）。

- `APP_ENV=dev` → `env/.env.dev`（dev テストコミュニティ）/ 未指定 → `env/.env`（prod）
- 同じアプリを prod/dev 両コミュニティに導入すれば、認証情報は共通で `COMMUNITY_ID` だけ差し替えればよい。
- 状態は Firestore に `COMMUNITY_ID` 単位で分かれるため、dev は prod のカーソル/メンバーを汚さない。
- ローカル例: `docker compose run --rm --no-deps -e APP_ENV=dev metamon python3 src/welcome_newcomer.py`

## スタンプ（旧ファボの代替）

`AddStampToPost(post_id, stamp_id)`。`stamp_id` は `GetStamps` で取得（`mixi2_probe` が列挙）。公式スタンプ ID（例 `o_hearts`＝💕）はどのポストにも使える。コミュニティ固有スタンプはそのコミュニティの投稿にのみ。

## bot 感対策・運用パラメータ

返信前に `POLL_MIN_SLEEP`〜`POLL_MAX_SLEEP` 秒のランダム待機。1 起動あたり `MAX_REPLIES_PER_RUN` 件まで。これらの既定値は `hometamon_mixi2.py` の `DEFAULT_*` 定数（秘密ではないので `.env` には置かず、環境変数で上書き可）。

## 制約・既知事項

- **レート制限: 全 RPC 1 分 20 リクエスト**。`MAX_REPLIES_PER_RUN=5` なら 1 起動約 13 コールで安全圏。
- **必要なプラグイン権限（Requirement）5 つ**: `Community.Post.Read`(=1) / `Community.Post.Create`(=2) / `Community.Member.List.Read`(=4・歓迎の新規検知) / `Community.Post.Stamp.Create`(=10) / `Community.Member.DirectMessage.Create`(=11)。
  - 罠: 新バージョンに権限を足すとき `Community.Post.Create` を落とすと、**メンバー一覧取得は成功するのに `CreatePost` が `NOT_FOUND: CommunityReader.IsAdmin ...` で失敗**する（その権限グラントのレコードが無い意）。requirements は全部揃えて新バージョン作成 → コミュニティで再インストール。
- **編集された既処理ポストは再取得されない**（カーソルは作成順ベース＝編集で位置が変わらないため）。本番運用＝新規投稿に反応、なので実害なし。
- `BOT_USER_ID` は本来 user_id(UUID)。現状ハンドルでも返信除外でカバーされる。

## proto / 生成コード

公式 proto（[mixigroup/mixi2-api](https://github.com/mixigroup/mixi2-api)）を `main/proto/` に vendor し、`make gen-proto`（`grpc_tools.protoc`）で `main/src/mixi2_gen/` に Python スタブを生成。生成物はコミット対象（ランタイムは grpcio+protobuf のみで動く）。`.gitattributes` で生成物/vendor を `linguist-generated`/`vendored` 指定し、GitHub の diff/統計から除外している。mixi2 が API を更新したら proto を取り込み直して再生成する。
