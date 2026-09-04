# Client-ready paid ads report

Create a readable Markdown report and, when requested, a polished PDF from the same
validated `audit-report.json`. Never reconstruct structured facts by scraping prose.

## Workflow

1. Complete any missing analysis and normalize it using `references/data-contract.md`.
2. Resolve the skill root in the current runtime; do not assume the current working
   directory is the skill directory. Validate input with the script at that resolved path:
   `python3 <skill-root>/scripts/generate_report.py --input audit-report.json --check-input`
3. Generate Markdown and PDF:
   `python3 <skill-root>/scripts/generate_report.py --input audit-report.json --markdown ADS-AUDIT-REPORT.md --output ADS-AUDIT-REPORT.pdf`
4. Run structural PDF checks:
   `python3 <skill-root>/scripts/generate_report.py --check-pdf ADS-AUDIT-REPORT.pdf`
5. Render every page to images using an available PDF renderer. Inspect every rendered
   page for clipping, overlap, broken tables, blank pages, unreadable text, missing
   captions, and unsafe image scaling. Fix the input or renderer and repeat until clean.

The script requires Python 3 with ReportLab and pypdf. Prefer the runtime's bundled
document dependencies. If they are unavailable, use a native document/PDF artifact
capability, but
preserve the same schema, sections, and checks. If neither path can make a PDF, deliver
the Markdown report and state the limitation; never claim a PDF exists.

## Required sections

Cover, executive summary, audit scope and provenance, scorecard, key metrics, findings,
prioritized action plan, limitations, methodology/scoring, and evidence appendix. Omit
empty optional sections instead of leaving empty headings.

Use 0.75-inch margins, repeated table headers, wrapped cells, bounded images and charts,
captions, section hierarchy, page numbers, and restrained accessible colors. Keep client
language direct, distinguish facts/calculations/benchmarks/recommendations, and preserve
date range, timezone, currency, attribution, account, and retrieval details.
