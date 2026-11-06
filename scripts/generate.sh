#!/usr/bin/env bash
# Regenerate both the client and the server models from openapi.yaml.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

"$SCRIPT_DIR/generate-client.sh"
"$SCRIPT_DIR/generate-server.sh"
