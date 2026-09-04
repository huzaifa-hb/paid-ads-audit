# Paid Ads Audit

An AI skill that audits your ad accounts the way a senior media buyer would. It runs inside ChatGPT or Claude, scores each platform out of 100, and hands you a prioritized fix list you can act on the same day.

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Latest release](https://img.shields.io/github/v/release/huzaifa-hb/paid-ads-audit?label=release)](https://github.com/huzaifa-hb/paid-ads-audit/releases/latest)
[![Works with ChatGPT](https://img.shields.io/badge/works%20with-ChatGPT-10a37f)](#install-in-chatgpt)
[![Works with Claude](https://img.shields.io/badge/works%20with-Claude-d97757)](#install-in-claude)
[![Platforms](https://img.shields.io/badge/platforms-Google%20%7C%20Meta%20%7C%20YouTube%20%7C%20LinkedIn%20%7C%20TikTok%20%7C%20Microsoft%20%7C%20Apple-555)](#what-it-covers)

## Download

| Where you use AI | Download this | Then |
|---|---|---|
| ChatGPT (Business, Enterprise, Edu) or Codex | [paid-ads-audit-chatgpt.skill](https://github.com/huzaifa-hb/paid-ads-audit/releases/latest/download/paid-ads-audit-chatgpt.skill) | [Install in ChatGPT](#install-in-chatgpt) |
| Claude.ai (web or desktop) or Claude Code | [paid-ads-audit-claude.skill](https://github.com/huzaifa-hb/paid-ads-audit/releases/latest/download/paid-ads-audit-claude.skill) | [Install in Claude](#install-in-claude) |

Both files are plain zip archives. If a file picker refuses the `.skill` extension, rename it to `.zip` and try again.

## What it does

You paste an export, a screenshot, or a few numbers from Ads Manager. The skill asks for the context it needs (business type, spend, goal, platforms), then works through a checklist of over 250 items covering tracking, structure, bidding, budget, creative, landing pages, and compliance. You get:

- A health score per platform, graded A to F, plus a spend-weighted account score.
- Findings ranked Critical, High, Medium, Low, each with the evidence behind it.
- A quick-wins list you can ship this week and a longer action plan with owner, impact, and effort.
- Optional extras: a client-ready PDF report, a media plan by industry, budget forecasts, A/B test design, competitor research, and ad copy or image concepts.

If you connect a live ad platform (through an MCP server or a ChatGPT app), it pulls the data itself. If not, exports and screenshots work fine.

## What it covers

| Platform | Checks | Includes |
|---|---|---|
| Google Ads | 74 | Search terms and wasted spend, Quality Score, PMax asset groups, conversion tracking, Consent Mode V2, bidding fit for conversion volume |
| Meta Ads | 46 | Pixel and CAPI health, EMQ, creative fatigue and diversity, audience overlap, Advantage+ setup, learning phase |
| YouTube | included with Google | Skippable, bumper, Shorts, thumbnails, view-through attribution |
| LinkedIn Ads | 25 | Insight Tag, lead gen forms, audience size, bid type, B2B benchmarks |
| TikTok Ads | 25 | Pixel and Events API, sound-on creative, Smart+, Shop campaigns, budget floors |
| Microsoft Ads | 20 | UET tag, Google import drift, Copilot placements |
| Apple Ads | yes | Search tab, AdAttributionKit, keyword structure |

Cross-platform lanes look at tracking, budget allocation, creative, and compliance together, so a Meta problem that is really a tracking problem shows up as one.

## Install in ChatGPT

Skills in ChatGPT are available on Business, Enterprise, Healthcare, and Edu workspaces. Your admin has to allow skill uploads.

1. Download [paid-ads-audit-chatgpt.skill](https://github.com/huzaifa-hb/paid-ads-audit/releases/latest/download/paid-ads-audit-chatgpt.skill).
2. In ChatGPT open Skills (under Plugins or Customize depending on your workspace), choose Create, then Upload from your computer.
3. Pick the file, review the instructions ChatGPT shows you, and click Install.
4. Start a chat and type `@Paid Ads` or just describe the job. The skill also triggers on its own when you ask about ad performance.

Using Codex instead? Run this in a terminal:

```bash
curl -fsSL https://raw.githubusercontent.com/huzaifa-hb/paid-ads-audit/main/install.sh | bash -s -- codex
```

Then call it with `$ads` in Codex.

## Install in Claude

Skills work on Claude Free, Pro, Max, Team, and Enterprise.

1. Download [paid-ads-audit-claude.skill](https://github.com/huzaifa-hb/paid-ads-audit/releases/latest/download/paid-ads-audit-claude.skill).
2. In Claude go to Settings, then Customize, then Skills, and click Add (or the + button).
3. Select the file. The skill appears in your list with a toggle. Leave it on.
4. Start a chat and ask for an audit. Claude picks the skill up automatically.

Using Claude Code instead? Run this in a terminal:

```bash
curl -fsSL https://raw.githubusercontent.com/huzaifa-hb/paid-ads-audit/main/install.sh | bash -s -- claude
```

This installs the skill to `~/.claude/skills/ads` and the six audit subagents to `~/.claude/agents`, so a full audit runs the platform checks in parallel. Then type `/ads audit` inside Claude Code.

Prefer to do it by hand? Copy the `claude/ads` folder into `~/.claude/skills/` and the files in `claude/ads/agents/` into `~/.claude/agents/`.

## How to run an audit

Give the skill something to look at and tell it what you care about. Example:

```
Audit my Meta and Google accounts. DTC skincare, $18k/month split 70/30,
goal is purchases at a 3.0 ROAS. Last 30 days vs the 30 before.
```

Then attach or paste:

- Google Ads: campaign export (CSV), Search Terms report, and a screenshot of Conversions settings.
- Meta: Ads Manager export at ad level with Reach and Frequency columns, and an Events Manager screenshot showing EMQ.
- LinkedIn, TikTok, Microsoft, Apple: the campaign export from each manager plus a screenshot of the pixel or tag status.

The full list of what helps, by platform, is in [docs/data-checklist.md](docs/data-checklist.md). Example prompts for every mode (budget, plan, creative, report, math) are in [docs/prompts.md](docs/prompts.md).

Claude Code users can also call modes directly: `/ads google`, `/ads meta`, `/ads budget`, `/ads plan ecommerce`, `/ads report`, and so on. In ChatGPT and Claude.ai you just say what you want.

## Your data

The skill is a set of instructions. It contains no tracking, sends nothing anywhere, and only sees what you paste, upload, or connect. Live connections are read-only during audits. It never edits a campaign unless you ask it to in plain words.

Benchmarks in the skill are directional. Your account is the source of truth, and the skill is written to say so rather than pretend a benchmark is your target.

## Repository layout

```
chatgpt/ads/     Source for the ChatGPT and Codex version
claude/ads/      Source for the Claude.ai and Claude Code version
install.sh       One-line installer for Claude Code and Codex
scripts/         package.sh zips the two folders into .skill files
.github/         Workflow that builds the .skill files and attaches them to each release
docs/            Data checklist and example prompts
```

The `.skill` downloads live on the [Releases page](https://github.com/huzaifa-hb/paid-ads-audit/releases). They are built from the source folders by the release workflow, so the source and the download never drift apart.

The two versions share the same checklists, benchmarks, and scoring. They differ in how they talk to each platform's tooling, which is why there are two files instead of one.

## Feedback

Found a check that misfires or a benchmark that is out of date? Open an [issue](https://github.com/huzaifa-hb/paid-ads-audit/issues) with the platform and what you expected. Pull requests are welcome; change both `claude/ads` and `chatgpt/ads` when the fix applies to both.

## License

MIT. See [LICENSE](LICENSE).
