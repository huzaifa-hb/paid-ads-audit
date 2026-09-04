# Portable orchestration

Use this for full audits and tasks with three or more independent lanes. The coordinator
owns intake, source discovery, evidence, aggregation, files, and quality control.

Select only applicable briefs from `references/agent-roles/`: audit-google, audit-meta,
audit-creative, audit-tracking, audit-budget, audit-compliance, creative-strategist,
copy-writer, visual-designer, and format-adapter.

## Codex path

When subagent collaboration exists and lanes are independent, delegate them in parallel.
Pass the relevant role brief as guidance. Fetch and normalize shared connected data first
because delegated agents may not inherit every connection. Agents return structured
results; only the coordinator aggregates or writes shared files. Do not rely on model
names, turn limits, or provider-specific tools. If a lane fails, retry inline or mark it
incomplete; never fabricate a score.

## ChatGPT and no-subagent path

Run the same briefs inline: platform delivery/settings; tracking/attribution;
creative/landing page; budget/bidding; compliance; synthesis. Maintain one evidence
ledger and findings array. Do not expose internal handoffs or ask the user to invoke
each lane.

## Lane response contract

```json
{
  "lane": "audit-meta",
  "status": "complete|partial|unavailable",
  "sources": [],
  "coverage": {"applicable": 0, "evaluated": 0, "unknown": 0, "not_applicable": 0},
  "score": null,
  "findings": [],
  "limitations": []
}
```

Unknown and not-applicable checks are excluded from the scoring denominator. Report
coverage beside every score. Weight platform scores by verified spend share only when
all included platforms share the same date range and currency. Otherwise present them
separately and mark the aggregate unavailable. Do not double-count cross-platform lanes.
