# 褒めたもん 現状メモ

最終更新: 2026-06（mixi2移行・歓迎機能・Firestore化）

> 使い方・構成は [README.md](README.md) を参照。本ファイルは進捗と残課題のログ。

## 現状
- **「褒める」機能の mixi2 移行が完了**（実環境でエンドツーエンド動作確認済み：返信＋スタンプ付与まで成功）。mixi2 が現在の稼働対象。
- **返信に画像添付**（X版踏襲、確率 `IMAGE_RATIO` 既定0.2）。`InitiatePostMediaUpload`→upload_url へ POST→`GetPostMediaStatus` 完了待ち→`CreatePost(media_id_list)`。dev で実投稿まで確認済み。
- **新規参加者への「歓迎」機能を追加**（Phase1）。コミュニティのメンバー一覧の差分で新規参加を検知し、あいさつ＋使い方案内をコミュニティへ公開ポストする。dev コミュニティで実投稿まで確認済み。
- **状態保存を Firestore に一本化**。褒めのカーソル（最新 post_id）と歓迎の既知メンバー集合を Firestore に保存（旧 `state/mixi2_cursor.txt` は廃止）。ローカル/CI は Firestore エミュレータ、本番 Cloud Run は ADC で実 Firestore。
- **prod/dev のコミュニティ切替**に対応。実行時の環境変数 `APP_ENV=dev` で `env/.env.dev`（別テストコミュニティ）を読む。状態は `COMMUNITY_ID` 単位で分かれるため prod を汚さない。
- X 版コードはレガシーとして残置（削除せず分岐から外しただけ）。デプロイ対象ではない。
- 実行経路: コミュニティ巡回型。cron で **褒め=`hometamon_mixi2.py`（15分）／歓迎=`welcome_newcomer.py`（1時間）** を定期実行 → 差分取得 → 分類/検知 → 返信＋スタンプ／歓迎ポスト → DM レポート。
- テスト: `cd main && uv run pytest`（X版＋mixi2版で計 95 件 green）。`black --check` も通過。

## 残課題 / TODO
- [ ] Cloud Run へのデプロイ（cron → Cloud Run Jobs + Scheduler、Firestore は本番プロジェクトへ）。手順メモは `CLOUD_RUN.md`。
- [ ] `.env` の `ADMIN_USER_ID` 記入（レポート DM を有効化したい場合）。
- [ ] `BOT_USER_ID` を UUID 化（任意。現状はハンドルだが返信除外でカバー済み）。
- [ ] （任意）CI に「proto から再生成して差分が出たら落とす」チェックを追加。

## スコープ外（レガシー機能・未移行）
朝/夜挨拶・15 時お菓子投稿・LINE スタンプ宣伝・フォロー管理。
コードは X 版に残るが mixi2 では非対応 or 未移行。
