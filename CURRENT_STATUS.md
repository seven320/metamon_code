# 褒めたもん（metamon_code）現状整理メモ

最終更新: 2026-02-15（Codex更新）

## 1. 目的と実行の流れ
- エントリポイントは `main/src/hometamon.py` の `main()`。
- Home Timeline を読み、条件に応じて以下を実行。
  - 挨拶リプ（おはよう / おやすみ）
  - 褒めリプ（キーワードベース）
  - 15時のおやつツイート
  - フォローバック管理
  - 実行件数のDMレポート送信
- 本番コンテナ（`prd`）では `main/crontab` により 6分ごとに `python3 /src/hometamon.py` を実行する設計。

## 2. ランタイム/依存の現状
- Docker Python は `3.13-alpine`。
- 依存管理は `requirements.txt` から `pyproject.toml` + `uv.lock` へ移行済み。
- `main/Dockerfile` は `uv sync --frozen` で `.venv` を作成し、`/app/.venv/bin` を `PATH` に追加。
- direct dependency（2026-02-15時点）
  - `black>=26.1.0`
  - `pykakasi>=2.3.0`
  - `pytest>=9.0.2`
  - `pytest-mock>=3.15.1`
  - `python-dotenv>=1.2.1`
  - `tqdm>=4.67.3`
  - `tweepy>=4.16.0`

## 3. Docker/開発運用
- `main/Dockerfile` は multi-stage 構成。
  - `dev`: `CMD ["sh"]`
  - `prd`: `crond` 常駐
- `docker-compose.yml` は本番相当定義、`docker-compose.override.yml` で開発用差分（`target: dev`、volume mount、`command: sh`）を上書き。
- `Makefile` は `docker compose` コマンドへ統一済み。`--no-cache` は通常運用から削除済み。

## 4. CI/CD の現状
- ワークフローは2本（どちらも `pull_request` トリガー）。
  - `ci.yml`: Docker Buildx + GitHub Actions cache（`type=gha`）で `dev` イメージをビルドし、`pytest tests` を実行。
  - `linter.yml`: `reviewdog/action-black` で black結果をPRコメントとして指摘（warning、failしない設定）。
- CI高速化として Docker layer cache を導入済み。

## 5. テスト現状（最新確認）
- Docker内で `pytest tests` 実行済み。
- 結果: **62 passed**（警告のみ）。
- `tweepy` 更新に伴い `OAuthHandler` の deprecation warning は出るが、現時点ではテスト成功。

## 6. 残課題/リスク
- `main()` で `hometamon.tweet_linestamp()` を呼んでいる一方、実装は `test_tweet_linestamp()` 名のまま。
  - 条件ヒット時に `AttributeError` となるリスクが継続。
- `OAuthHandler` は非推奨警告が出るため、`OAuth1UserHandler` への移行を検討したい。
- Bot判定ロジック（除外ワード等）はハードコード中心で、運用ルール変更時はコード変更が必要。

## 7. 次にやると良いこと
1. `tweet_linestamp` 呼び出し不整合を修正。
2. Tweepy認証実装を `OAuth1UserHandler` へ移行。
3. `.env` 必須キーのドキュメント化と起動時バリデーション追加。
