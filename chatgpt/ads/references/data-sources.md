# Connected data sources

Use available connected apps or MCP tools before requesting manual exports. This skill
must adapt to connections installed in the future, including providers and tool names
that do not appear anywhere in this package. Treat the runtime's current tool catalog,
descriptions, input schemas, and read-only probe results as authoritative for capability
discovery.

Do not maintain a closed allowlist of MCP names. The examples below describe source
roles, not the only supported products.

## Adaptive discovery for unfamiliar MCPs

At the start of each data-backed request:

1. Inspect or search the current runtime's callable apps, MCP tools, and resources using
   whatever discovery mechanism the surface exposes.
2. Read candidate tool descriptions and input schemas. Classify each candidate by the
   facts it can supply: advertising delivery, commerce, analytics, CRM, lifecycle/email,
   call tracking, attribution, creative library, finance, or another relevant role.
3. Prefer semantic capability matches over names. A newly connected warehouse, BI tool,
   or agency reporting MCP may be the best source even if its name does not mention ads.
4. Distinguish read operations from mutations using the exposed schema and description.
   During audits, call only clearly read-only discovery/query operations.
5. Make the smallest safe probe needed to confirm access, scope, returned fields,
   pagination, and account identity. A configured or visible MCP is not proven usable
   until a read succeeds.
6. Build a temporary source adapter from returned fields into the normalization contract
   below. Do not require the MCP to use familiar field or entity names.
7. If descriptions are vague, schemas are ambiguous, or a call could write externally,
   do not guess. Use a safer read-only candidate, request an export, or ask one focused
   question about the connection.
8. If tools have changed since an app was connected and calls fail with a schema mismatch,
   report that the app/tool metadata may need refreshing; do not repeatedly retry an
   incompatible call or claim the underlying data is absent.

Do not load or query every connection indiscriminately. Select candidates relevant to
the user's requested platforms, business model, and questions.

## Source selection

| Need | Preferred authority | Useful corroboration |
|---|---|---|
| Delivery, spend, impressions, clicks, campaign settings | Native ad-platform connection | Analytics or commerce source |
| Platform-attributed conversions, reach, frequency | Native ad-platform connection | Analytics source, clearly distinguished |
| Orders, refunds, discounts, net sales | Shopify or connected commerce system | Payment processor or warehouse |
| Email/SMS flows and attributed lifecycle revenue | Klaviyo or connected lifecycle system | Commerce system |
| Sessions, events, landing-page behavior | Connected analytics source | Ad platform and commerce system |
| Competitor creative | Official ad libraries or connected research source | Public web sources |

Supported advertising lanes include Google Ads, Meta Ads, YouTube through Google Ads,
LinkedIn Ads, TikTok Ads, Microsoft Ads, and Apple Ads. Commerce, CRM, analytics, and
lifecycle connections are supporting sources rather than substitutes for platform facts.

## Discovery sequence

1. Inspect currently available apps, MCP tools, or data sources, including unfamiliar
   and newly installed connections.
2. Match tools to the requested provider and read their descriptions or schemas.
3. List or search accessible accounts only when necessary to identify the target.
4. Ask the user to choose if more than one account is plausible.
5. Query the exact requested range and comparison period with explicit status filters.
6. Paginate until complete. Record truncation, sampling, unavailable fields, and errors.
7. Fetch currency, timezone, attribution, conversion definitions, and optimization goal.
8. Use exports, screenshots, or pasted data only for gaps connected sources cannot fill.

Do not claim a connector is unavailable until the current tool inventory has been
checked and a safe read has been attempted where possible. Do not install, reconnect,
reauthorize, refresh, or modify a connector without direction.
Never request or expose secrets, tokens, customer PII, or audience-member data.

## Minimum datasets

For each platform obtain, when available: account/timezone/currency; performance by day
and entity; spend, impressions, reach, frequency, clicks and cost metrics; conversions,
value, CPA and ROAS; status, objective, budget, bidding and attribution settings;
creative delivery/performance; search terms for search ads; tracking diagnostics; and
change history when explaining shifts.

For commerce, obtain gross sales, discounts, refunds, net sales, orders, and customer
type when available. For lifecycle marketing, obtain campaign/flow delivery, attributed
revenue, and the source's attribution definition.

## Evidence ledger and reconciliation

Record one row per query:

`source | account | date range | timezone | currency | grain | filters | attribution | retrieved_at | completeness`

When values disagree, preserve both definitions, quantify the difference, identify
likely causes, and select an authority only for a clearly stated business question.
Never relabel commerce attribution as platform-attributed ROAS. Align dates and
timezones before joins, preserve native IDs, disclose currency conversion, and keep
refunds and cancellations explicit.

All external writes remain out of scope unless explicitly requested.

## Runtime normalization contract

Adapt unfamiliar source fields into this conceptual shape while retaining the original
field names in notes:

```json
{
  "source": "runtime connection name",
  "source_role": "advertising|commerce|analytics|crm|lifecycle|other",
  "account": {"native_id": "...", "name": "..."},
  "period": {"start": "YYYY-MM-DD", "end": "YYYY-MM-DD", "timezone": "..."},
  "currency": "...",
  "grain": "day|campaign|ad_set|ad|order|event|other",
  "dimensions": {},
  "metrics": {},
  "attribution": {},
  "pagination": {"complete": true, "notes": []},
  "retrieved_at": "ISO-8601 timestamp",
  "raw_field_map": {"normalized_field": "original MCP field"},
  "limitations": []
}
```

Normalize only defensible mappings. Preserve unknown fields for interpretation rather
than forcing them into a nearby metric. If a new source provides a better primary fact
than the examples in this file, use it and explain why; retain the native ad platform as
authority for platform-calculated delivery and attribution metrics when available.

The skill intentionally declares no fixed MCP dependencies in `agents/openai.yaml`.
Fixed dependency declarations would prevent it from adapting cleanly to the user's
current and future connection set.
