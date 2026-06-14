#!/usr/bin/env bash
# 褒めたもん mixi2版 — Cloud Run デプロイ（褒め/歓迎の2ジョブをビルド＆更新）
#
# 「1回実行して終了」型の bot を Cloud Run Jobs にし、Cloud Scheduler で定期起動する。
# このスクリプトは「イメージのビルド＆push → 2ジョブを create-or-update」までを冪等に行う。
# 初回 push でも更新でも同じコマンドで動く（GitHub Actions の自動デプロイからも呼ぶ）。
#
# 前提（初回のみ別途・手元の CLOUD_RUN.md 参照）:
#   - gcloud 認証済み（ローカルは `gcloud auth login`／CIは Workload Identity 連携）
#   - API 有効化: run / artifactregistry / cloudbuild / cloudscheduler / secretmanager / firestore
#   - Artifact Registry リポジトリ作成済み（既定名 hometamon）
#   - Secret Manager に mixi2-client-id / mixi2-client-secret を登録済み
#   - Firestore(Native) 作成済み＋ジョブ実行SAに roles/datastore.user
#   - Cloud Scheduler トリガー作成済み（praise=*/15 * * * *, welcome=0 * * * *）
#
# 使い方（値は環境変数で渡す。CI も同じ変数を渡す）:
#   PROJECT_ID=xxx API_ADDRESS=xxx TOKEN_URL=xxx COMMUNITY_ID=xxx \
#     [MIXI2_DRY_RUN=0] ./scripts/deploy.sh
set -euo pipefail

# ---- 設定（環境変数で上書き）----------------------------------------------
PROJECT_ID="${PROJECT_ID:?PROJECT_ID を設定してください}"
REGION="${REGION:-asia-northeast1}"
REPO="${REPO:-hometamon}"
IMAGE="${IMAGE:-${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO}/bot:latest}"

# 接続・識別子（非秘密）。CLIENT_ID/SECRET は Secret Manager 参照なのでここには無い。
API_ADDRESS="${API_ADDRESS:?API_ADDRESS を設定してください}"
TOKEN_URL="${TOKEN_URL:?TOKEN_URL を設定してください}"
COMMUNITY_ID="${COMMUNITY_ID:?COMMUNITY_ID を設定してください}"
PRAISE_STAMP_ID="${PRAISE_STAMP_ID:-o_hearts}"
ADMIN_USER_ID="${ADMIN_USER_ID:-}"
BOT_USER_ID="${BOT_USER_ID:-}"
# 状態は Firestore（ADC）。プロジェクト未指定なら PROJECT_ID を使う。
GOOGLE_CLOUD_PROJECT="${GOOGLE_CLOUD_PROJECT:-$PROJECT_ID}"
# 初回は 1（書き込みせず疎通）。本番化したら 0 を渡す。
MIXI2_DRY_RUN="${MIXI2_DRY_RUN:-1}"

# 空の識別子は env から除外（空文字を焼かない）
ENV_PAIRS="API_ADDRESS=${API_ADDRESS},TOKEN_URL=${TOKEN_URL},COMMUNITY_ID=${COMMUNITY_ID}"
ENV_PAIRS="${ENV_PAIRS},PRAISE_STAMP_ID=${PRAISE_STAMP_ID}"
ENV_PAIRS="${ENV_PAIRS},GOOGLE_CLOUD_PROJECT=${GOOGLE_CLOUD_PROJECT},MIXI2_DRY_RUN=${MIXI2_DRY_RUN}"
[ -n "$ADMIN_USER_ID" ] && ENV_PAIRS="${ENV_PAIRS},ADMIN_USER_ID=${ADMIN_USER_ID}"
[ -n "$BOT_USER_ID" ] && ENV_PAIRS="${ENV_PAIRS},BOT_USER_ID=${BOT_USER_ID}"

SECRETS="CLIENT_ID=mixi2-client-id:latest,CLIENT_SECRET=mixi2-client-secret:latest"

# ---- ビルド＆push（Cloud Build：ローカルDocker不要）------------------------
echo "==> build & push: ${IMAGE}"
gcloud builds submit main --tag "${IMAGE}" --project "${PROJECT_ID}"

# ---- ジョブを create-or-update --------------------------------------------
deploy_job() {
  local name="$1" module="$2" action=create
  if gcloud run jobs describe "${name}" --region "${REGION}" --project "${PROJECT_ID}" >/dev/null 2>&1; then
    action=update
  fi
  echo "==> ${action} job: ${name} (-m ${module})"
  gcloud run jobs "${action}" "${name}" \
    --image "${IMAGE}" --region "${REGION}" --project "${PROJECT_ID}" \
    --command python --args="-m,${module}" \
    --task-timeout 300 --max-retries 1 \
    --set-env-vars "${ENV_PAIRS}" \
    --set-secrets "${SECRETS}"
}

deploy_job hometamon-praise  src.hometamon_mixi2
deploy_job hometamon-welcome src.welcome_newcomer

echo "==> done. (cron は Cloud Scheduler トリガーで起動。MIXI2_DRY_RUN=${MIXI2_DRY_RUN})"
