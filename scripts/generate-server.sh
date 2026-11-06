#!/usr/bin/env bash
# Regenerate the shared Pydantic v2 data models from openapi.yaml.
#
# Uses datamodel-code-generator (the canonical model generator). The FastAPI
# app in this repo imports these models so request/response bodies stay in sync
# with the OpenAPI contract.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SPEC="$REPO_ROOT/openapi.yaml"
OUT="$REPO_ROOT/src/explore_openapi_with_python/generated/models/models.py"

uv run datamodel-codegen \
  --input "$SPEC" \
  --input-file-type openapi \
  --output "$OUT" \
  --output-model-type pydantic_v2.BaseModel

echo "Server models generated at src/explore_openapi_with_python/generated/models/models.py"
