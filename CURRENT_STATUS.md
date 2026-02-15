# 褒めたもん（metamon_code）現状整理メモ

最終更新: 2026-02-15（Codex調査）

## 1. 目的と実行の流れ
- `main/src/hometamon.py` の `main()` がエントリポイント。
- Home Timeline を取得し、条件に応じて以下を実行する構成。
  - 挨拶リプ（おはよう / おやすみ）
  - 褒めリプ（キーワードベース）
  - 15時のおやつツイート
  - フォローバック管理
  - 実行件数のDMレポート送信
- Docker運用時は `main/crontab` で **6分ごと** に `python3 /src/hometamon.py` を叩く設計。

## 2. 現在のランタイム/依存の特徴
- READMEの依存記載が古め（Django など現状未使用の記載が残る）。
- 実際のコンテナ依存は `main/Dockerfile` 側がソースオブトゥルースに近い。
  - `python-dotenv==1.0.0`
  - `tweepy==3.8.0`（v1.1 API時代）
  - `pytest==5.4.1`, `pytest-mock==3.1.0`
- ローカル直実行では `dotenv` など未導入環境だとテスト収集時に失敗する。

## 3. CI/CD の状態
- GitHub Actions が2本。
  - `ci.yml`: push時に docker-compose build → コンテナ内pytest
  - `linter.yml`: PR時に black + reviewdog
- 直近履歴でも CI / linter の調整コミットが入っており、保守は継続されていた形跡あり。

## 4. いま見えている技術的リスク
- `main/src/hometamon.py` の `main()` 内で `hometamon.tweet_linestamp()` を呼んでいるが、定義されているのは `test_tweet_linestamp()`。
  - 指定日時に到達すると `AttributeError` になる可能性が高い。
- Twitter APIが古い実装（`tweepy==3.8.0` + v1.1想定）で、現行運用時は権限・API仕様差分を要確認。
- 除外ワードや分類はハードコード中心で、運用ルール変更時にコード修正が必要。
- READMEの手順・依存情報と実態の乖離あり（再起動時のオンボーディング負荷が高い）。

## 5. テスト現状（この調査での実行）
- `pytest -q` は、環境に `python-dotenv` が無いため import error で停止。
- Docker経由テストは、この実行環境に Docker コマンドが無く未実施。

## 6. リリース再開に向けた優先TODO（提案）
1. **クリティカルバグ修正**: `tweet_linestamp` 呼び出し不整合を解消。
2. **Secrets/Env棚卸し**: `.env` 必須値（APIキー、管理者ID等）を再確認。
3. **実行確認**: `--test` 相当の安全モード（投稿しないdry-run）を用意して疎通確認。
4. **README更新**: 実行手順を Docker中心に一本化、依存記載を最新化。
5. **段階リリース**: まず cron 無効 + 手動単発、次に cron 有効化。

## 7. 現状理解サマリ（短く）
- Botの基本機能は保たれているが、**そのまま本番再開はやや危険**。
- 特に `tweet_linestamp` 名称不整合は先に潰すべき。
- 依存と運用手順の再整備をした上で、段階的に復帰するのが安全。
