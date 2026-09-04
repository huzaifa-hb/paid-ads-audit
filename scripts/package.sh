#!/usr/bin/env bash
# Rebuilds the two .skill files in dist/ from the source folders.
# Run from the repo root: ./scripts/package.sh
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p dist
rm -f dist/paid-ads-audit-claude.skill dist/paid-ads-audit-chatgpt.skill
(cd claude  && zip -qr ../dist/paid-ads-audit-claude.skill  ads -x '*.DS_Store')
(cd chatgpt && zip -qr ../dist/paid-ads-audit-chatgpt.skill ads -x '*.DS_Store')
ls -la dist
