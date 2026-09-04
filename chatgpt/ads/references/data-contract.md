# Audit data contract

Use this conceptually in chat and literally for `audit-report.json`. Unknown values are
`null`, not zero.

```json
{
  "title": "Paid Advertising Audit",
  "client": "Client or account name",
  "generated_at": "ISO-8601 timestamp",
  "period": {"start": "YYYY-MM-DD", "end": "YYYY-MM-DD", "comparison_start": null, "comparison_end": null},
  "currency": "USD",
  "timezone": "America/New_York",
  "objective": "profitable purchases",
  "executive_summary": "Short evidence-backed summary",
  "sources": [{"provider": "Meta Ads", "account": "Account", "start": "YYYY-MM-DD", "end": "YYYY-MM-DD", "timezone": "America/New_York", "currency": "USD", "grain": "campaign/day", "filters": "active and paused", "attribution": "source-defined", "retrieved_at": "ISO-8601 timestamp", "completeness": "complete", "status": "complete", "notes": []}],
  "platforms": [{"name": "Meta Ads", "score": 72, "grade": "C", "coverage_pct": 80, "spend": 1000, "summary": "...", "metrics": [{"name": "ROAS", "value": 2.1, "unit": "x", "status": "observed", "source_refs": [0]}]}],
  "reconciliations": [{"name": "Paid-attributed purchases vs store orders", "left_label": "Meta attributed purchases", "left_value": 120, "left_source_refs": [0], "right_label": "Shopify orders", "right_value": 105, "right_source_refs": [1], "difference": 15, "difference_pct": 14.29, "definitions": "Platform attribution versus non-cancelled store orders", "interpretation": "Different attribution and order definitions; not an error by itself."}],
  "findings": [{"id": "M-001", "platform": "Meta Ads", "category": "tracking", "severity": "high", "title": "...", "evidence": "...", "impact": "...", "recommendation": "...", "effort": "medium", "owner": "Analytics", "verification": "...", "confidence": "high", "source_refs": [0]}],
  "actions": [{"priority": 1, "action": "...", "owner": "...", "timing": "0-7 days", "impact": "high", "effort": "medium", "success_measure": "...", "finding_ids": ["M-001"]}],
  "limitations": [],
  "methodology": "Observed data, calculations, and benchmark use"
}
```

Validation: timestamps are ISO-8601; dates are ordered; scores are 0-100; grades are A 90-100, B 75-89,
C 60-74, D 40-59, F below 40; coverage is 0-100; finding IDs are unique; action
references resolve; severity is critical/high/medium/low; confidence is high/medium/low;
metric status is observed/calculated/estimated/benchmark/missing/unsupported; and every
metric, finding, and reconciliation side uses in-bounds source references. Each source
includes timezone, currency, grain, filters, attribution, retrieval timestamp, and
completeness. Omit scores when evidence is insufficient. Currency conversion must include
its rate source and timestamp in source notes.
