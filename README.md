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

## Why this exists

Ask a general chatbot to "look at my ads" and you get generic advice: refresh creative, add negatives, check your pixel. This skill replaces that with the actual working method of a senior media buyer, written down as a set of instructions the AI has to follow. It knows that Smart Bidding needs conversion volume before it is safe, that a Meta ad set with less than 5x CPA in daily budget will never leave learning, that a TikTok ad without sound is a wasted impression, and that a ROAS number means nothing until you know the attribution window behind it. It checks for those things, in order, and shows you the evidence.

Everything the skill knows lives in plain text files you can read: over 30 reference documents covering audit checklists, platform benchmarks, bidding decision trees, tracking stacks, ad policies, creative specs, and copy frameworks. Nothing is hidden in a model's weights.

## What a full audit gives you

1. It asks for the context that changes the answer: business type, monthly spend by platform, the goal, and your target CPA or ROAS. If you already gave it, it does not ask again.
2. It reads whatever you give it: platform exports, screenshots, pasted numbers, or a live connection to the ad platform.
3. It works through the platform checklists. Each check is graded pass, warning, fail, or not applicable, with a severity of Critical, High, Medium, or Low.
4. It scores each platform 0 to 100 using a weighted formula: severity multipliers (Critical counts 5.0, High 3.0, Medium 1.5, Low 0.5) across category weights that differ per platform. On Google, conversion tracking is 25% of the score and wasted spend is 20%. On Meta, pixel and CAPI health is 30% and creative diversity and fatigue is another 30%. Checks that do not apply are excluded so a small account is not penalized for features it does not need.
5. It rolls the platform scores into one account score weighted by spend share, graded A to F.
6. It hands you three things: a quick-wins list for this week, a prioritized action plan where each item has an owner, expected impact, effort, the evidence behind it, and how to verify the fix worked, and a plain list of what it could not check and why.

In Claude Code the platform audits run in parallel as six separate agents (Google, Meta, creative, tracking, budget, compliance) and the results are validated before they are combined. In ChatGPT, Claude.ai, and Codex the same lanes run in sequence with the same output.

## Platform coverage

| Platform | Checks | What gets examined |
|---|---|---|
| Google Ads | 80 | Enhanced Conversions, Consent Mode V2, conversion action hygiene, search terms and negative lists, brand and non-brand separation, Quality Score as a diagnostic, RSA strength, PMax asset groups and search categories, AI Max, Demand Gen, CTV tracking, location and network settings, bidding fit for conversion volume |
| Meta Ads | 50 | Pixel and CAPI setup, Event Match Quality per event, deduplication, creative fatigue signals and refresh cadence, Andromeda creative similarity, Advantage+ Sales and Advantage+ Audience, learning phase status, CBO versus ABO, audience overlap and exclusions, Special Ad Categories |
| YouTube | dedicated module | Skippable, non-skippable, bumper, Shorts, Demand Gen, and Connected TV, the VAC to Demand Gen migration, view-through attribution, thumbnail and hook quality |
| LinkedIn Ads | 27 | Insight Tag and CAPI, audience size and precision, Thought Leader Ads, ABM and predictive audiences, lead gen form completion, manual versus automated bidding, CRM revenue attribution, EU messaging compliance |
| TikTok Ads | 28 | Pixel and Events API Gateway, ttclid passback, sound and caption presence, safe zones, Spark Ads, Smart+ modular control, Search toggle, TikTok Shop, 50 conversions a week learning threshold |
| Microsoft Ads | 24 | UET tag, Google import validation and sync drift, LinkedIn profile targeting, Copilot placements and Copilot Checkout, cost advantage versus Google |
| Apple Ads | dedicated module | Campaign structure, Custom Product Pages, MMP attribution, AdAttributionKit, Today, Search, and Product Page tab coverage, Maximize Conversions, CPA benchmarks by country |

Cross-platform checks sit on top of these. Tracking health, budget allocation, creative, and compliance are each assessed across every active platform together, so a Meta problem that is really a tracking problem gets reported once, as a tracking problem.

