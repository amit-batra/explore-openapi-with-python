#!/usr/bin/env bash
# Regenerate the typed OpenAPI client from openapi.yaml into the package.
#
# Uses openapi-python-client (the canonical, actively maintained generator from
# the openapi-generators org). Output is a self-contained package that imports
# httpx + attrs at runtime.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SPEC="$REPO_ROOT/openapi.yaml"
OUT="$REPO_ROOT/src/generated/client"

uv run openapi-python-client generate \
  --path "$SPEC" \
  --output-path "$OUT" \
  --meta none

rm -rf "$OUT/.ruff_cache"
echo "Client generated at src/generated/client"
