---
name: ads-audit
description: "Full multi-platform paid advertising audit using connected data sources and portable parallel-or-inline analysis. Covers every active supported platform and produces evidence-backed scores and actions."
---

# Full Multi-Platform Ads Audit

## Process

1. Resolve and query relevant connected sources using `references/data-sources.md`.
2. Confirm exact account, dates, timezone, currency, attribution, and requested objective.
3. Build the evidence ledger and validate that at least one platform has usable data.
4. Detect business type and every active supported platform. Treat YouTube as a distinct
   lane even when its delivery data comes through Google Ads.
5. Follow `references/orchestration.md` using parallel roles in Codex when available or
   identical lanes inline in ChatGPT:
   - `audit-google`: Conversion tracking, waste, structure, keywords, ads, settings (G01-G80)
   - `audit-meta`: Pixel/CAPI health, creative, structure, audience (M01-M50)
   - `audit-creative`: LinkedIn, TikTok, Microsoft creative checks + cross-platform synthesis
   - `audit-tracking`: LinkedIn, TikTok, Microsoft tracking + cross-platform tracking health
   - `audit-budget`: LinkedIn, TikTok, Microsoft budget/bidding + cross-platform allocation
   - `audit-compliance`: All-platform compliance, settings, performance benchmarks
   - Apply the YouTube and Apple instructions when those platforms are active.
6. Validate every lane against `references/data-contract.md`; unknown checks are not failures.
7. Score applicable evaluated checks and show coverage beside every score.
8. Aggregate by verified spend share only when ranges and currencies align.
9. Produce prioritized actions and, when requested, the client-ready report workflow.

## Data Collection

Prefer connected sources. Use exports, screenshots, or pasted data only for missing fields:
- Google Ads: account export, Change History, Search Terms Report
- Meta Ads: Ads Manager export, Events Manager screenshot, EMQ scores
- LinkedIn Ads: Campaign Manager export, Insight Tag status
- TikTok Ads: Ads Manager export, Pixel/Events API status
- Microsoft Ads: account export, UET tag status, import validation results
- Apple Ads: account export, attribution and Custom Product Page performance
- Shopify/Klaviyo/analytics: corroborating commerce and lifecycle facts with definitions

If a source remains unavailable, mark affected checks unknown and disclose coverage.

## Scoring

Read `references/scoring-system.md` for full algorithm.

### Per-Platform Weights

| Platform | Category Weights |
|----------|-----------------|
| Google | Conversion 25%, Waste 20%, Structure 15%, Keywords 15%, Ads 15%, Settings 10% |
| Meta | Pixel/CAPI 30%, Creative 30%, Structure 20%, Audience 20% |
| LinkedIn | Tech 25%, Audience 25%, Creative 20%, Lead Gen 15%, Budget 15% |
| TikTok | Creative 30%, Tech 25%, Bidding 20%, Structure 15%, Performance 10% |
| Microsoft | Tech 25%, Syndication 20%, Structure 20%, Creative 20%, Settings 15% |

### Aggregate Score

```
Aggregate = Sum(Platform_Score x Platform_Budget_Share)
Grade: A (90-100), B (75-89), C (60-74), D (40-59), F (<40)
```

## Output Files

- `ADS-AUDIT-REPORT.md`: Comprehensive multi-platform findings
- `ADS-ACTION-PLAN.md`: Prioritized recommendations (Critical > High > Medium > Low)
- `ADS-QUICK-WINS.md`: Items fixable in <15 minutes with high impact

## Report Structure

### Executive Summary
- Aggregate Ads Health Score (0-100) with grade
- Per-platform scores
- Business type detected
- Active platforms identified
- Top 5 critical issues across all platforms
- Top 5 quick wins across all platforms

### Per-Platform Sections
Each platform section includes:
- Platform Health Score with grade
- Category breakdown with pass/warning/fail per check
- Platform-specific Quick Wins
- Detailed findings with remediation steps

### Cross-Platform Analysis
- Budget allocation assessment (actual vs recommended)
- Tracking consistency (are all platforms tracking the same events?)
- Creative consistency (is messaging aligned across platforms?)
- Attribution overlap (are platforms double-counting conversions?)

### Strategic Recommendations
- Platform prioritization based on business type
- Budget reallocation recommendations
- Scaling opportunities (platforms/campaigns ready to scale)
- Pause-review candidates with evidence and decision conditions

## Priority Definitions

- **Critical**: Revenue/data loss risk (fix immediately)
- **High**: Significant performance drag (fix within 7 days)
- **Medium**: Optimization opportunity (fix within 30 days)
- **Low**: Best practice, minor impact (backlog)

## Quick Wins Criteria

```
IF severity == "Critical" OR severity == "High"
AND estimated_fix_time < 15 minutes
THEN flag as Quick Win
SORT BY (severity_multiplier x estimated_impact) DESC
```
