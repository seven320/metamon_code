#!/usr/bin/env bash
# Generate Python gRPC stubs from the vendored mixi2-api protos.
# Output is committed under src/mixi2_gen/ so runtime needs only grpcio+protobuf
# (not grpcio-tools). Re-run after bumping the vendored proto version.
#
# Usage:  cd main && uv run bash scripts/gen_proto.sh
set -euo pipefail
cd "$(dirname "$0")/.."

OUT=src/mixi2_gen
rm -rf "$OUT"
mkdir -p "$OUT"

python -m grpc_tools.protoc \
  -Iproto \
  --python_out="$OUT" \
  --grpc_python_out="$OUT" \
  proto/social/mixi/application/const/v1/*.proto \
  proto/social/mixi/application/model/v1/*.proto \
  proto/social/mixi/application/service/application_api/v1/service.proto

# Mark the generated tree as a namespace-safe package root.
touch "$OUT/__init__.py"
echo "Generated stubs into $OUT"
