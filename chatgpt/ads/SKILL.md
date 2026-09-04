---
name: ads
description: "End-to-end paid advertising analysis, auditing, planning, optimization, creative development, testing, and reporting across Google, Meta, YouTube, LinkedIn, TikTok, Microsoft, and Apple Ads. Automatically use for paid-media account reviews, campaign performance questions, budget or bidding work, tracking and attribution checks, competitor research, landing-page reviews, ad copy or image creation, brand extraction, experiment design, and client-ready reports. Prefer connected advertising, commerce, email, and analytics apps or MCP tools for live data; accept exports and screenshots when connections are unavailable."
license: MIT
metadata:
  short-description: "Audit, improve, create, and report on paid ads"
---

# Paid Ads

Run paid-media work end to end while preserving platform facts, source provenance,
and the user's authorization boundaries. The user's request determines the mode;
do not require slash commands.

## Automatic routing

Infer the mode from the request and load only the linked instructions and references.
If several modes are needed, run them as one coherent workflow in dependency order.

| User intent | Load |
|---|---|
| Full account audit, health check, multi-platform review | `skills/ads-audit/instructions.md` |
| Google Ads or Search/PMax/Demand Gen | `skills/ads-google/instructions.md` |
| Meta, Facebook, or Instagram Ads | `skills/ads-meta/instructions.md` |
| YouTube Ads | `skills/ads-youtube/instructions.md` |
| LinkedIn Ads | `skills/ads-linkedin/instructions.md` |
| TikTok Ads | `skills/ads-tiktok/instructions.md` |
| Microsoft/Bing Ads | `skills/ads-microsoft/instructions.md` |
| Apple Ads | `skills/ads-apple/instructions.md` |
| Creative audit or fatigue review | `skills/ads-creative/instructions.md` |
| Landing-page review | `skills/ads-landing/instructions.md` |
| Budget, bidding, scaling, or forecasting | `skills/ads-budget/instructions.md` |
| Paid-media strategy or plan | `skills/ads-plan/instructions.md` |
| Competitor advertising research | `skills/ads-competitor/instructions.md` |
| CPA, ROAS, break-even, LTV:CAC, MER, or PPC math | `skills/ads-math/instructions.md` |
| A/B test or experiment design | `skills/ads-test/instructions.md` |
| Brand identity extraction from a site | `skills/ads-dna/instructions.md` |
| Campaign concepts, briefs, or ad copy | `skills/ads-create/instructions.md` |
| Generate ad images | `skills/ads-generate/instructions.md` |
| Product advertising photos | `skills/ads-photoshoot/instructions.md` |
| Client-ready report or PDF | `skills/ads-report/instructions.md` |

Routing rules:

- “Audit my ads” means the full audit, not only one platform.
- A named platform routes to its platform instructions unless the user explicitly
  asks for a cross-platform comparison.
- Report requests include the necessary analysis before formatting unless valid,
  current audit results are already supplied.
- Creative production routes through brand extraction when a website or brand
  source is available, then campaign creation, then image generation.
- Never make the user learn internal mode names. Continue naturally from context.

## Intake

Extract context already provided and ask only for missing information that materially
changes the work: business type and offer; primary objective and target conversion;
reporting range and comparison period; active platforms and intended accounts; target
CPA, ROAS, revenue, or other success threshold; and approximate spend when unavailable.

For live-account analysis, confirm the intended account when a connection exposes
multiple plausible accounts. Do not guess an account, currency, timezone, attribution
window, or conversion definition.

## Data acquisition

Before asking for exports, inspect the tools available in the current surface and use
the user's connected apps or MCP servers, including connections added after this skill
was written. Read `references/data-sources.md`. Never limit discovery to providers or
tool names mentioned in this package.

Use the advertising platform as the authority for delivery, spend, clicks, platform
conversions, attribution settings, and platform-calculated reach or frequency. Use
Shopify or another commerce source for orders, refunds, and net sales; Klaviyo or
another lifecycle source for owned-channel outcomes. Reconcile sources explicitly;
do not silently replace one source's definition with another.

Data access is read-only unless the user explicitly asks to change campaigns or
external systems. Never broaden a read request into campaign mutations.

## Evidence contract

Every analysis must record source/app and account; exact dates, timezone, and currency;
aggregation and attribution settings; filters and campaign status scope; unavailable
fields; and whether important values are observed, calculated, estimated,
benchmark-based, missing, or unsupported.

Never substitute an adjacent period. Never sum daily reach or average daily frequency
and present the result as an exact platform calculation. Do not merge conversion or
revenue numbers with different definitions without showing the reconciliation.

## Orchestration across ChatGPT and Codex

Read `references/orchestration.md` for a full audit or any task with three or more
independent lanes.

- In Codex, if subagents are available and lanes are independent, run relevant role
  briefs from `references/agent-roles/` in parallel and validate their structured output.
- In ChatGPT or a surface without subagents, run the same lanes inline using the same
  role briefs and evidence ledger.
- Never make subagents a prerequisite. Both paths produce the same result contract,
  scoring rules, caveats, and final checks.
- Do not pin model families or assume provider-specific tool names.

## Analysis principles

- Separate observed facts from interpretation and recommendations.
- Apply benchmarks as directional context, not account truth. State source/date when a
  benchmark affects a recommendation.
- Treat thresholds and platform practices in references as defaults requiring
  calibration to the objective, volume, market, and current platform documentation.
- Do not recommend a pause, budget, bid, or tracking change solely from a heuristic.
- For regulated categories, load `references/compliance.md`, flag uncertainty, and do
  not present the result as legal advice.

## Shared outputs

Use `references/data-contract.md`. A complete result includes an executive summary;
data coverage and provenance; platform scores and findings; cross-platform findings;
prioritized actions with owner, impact, effort, evidence, and verification; limitations;
optional `audit-report.json`; and an optional client PDF through the report workflow.

## Creative generation

Use the native image-generation capability available in the current ChatGPT or Codex
surface. Read the generation or photoshoot instructions. Do not require third-party
image providers, API keys, or provider-specific plugins.

## Completion gate

- Verify every conclusion is supported or clearly labelled.
- Check date ranges, currencies, attribution definitions, formulas, and totals.
- Reconcile contradictions between apps instead of hiding them.
- Verify all requested platforms and outputs are covered.
- Validate structured output against `references/data-contract.md`.
- For PDFs, validate input, generate, render and inspect every page, then run the
  post-generation check in the report instructions.
