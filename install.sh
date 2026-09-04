#!/usr/bin/env bash
# Installs the Paid Ads Audit skill for Claude Code or Codex.
#
#   curl -fsSL https://raw.githubusercontent.com/huzaifa-hb/paid-ads-audit/main/install.sh | bash -s -- claude
#   curl -fsSL https://raw.githubusercontent.com/huzaifa-hb/paid-ads-audit/main/install.sh | bash -s -- codex
#
# Options:
#   claude          Install to ~/.claude/skills/ads and ~/.claude/agents
#   codex           Install to ~/.codex/skills/ads
#   --project       Install into the current folder instead of your home directory
#   --no-agents     (claude only) Skip copying the audit subagents

set -euo pipefail

REPO="huzaifa-hb/paid-ads-audit"
TARGET=""
SCOPE="global"
WITH_AGENTS=1

for arg in "$@"; do
  case "$arg" in
    claude|codex) TARGET="$arg" ;;
    --project) SCOPE="project" ;;
    --no-agents) WITH_AGENTS=0 ;;
    -h|--help) sed -n '2,13p' "$0"; exit 0 ;;
    *) echo "Unknown option: $arg" >&2; exit 1 ;;
  esac
done

if [ -z "$TARGET" ]; then
  echo "Usage: install.sh <claude|codex> [--project] [--no-agents]" >&2
  exit 1
fi

if [ "$TARGET" = "claude" ]; then
  SRC_DIR="claude/ads"
  if [ "$SCOPE" = "global" ]; then
    SKILL_DEST="$HOME/.claude/skills/ads"
    AGENT_DEST="$HOME/.claude/agents"
  else
    SKILL_DEST="$PWD/.claude/skills/ads"
    AGENT_DEST="$PWD/.claude/agents"
  fi
else
  SRC_DIR="chatgpt/ads"
  if [ "$SCOPE" = "global" ]; then
    SKILL_DEST="$HOME/.codex/skills/ads"
  else
    SKILL_DEST="$PWD/.agents/skills/ads"
  fi
fi

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

echo "Downloading $REPO ..."
curl -fsSL "https://github.com/$REPO/archive/refs/heads/main.tar.gz" | tar -xz -C "$TMP"
SRC="$TMP/paid-ads-audit-main/$SRC_DIR"

if [ ! -f "$SRC/SKILL.md" ]; then
  echo "Download looks incomplete (no SKILL.md found). Try again." >&2
  exit 1
fi

if [ -d "$SKILL_DEST" ]; then
  echo "Replacing existing install at $SKILL_DEST"
  rm -rf "$SKILL_DEST"
fi
mkdir -p "$(dirname "$SKILL_DEST")"
cp -R "$SRC" "$SKILL_DEST"
echo "Skill installed to $SKILL_DEST"

if [ "$TARGET" = "claude" ] && [ "$WITH_AGENTS" = "1" ]; then
  mkdir -p "$AGENT_DEST"
  cp "$SRC/agents/"*.md "$AGENT_DEST/"
  echo "Audit subagents installed to $AGENT_DEST"
fi

echo
if [ "$TARGET" = "claude" ]; then
  echo "Done. Open Claude Code and type: /ads audit"
else
  echo "Done. Open Codex and type: \$ads audit my accounts"
  echo "Restart Codex if the skill does not show up right away."
fi
