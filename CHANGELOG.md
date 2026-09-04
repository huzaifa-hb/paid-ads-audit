# Changelog

## 1.0.1 (2026-09-04)

- Claude version: added the missing `ads-report` sub-skill, `scripts/generate_report.py`, and `references/data-contract.md`, so `/ads report` works in Claude Code and Claude.ai.
- Claude version: the report quality gate in SKILL.md now names the script's real flags (`--check-input`, `--markdown`, `--output`, `--check-pdf`).
- Both versions: the example in `data-contract.md` now defines the second source it references, so it passes validation as written.

## 1.0.0 (2026-09-04)

First public release.

- ChatGPT and Codex version (`chatgpt/ads`).
- Claude.ai and Claude Code version (`claude/ads`).
- Coverage: Google, Meta, YouTube, LinkedIn, TikTok, Microsoft, and Apple Ads.
- Modes: audit, per-platform deep dives, creative, landing page, budget and bidding, media plan by industry, competitor research, PPC math, A/B test design, brand extraction, campaign concepts, image generation, product photoshoot, PDF report.
- One-line installer for Claude Code and Codex.
