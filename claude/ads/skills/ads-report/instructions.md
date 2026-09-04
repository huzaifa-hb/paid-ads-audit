---
name: ads-report
description: "Client-ready paid ads audit report. Builds a validated audit-report.json, then renders a Markdown report and a PDF using scripts/generate_report.py with structural checks before delivery. Use when user says report, PDF, client deliverable, audit report, export the audit, or send this to the client."
user-invokable: false
---

# Ads Report: Client-Ready PDF Audit Report

Turns completed audit results into a Markdown report and a PDF from one validated
`audit-report.json`. Never rebuild structured facts by re-reading prose; the JSON is
the single source.

## Quick Reference

| Command | What it does |
|---------|-------------|
| `/ads report` | Build `audit-report.json` from the current audit, then render Markdown + PDF |
| `/ads report --markdown-only` | Skip the PDF and deliver `ADS-AUDIT-REPORT.md` |

## Process

1. **Confirm analysis is complete.** If no audit has been run in this session, run
   `/ads audit` (or the relevant platform skill) first. Do not write a report from
   assumptions.
2. **Build `audit-report.json`** in the current working directory following
   `references/data-contract.md` exactly. Unknown values are `null`, never zero.
   Every metric carries a status (observed, calculated, estimated, benchmark, missing,
   unsupported) and every finding points at a source entry.
3. **Resolve the skill root.** The script lives at `<skill-root>/scripts/generate_report.py`.
   In Claude Code the skill root is the directory containing this skill's `SKILL.md`
   (typically `~/.claude/skills/ads`). Do not assume the current directory is the skill root.
4. **Validate the input:**
   `python3 <skill-root>/scripts/generate_report.py --input audit-report.json --check-input`
   Fix every reported problem in the JSON and re-run until it passes.
5. **Render:**
   `python3 <skill-root>/scripts/generate_report.py --input audit-report.json --markdown ADS-AUDIT-REPORT.md --output ADS-AUDIT-REPORT.pdf`
6. **Check the PDF structure:**
   `python3 <skill-root>/scripts/generate_report.py --check-pdf ADS-AUDIT-REPORT.pdf`
7. **Inspect every page.** Render pages to images with an available tool (for example
   `pdftoppm` or PyMuPDF) and read each one. Look for clipping, overlap, broken tables,
   blank pages, unreadable text, missing captions, and images that spill past the margins.
   Fix the JSON or the renderer and repeat steps 5 to 7 until clean.
8. **Deliver** the PDF and the Markdown, and summarize the top findings in chat.

## Dependencies

The script needs Python 3 with `reportlab` (PDF) and `pypdf` (PDF checks). Markdown
output has no dependencies. If `reportlab` is missing, offer to install it
(`pip install reportlab pypdf`); if that is not possible, deliver the Markdown report,
say the PDF was not produced, and never claim a PDF exists.

## Required sections

Cover, executive summary, audit scope and data provenance, platform scorecard, key
metrics, findings, prioritized action plan, limitations, methodology and scoring,
evidence appendix. Omit empty optional sections instead of leaving empty headings.

## Layout rules

0.75-inch margins, repeated table headers, wrapped table cells with no clipping, images
and charts bounded within the page, a caption on every visual, page numbers, clear
section hierarchy, restrained colors. Client language is direct. Facts, calculations,
benchmarks, and recommendations are visibly distinguished. Date range, timezone,
currency, attribution setting, account, and retrieval time are preserved from the JSON.

## Output

```
ADS-AUDIT-REPORT.md
ADS-AUDIT-REPORT.pdf
audit-report.json
```
