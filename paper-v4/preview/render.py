"""Render the paper's small Markdown subset as a review PDF, not arXiv sources."""

import argparse
from functools import partial
from html import escape
import json
from pathlib import Path
import re

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import (
    KeepTogether,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


def inline(text):
    text = escape(" ".join(text.split()))

    def link(match):
        label, target = match.groups()
        if target.startswith(("https://", "http://")):
            return f'<link href="{target}" color="#254b65">{label}</link>'
        return label

    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link, text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    return re.sub(r"\*([^*]+)\*", r"<i>\1</i>", text)


def table_rows(block):
    lines = block.splitlines()
    rows = [
        [cell.strip() for cell in line.strip().strip("|").split("|")] for line in lines
    ]
    if len(rows) < 3 or any(len(row) != len(rows[0]) for row in rows):
        raise ValueError("Table requires a header, separator and equal-width data rows")
    if not all(re.fullmatch(r":?-{3,}:?", cell) for cell in rows[1]):
        raise ValueError("Malformed table separator")
    if len(rows[0]) not in {4, 8}:
        raise ValueError(
            "Review layout supports only the four/eight-column paper tables"
        )
    return [rows[0], *rows[2:]]


def column_weights(count):
    if count == 4:
        return [0.30, 0.12, 0.12, 0.46]
    if count == 8:
        return [0.15, 0.11, 0.09, 0.12, 0.13, 0.15, 0.14, 0.11]
    raise ValueError("Review layout supports only four/eight-column paper tables")


def grouped_exhibit(flow, contents):
    if flow and isinstance(flow[-1], Paragraph):
        contents.insert(0, flow.pop())
    while flow and isinstance(flow[-1], Paragraph) and flow[-1].getKeepWithNext():
        contents.insert(0, flow.pop())
    return KeepTogether(contents)


def render(source, output):
    if source.resolve() == output.resolve():
        raise ValueError("PDF output must not overwrite the Markdown source")
    text = source.read_text()
    if not text.startswith("# ") or re.search(
        r"(?m)^(?:```(?!json$|$)|[-*] |\d+\. )", text
    ):
        raise ValueError(
            "Unsupported Markdown: expected title, headings, paragraphs and tables"
        )
    output.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(output),
        pagesize=A4,
        leftMargin=48,
        rightMargin=48,
        topMargin=43,
        bottomMargin=45,
        title=text.splitlines()[0][2:],
        author="Luis Guzman Lorenzo",
    )
    body = ParagraphStyle(
        "body", fontName="Times-Roman", fontSize=10.5, leading=13.3, spaceAfter=6
    )
    headings = {
        1: ParagraphStyle(
            "title",
            fontName="Times-Bold",
            fontSize=20,
            leading=23,
            spaceAfter=9,
            keepWithNext=True,
        ),
        2: ParagraphStyle(
            "section",
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=15,
            spaceBefore=10,
            spaceAfter=6,
            keepWithNext=True,
        ),
        3: ParagraphStyle(
            "subsection",
            fontName="Helvetica-Bold",
            fontSize=10.3,
            leading=13,
            spaceBefore=6,
            spaceAfter=5,
            keepWithNext=True,
        ),
    }
    cell = ParagraphStyle("cell", parent=body, fontSize=9, leading=11.4, spaceAfter=0)
    header = ParagraphStyle(
        "header", parent=cell, fontName="Helvetica-Bold", fontSize=8.2, leading=10
    )
    code = ParagraphStyle(
        "evidence",
        fontName="Courier",
        fontSize=8,
        leading=10,
        leftIndent=6,
        spaceBefore=3,
        spaceAfter=8,
    )
    flow = []
    for block in re.split(r"\n\s*\n", text.strip()):
        if block.startswith("```"):
            match = re.fullmatch(r"```json\n(.+)\n```", block, re.S)
            if match is None:
                raise ValueError("Unsupported or incomplete JSON exhibit")
            json.loads(match[1])
            if any(len(line) > 100 for line in match[1].splitlines()):
                raise ValueError("JSON exhibit exceeds the 100-character print width")
            flow.append(grouped_exhibit(flow, [Preformatted(match[1], code)]))
        elif block.startswith("#"):
            match = re.fullmatch(r"(#{1,3}) (.+)", block)
            if match is None:
                raise ValueError(f"Unsupported heading: {block!r}")
            if match[1] == "##" and match[2].startswith("Appendix "):
                flow.append(PageBreak())
            flow.append(Paragraph(inline(match[2]), headings[len(match[1])]))
        elif block.startswith("|"):
            rows = table_rows(block)
            weights = column_weights(len(rows[0]))
            values = [
                [Paragraph(inline(value), header if i == 0 else cell) for value in row]
                for i, row in enumerate(rows)
            ]
            table = Table(
                values,
                colWidths=[doc.width * w for w in weights],
                repeatRows=1,
                hAlign="LEFT",
            )
            table.setStyle(
                TableStyle(
                    [
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("LINEABOVE", (0, 0), (-1, 0), 0.7, colors.black),
                        ("LINEBELOW", (0, 0), (-1, 0), 0.4, colors.black),
                        ("LINEBELOW", (0, -1), (-1, -1), 0.7, colors.black),
                        ("LEFTPADDING", (0, 0), (-1, -1), 4),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                        ("TOPPADDING", (0, 0), (-1, -1), 5),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                    ]
                )
            )
            flow.append(grouped_exhibit(flow, [table, Spacer(1, 8)]))
        else:
            flow.append(Paragraph(inline(block), body))

    def footer(canvas, document):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#555555"))
        canvas.drawString(48, 25, "Malleus | Author-review draft")
        canvas.drawRightString(A4[0] - 48, 25, str(document.page))
        canvas.restoreState()

    doc.build(
        flow,
        onFirstPage=footer,
        onLaterPages=footer,
        canvasmaker=partial(Canvas, invariant=1),
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    render(args.source, args.output)
