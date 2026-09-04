#!/usr/bin/env bash
# Zips claude/ads and chatgpt/ads into .skill files under build/.
# The release workflow runs this on every version tag; you can also run it
# locally from the repo root to test an upload before tagging.
set -euo pipefail
cd "$(dirname "$0")/.."
rm -rf build && mkdir -p build
(cd claude  && zip -qr ../build/paid-ads-audit-claude.skill  ads -x '*.DS_Store')
(cd chatgpt && zip -qr ../build/paid-ads-audit-chatgpt.skill ads -x '*.DS_Store')
ls -la build