## Beyond the audit

The audit is one of 17 modes. Each is a separate instruction set the skill loads on demand.

**Money**

- Budget and bidding review applies the 70/20/10 allocation rule, the 3x kill rule, the 20% scaling rule, and per-platform bidding decision trees. It tells you what to kill, what to scale, and whether the account is ready to scale at all.
- PPC math covers CPA, ROAS, CPL, break-even, impression share opportunity sizing, budget forecasting, LTV to CAC, and MER. It needs no data connection, just pasted numbers.
- A/B test design gives you a structured hypothesis, a significance calculator, sample size and duration estimates, and setup instructions for Meta Experiments, Google Experiments, LinkedIn A/B, and TikTok split tests.

**Strategy**

- Media planning produces platform selection, campaign architecture, budget phasing, creative strategy, a tracking setup plan, and a phased roadmap. It ships with 12 industry templates: ecommerce, ecommerce creative, SaaS, B2B enterprise, local service, info products, mobile app, real estate, healthcare, finance, agency, and a generic fallback.
- Competitor research works from ad libraries and auction insights to analyze competitor copy, creative strategy, messaging themes, keyword targeting, and estimated spend, then maps platform, messaging, audience, and creative gaps. It includes response playbooks for when a competitor bids on your brand and when you are outspent.

**Post-click**

- Landing page review scores message match, page speed against ad-traffic thresholds, mobile experience, trust signals, form length, consent banner impact, and UTM handling, with a health score and a quick-wins list.

**Creative**

- Creative audit assesses copy, video, image, and format diversity per platform, detects fatigue from frequency and CTR decay, and applies the Andromeda similarity score for Meta and Symphony awareness for TikTok.
- Brand DNA extraction reads a website and writes a brand profile: colors, typography, tone of voice, imagery style, with confidence scores.
- Campaign creation turns that profile plus audit results into campaign concepts, messaging pillars, and copy briefs, using six frameworks: AIDA, PAS, BAB, 4P, FAB, and Star-Story-Solution.
- Image generation and product photoshoot produce platform-sized assets and five product photography styles (studio, floating, ingredient, in use, lifestyle) with safe-zone specs for Feed, Reels, Stories, Shorts, and TikTok.

**Reporting**

- Client report packages the audit as a PDF with an executive summary, scorecard, findings, action plan, limitations, and methodology, and runs a layout check before it hands it over.

## Rules the skill will not break

These are hard-coded gates, not suggestions. They exist because each one is a mistake that costs real money.

- Never recommend Broad Match on Google without Smart Bidding in place.
- Never recommend edits to a campaign that is still in the learning phase.
- Flag any ad group or campaign with a CPA above 3x target for a pause decision.
- Meta ad sets need at least 5x CPA in daily budget, TikTok ad groups at least 50x, before performance is judged.
- Flag Meta accounts running fewer than 10 genuinely distinct creatives.
- Verify the tracking stack (Consent Mode V2, CAPI, Events API, AdAttributionKit) before making any optimization recommendation.
- Always check Special Ad Category status for housing, employment, credit, and finance advertisers.
- Never substitute an adjacent date range, never sum daily reach and call it reach, never merge conversion numbers with different definitions without showing the reconciliation.

Every number in the output is labelled as observed, calculated, estimated, benchmark-based, or missing. Benchmarks come from named 2025 and 2026 sources (WordStream and LocaliQ, Triple Whale, SplitMetrics) and are treated as direction, never as your target.

## Built for DTC and ecommerce accounts

A dedicated playbook covers the situations ecommerce buyers hit most: deriving break-even ROAS from real unit economics, a staged ROAS progression model for new accounts, learning phase budget math, isolating new-customer ROAS from blended, reading MER trend against platform ROAS trend, telling creative fatigue apart from audience saturation, a seven-step triage for sudden performance drops, Amazon and DTC cross-channel decisions including Brand Referral Bonus and price parity, and a three-numbers attribution framework you can explain to a CEO.

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
