#!/usr/bin/env python3
"""Validate paid-ads audit JSON and render matching Markdown/PDF reports."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime
from pathlib import Path


REQUIRED_SECTIONS = (
    "Executive Summary",
    "Scope and Data Provenance",
    "Platform Scorecard",
    "Findings",
    "Prioritized Action Plan",
    "Limitations",
    "Methodology",
)
SEVERITIES = {"critical", "high", "medium", "low"}
CONFIDENCE = {"high", "medium", "low"}
METRIC_STATUS = {"observed", "calculated", "estimated", "benchmark", "missing", "unsupported"}


def fail(message: str) -> None:
    raise ValueError(message)


def load_json(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"Cannot read valid JSON from {path}: {exc}")
    if not isinstance(data, dict):
        fail("Top-level audit report must be a JSON object")
    return data


def parse_date(value: object, label: str) -> date:
    if not isinstance(value, str):
        fail(f"{label} must be an ISO date string")
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        fail(f"{label} must use YYYY-MM-DD: {exc}")


def valid_timestamp(value: object) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
        return True
    except ValueError:
        return False


def expected_grade(score: float) -> str:
    if score >= 90:
        return "A"
    if score >= 75:
        return "B"
    if score >= 60:
        return "C"
    if score >= 40:
        return "D"
    return "F"


def validate(data: dict) -> list[str]:
    errors: list[str] = []

    def check(condition: bool, message: str) -> None:
        if not condition:
            errors.append(message)

    for key in ("title", "client", "generated_at", "period", "currency", "timezone", "objective", "executive_summary", "sources", "platforms", "reconciliations", "findings", "actions", "limitations", "methodology"):
        check(key in data, f"missing required field: {key}")

    check(valid_timestamp(data.get("generated_at")), "generated_at must be an ISO-8601 timestamp")
    for key in ("title", "client", "currency", "timezone", "objective", "methodology"):
        check(bool(str(data.get(key, "")).strip()), f"{key} is empty")

    period = data.get("period", {})
    if isinstance(period, dict) and period.get("start") and period.get("end"):
        try:
            check(parse_date(period["start"], "period.start") <= parse_date(period["end"], "period.end"), "period.start is after period.end")
        except ValueError as exc:
            errors.append(str(exc))
    else:
        errors.append("period.start and period.end are required")

    check(bool(str(data.get("executive_summary", "")).strip()), "executive_summary is empty")
    check(isinstance(data.get("sources"), list) and len(data.get("sources", [])) > 0, "at least one source is required")
    check(isinstance(data.get("platforms"), list) and len(data.get("platforms", [])) > 0, "at least one platform is required")
    check(isinstance(data.get("reconciliations"), list), "reconciliations must be an array")
    check(isinstance(data.get("findings"), list), "findings must be an array")
    check(isinstance(data.get("actions"), list), "actions must be an array")
    check(isinstance(data.get("limitations"), list), "limitations must be an array")

    for index, source in enumerate(data.get("sources", [])):
        check(isinstance(source, dict), f"sources[{index}] must be an object")
        if not isinstance(source, dict):
            continue
        for key in ("provider", "account", "start", "end", "timezone", "currency", "grain", "filters", "attribution", "retrieved_at", "completeness", "status"):
            check(bool(source.get(key)), f"sources[{index}].{key} is required")
        check(valid_timestamp(source.get("retrieved_at")), f"sources[{index}].retrieved_at must be an ISO-8601 timestamp")

    for index, platform in enumerate(data.get("platforms", [])):
        check(isinstance(platform, dict), f"platforms[{index}] must be an object")
        if not isinstance(platform, dict):
            continue
        check(bool(platform.get("name")), f"platforms[{index}].name is required")
        score = platform.get("score")
        if score is not None:
            check(isinstance(score, (int, float)) and 0 <= score <= 100, f"platforms[{index}].score must be 0-100 or null")
            if isinstance(score, (int, float)):
                check(platform.get("grade") == expected_grade(float(score)), f"platforms[{index}].grade does not match score")
        coverage = platform.get("coverage_pct")
        if coverage is not None:
            check(isinstance(coverage, (int, float)) and 0 <= coverage <= 100, f"platforms[{index}].coverage_pct must be 0-100")
        for metric_index, metric in enumerate(platform.get("metrics", [])):
            check(metric.get("status") in METRIC_STATUS, f"platforms[{index}].metrics[{metric_index}].status is invalid")
            refs = metric.get("source_refs")
            check(isinstance(refs, list) and len(refs) > 0, f"platforms[{index}].metrics[{metric_index}].source_refs is required")
            for source_ref in refs or []:
                check(isinstance(source_ref, int) and 0 <= source_ref < len(data.get("sources", [])), f"platforms[{index}].metrics[{metric_index}] has invalid source_ref {source_ref}")

    for index, item in enumerate(data.get("reconciliations", [])):
        check(isinstance(item, dict), f"reconciliations[{index}] must be an object")
        if not isinstance(item, dict):
            continue
        for key in ("name", "left_label", "right_label", "definitions", "interpretation"):
            check(bool(item.get(key)), f"reconciliations[{index}].{key} is required")
        for side in ("left", "right"):
            check(item.get(f"{side}_value") is not None, f"reconciliations[{index}].{side}_value is required")
            refs = item.get(f"{side}_source_refs")
            check(isinstance(refs, list) and len(refs) > 0, f"reconciliations[{index}].{side}_source_refs is required")
            for source_ref in refs or []:
                check(isinstance(source_ref, int) and 0 <= source_ref < len(data.get("sources", [])), f"reconciliations[{index}] has invalid {side}_source_ref {source_ref}")

    finding_ids: set[str] = set()
    for index, finding in enumerate(data.get("findings", [])):
        check(isinstance(finding, dict), f"findings[{index}] must be an object")
        if not isinstance(finding, dict):
            continue
        finding_id = finding.get("id")
        check(bool(finding_id), f"findings[{index}].id is required")
        check(finding_id not in finding_ids, f"duplicate finding id: {finding_id}")
        if finding_id:
            finding_ids.add(str(finding_id))
        check(finding.get("severity") in SEVERITIES, f"findings[{index}].severity is invalid")
        check(finding.get("confidence") in CONFIDENCE, f"findings[{index}].confidence is invalid")
        for key in ("title", "evidence", "impact", "recommendation"):
            check(bool(finding.get(key)), f"findings[{index}].{key} is required")
        for source_ref in finding.get("source_refs", []):
            check(isinstance(source_ref, int) and 0 <= source_ref < len(data.get("sources", [])), f"findings[{index}] has invalid source_ref {source_ref}")

    for index, action in enumerate(data.get("actions", [])):
        check(isinstance(action, dict), f"actions[{index}] must be an object")
        if not isinstance(action, dict):
            continue
        check(isinstance(action.get("priority"), int), f"actions[{index}].priority must be an integer")
        check(bool(action.get("action")), f"actions[{index}].action is required")
        for finding_id in action.get("finding_ids", []):
            check(str(finding_id) in finding_ids, f"actions[{index}] references unknown finding {finding_id}")
    return errors


def text(value: object, fallback: str = "Not available") -> str:
    if value is None or value == "":
        return fallback
    return str(value)


def markdown_report(data: dict) -> str:
    period = data["period"]
    lines = [
        f"# {text(data.get('title'))}",
        "",
        f"**Client/account:** {text(data.get('client'))}  ",
        f"**Period:** {period['start']} to {period['end']}  ",
        f"**Timezone:** {text(data.get('timezone'))}  ",
        f"**Currency:** {text(data.get('currency'))}  ",
        f"**Generated:** {text(data.get('generated_at'))}",
        "",
        "## Executive Summary",
        "",
        text(data.get("executive_summary")),
        "",
        "## Scope and Data Provenance",
        "",
        "| Source | Account | Range | Grain | Attribution | Status |",
        "|---|---|---|---|---|---|",
    ]
    for source in data.get("sources", []):
        lines.append(f"| {text(source.get('provider'))} | {text(source.get('account'))} | {text(source.get('start'))} to {text(source.get('end'))} | {text(source.get('grain'))} | {text(source.get('attribution'))} | {text(source.get('status'))} |")
    lines += ["", "## Platform Scorecard", "", "| Platform | Score | Grade | Coverage | Spend | Summary |", "|---|---:|:---:|---:|---:|---|"]
    for platform in data.get("platforms", []):
        score = text(platform.get("score"))
        coverage = f"{platform.get('coverage_pct')}%" if platform.get("coverage_pct") is not None else "Not available"
        lines.append(f"| {text(platform.get('name'))} | {score} | {text(platform.get('grade'))} | {coverage} | {text(platform.get('spend'))} | {text(platform.get('summary'))} |")
    lines += ["", "## Key Metrics", "", "| Platform | Metric | Value | Status | Sources |", "|---|---|---:|---|---|"]
    for platform in data.get("platforms", []):
        for metric in platform.get("metrics", []):
            value = f"{text(metric.get('value'))} {text(metric.get('unit'), '')}".strip()
            refs = ", ".join(str(int(ref) + 1) for ref in metric.get("source_refs", []))
            lines.append(f"| {text(platform.get('name'))} | {text(metric.get('name'))} | {value} | {text(metric.get('status'))} | {refs} |")
    if data.get("reconciliations"):
        lines += ["", "### Cross-source Reconciliation", ""]
        for item in data["reconciliations"]:
            lines += [f"**{item['name']}**", "", f"- {item['left_label']}: {text(item.get('left_value'))}", f"- {item['right_label']}: {text(item.get('right_value'))}", f"- Difference: {text(item.get('difference'))} ({text(item.get('difference_pct'))}%)", f"- Definitions: {item['definitions']}", f"- Interpretation: {item['interpretation']}", ""]
    lines += ["", "## Findings", ""]
    if data.get("findings"):
        for finding in sorted(data["findings"], key=lambda item: ("critical", "high", "medium", "low").index(item["severity"])):
            lines += [f"### {finding['id']}: {finding['title']}", "", f"- **Platform/category:** {text(finding.get('platform'))} / {text(finding.get('category'))}", f"- **Severity/confidence:** {finding['severity']} / {finding['confidence']}", f"- **Evidence:** {finding['evidence']}", f"- **Impact:** {finding['impact']}", f"- **Recommendation:** {finding['recommendation']}", f"- **Verification:** {text(finding.get('verification'))}", ""]
    else:
        lines += ["No validated findings were identified in the available evidence.", ""]
    lines += ["## Prioritized Action Plan", "", "| Priority | Action | Owner | Timing | Impact | Effort | Success measure |", "|---:|---|---|---|---|---|---|"]
    for action in sorted(data.get("actions", []), key=lambda item: item.get("priority", 999)):
        lines.append(f"| {text(action.get('priority'))} | {text(action.get('action'))} | {text(action.get('owner'))} | {text(action.get('timing'))} | {text(action.get('impact'))} | {text(action.get('effort'))} | {text(action.get('success_measure'))} |")
    lines += ["", "## Limitations", ""]
    limitations = data.get("limitations", [])
    lines += [f"- {item}" for item in limitations] if limitations else ["- No material limitations beyond those disclosed in the source ledger."]
    lines += ["", "## Methodology", "", text(data.get("methodology")), "", "## Evidence Appendix", ""]
    for index, source in enumerate(data.get("sources", []), 1):
        notes = "; ".join(str(item) for item in source.get("notes", [])) or "None"
        lines.append(f"{index}. **{text(source.get('provider'))} - {text(source.get('account'))}:** filters={text(source.get('filters'))}; attribution={text(source.get('attribution'))}; notes={notes}")
    return "\n".join(lines).rstrip() + "\n"


def build_pdf(data: dict, output: Path) -> None:
    try:
        from reportlab.lib import colors
        from reportlab.lib.enums import TA_CENTER
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.lib.units import inch
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, PageBreak, Paragraph, Spacer, Table, TableStyle, KeepTogether
    except ImportError as exc:
        fail(f"PDF generation requires reportlab: {exc}")

    font = "Helvetica"
    bold = "Helvetica-Bold"
    for candidate in ("/System/Library/Fonts/Supplemental/Arial Unicode.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        if Path(candidate).exists():
            pdfmetrics.registerFont(TTFont("ReportUnicode", candidate))
            font = "ReportUnicode"
            bold = "ReportUnicode"
            break

    navy, blue, pale, ink, muted = colors.HexColor("#132238"), colors.HexColor("#276EF1"), colors.HexColor("#EDF3FF"), colors.HexColor("#1D2733"), colors.HexColor("#5E6B78")
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="CoverTitle", parent=styles["Title"], fontName=bold, fontSize=26, leading=31, textColor=navy, alignment=TA_CENTER, spaceAfter=20))
    styles.add(ParagraphStyle(name="Section", parent=styles["Heading1"], fontName=bold, fontSize=16, leading=20, textColor=navy, spaceBefore=14, spaceAfter=9))
    styles.add(ParagraphStyle(name="Subsection", parent=styles["Heading2"], fontName=bold, fontSize=11, leading=14, textColor=blue, spaceBefore=9, spaceAfter=5))
    styles.add(ParagraphStyle(name="Body2", parent=styles["BodyText"], fontName=font, fontSize=9, leading=13, textColor=ink, spaceAfter=6))
    styles.add(ParagraphStyle(name="Small", parent=styles["BodyText"], fontName=font, fontSize=7.5, leading=10, textColor=ink))
    styles.add(ParagraphStyle(name="TableHeader", parent=styles["BodyText"], fontName=bold, fontSize=7.5, leading=10, textColor=colors.white))

    output.parent.mkdir(parents=True, exist_ok=True)

    def footer(canvas, doc):
        canvas.saveState()
        canvas.setFont(font, 8)
        canvas.setFillColor(muted)
        canvas.drawString(0.75 * inch, 0.42 * inch, text(data.get("client")))
        canvas.drawRightString(A4[0] - 0.75 * inch, 0.42 * inch, f"Page {doc.page}")
        canvas.restoreState()

    doc = BaseDocTemplate(str(output), pagesize=A4, leftMargin=0.75 * inch, rightMargin=0.75 * inch, topMargin=0.75 * inch, bottomMargin=0.7 * inch, title=text(data.get("title")), author="Paid Ads skill")
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal")
    doc.addPageTemplates([PageTemplate(id="report", frames=[frame], onPage=footer)])

    def p(value, style="Body2"):
        safe = text(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        return Paragraph(safe, styles[style])

    def table(rows, widths, header=True):
        wrapped = []
        for row_index, row in enumerate(rows):
            style = "TableHeader" if header and row_index == 0 else "Small"
            wrapped.append([cell if hasattr(cell, "wrap") else p(cell, style) for cell in row])
        result = Table(wrapped, colWidths=widths, repeatRows=1 if header else 0, hAlign="LEFT")
        commands = [("VALIGN", (0, 0), (-1, -1), "TOP"), ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#CCD5DF")), ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5), ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]
        if header:
            commands += [("BACKGROUND", (0, 0), (-1, 0), navy), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white)]
        result.setStyle(TableStyle(commands))
        return result

    period = data["period"]
    story = [Spacer(1, 1.35 * inch), p(data.get("title"), "CoverTitle"), p(data.get("client"), "CoverTitle"), Spacer(1, 0.2 * inch), p(f"{period['start']} to {period['end']}", "Body2"), p(f"{text(data.get('timezone'))} | {text(data.get('currency'))}", "Body2"), PageBreak()]
    story += [p("Executive Summary", "Section"), p(data.get("executive_summary"))]
    story += [p("Scope and Data Provenance", "Section")]
    source_rows = [["Source", "Account", "Range", "Attribution", "Status"]]
    for source in data.get("sources", []):
        source_rows.append([source.get("provider"), source.get("account"), f"{source.get('start')} to {source.get('end')}", source.get("attribution"), source.get("status")])
    story += [table(source_rows, [0.95*inch, 1.15*inch, 1.25*inch, 1.55*inch, 0.65*inch])]
    story += [p("Platform Scorecard", "Section")]
    platform_rows = [["Platform", "Score", "Grade", "Coverage", "Spend", "Summary"]]
    for platform in data.get("platforms", []):
        platform_rows.append([platform.get("name"), platform.get("score"), platform.get("grade"), f"{platform.get('coverage_pct')}%" if platform.get("coverage_pct") is not None else None, platform.get("spend"), platform.get("summary")])
    story += [table(platform_rows, [0.8*inch, 0.5*inch, 0.42*inch, 0.62*inch, 0.72*inch, 2.5*inch])]
    story += [p("Key Metrics", "Section")]
    metric_rows = [["Platform", "Metric", "Value", "Status", "Sources"]]
    for platform in data.get("platforms", []):
        for metric in platform.get("metrics", []):
            value = f"{text(metric.get('value'))} {text(metric.get('unit'), '')}".strip()
            refs = ", ".join(str(int(ref) + 1) for ref in metric.get("source_refs", []))
            metric_rows.append([platform.get("name"), metric.get("name"), value, metric.get("status"), refs])
    story += [table(metric_rows, [1.15*inch, 1.15*inch, 1.1*inch, 1.0*inch, 0.65*inch])]
    if data.get("reconciliations"):
        story += [p("Cross-source Reconciliation", "Subsection")]
        for item in data["reconciliations"]:
            story += [p(item["name"], "Subsection"), p(f"{item['left_label']}: {text(item.get('left_value'))} | {item['right_label']}: {text(item.get('right_value'))} | Difference: {text(item.get('difference'))} ({text(item.get('difference_pct'))}%)"), p(f"Definitions: {item['definitions']}"), p(f"Interpretation: {item['interpretation']}")]
    story += [p("Findings", "Section")]
    if data.get("findings"):
        for finding in sorted(data["findings"], key=lambda item: ("critical", "high", "medium", "low").index(item["severity"])):
            block = [p(f"{finding['id']}: {finding['title']}", "Subsection"), p(f"Severity: {finding['severity']} | Confidence: {finding['confidence']} | Platform: {text(finding.get('platform'))}"), p(f"Evidence: {finding['evidence']}"), p(f"Impact: {finding['impact']}"), p(f"Recommendation: {finding['recommendation']}")]
            story.append(KeepTogether(block))
    else:
        story += [p("No validated findings were identified in the available evidence.")]
    story += [p("Prioritized Action Plan", "Section")]
    action_rows = [["#", "Action", "Owner", "Timing", "Impact", "Success measure"]]
    for action in sorted(data.get("actions", []), key=lambda item: item.get("priority", 999)):
        action_rows.append([action.get("priority"), action.get("action"), action.get("owner"), action.get("timing"), action.get("impact"), action.get("success_measure")])
    story += [table(action_rows, [0.32*inch, 2.15*inch, 0.75*inch, 0.75*inch, 0.6*inch, 1.65*inch])]
    story += [p("Limitations", "Section")]
    limitations = data.get("limitations", []) or ["No material limitations beyond those disclosed in the source ledger."]
    story += [p(f"- {item}") for item in limitations]
    story += [p("Methodology", "Section"), p(data.get("methodology")), p("Evidence Appendix", "Section")]
    for index, source in enumerate(data.get("sources", []), 1):
        notes = "; ".join(str(item) for item in source.get("notes", [])) or "None"
        story += [p(f"{index}. {text(source.get('provider'))} - {text(source.get('account'))}", "Subsection"), p(f"Range: {text(source.get('start'))} to {text(source.get('end'))}; grain: {text(source.get('grain'))}; filters: {text(source.get('filters'))}; attribution: {text(source.get('attribution'))}; notes: {notes}")]
    doc.build(story)


def check_pdf(path: Path) -> list[str]:
    errors: list[str] = []
    if not path.exists() or path.stat().st_size < 1000:
        return [f"PDF is missing or unexpectedly small: {path}"]
    try:
        from pypdf import PdfReader
        reader = PdfReader(str(path))
        if not reader.pages:
            errors.append("PDF contains no pages")
        for index, page in enumerate(reader.pages, 1):
            width = float(page.mediabox.width)
            height = float(page.mediabox.height)
            if width <= 0 or height <= 0:
                errors.append(f"page {index} has invalid bounds")
            extracted = (page.extract_text() or "").strip()
            if not extracted:
                errors.append(f"page {index} appears blank or has no extractable text")
    except Exception as exc:
        errors.append(f"PDF parse failed: {exc}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path)
    parser.add_argument("--check-input", action="store_true")
    parser.add_argument("--markdown", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check-pdf", type=Path)
    args = parser.parse_args()

    if args.check_pdf and not args.input and not args.markdown and not args.output:
        errors = check_pdf(args.check_pdf)
        if errors:
            print("\n".join(f"ERROR: {item}" for item in errors), file=sys.stderr)
            return 1
        print(f"PDF structural check passed: {args.check_pdf}")
        return 0
    if not args.input:
        parser.error("--input is required unless only --check-pdf is used")

    data = load_json(args.input)
    errors = validate(data)
    if errors:
        print("\n".join(f"ERROR: {item}" for item in errors), file=sys.stderr)
        return 1
    print(f"Input validation passed: {args.input}")
    if args.check_input and not args.markdown and not args.output:
        return 0
    if args.markdown:
        args.markdown.parent.mkdir(parents=True, exist_ok=True)
        args.markdown.write_text(markdown_report(data), encoding="utf-8")
        print(f"Markdown written: {args.markdown}")
    if args.output:
        build_pdf(data, args.output)
        pdf_errors = check_pdf(args.output)
        if pdf_errors:
            print("\n".join(f"ERROR: {item}" for item in pdf_errors), file=sys.stderr)
            return 1
        print(f"PDF written and structurally checked: {args.output}")
    if not args.check_input and not args.markdown and not args.output:
        parser.error("choose --check-input, --markdown, or --output")
    return 0


if __name__ == "__main__":
    try:
        exit_code = main()
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        exit_code = 1
    raise SystemExit(exit_code)
