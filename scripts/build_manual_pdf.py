#!/usr/bin/env python
"""Build the Spanish operating manual PDF from its Markdown source."""
from __future__ import annotations

from html import escape
from pathlib import Path
import re
import os

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageTemplate,
    PageBreak,
    Paragraph,
    Spacer,
)

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "MANUAL-SAP-ABAP-LAB-001.md"
OUTPUT = ROOT / "docs" / "MANUAL-SAP-ABAP-LAB-001.pdf"

FONT_DIR = Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts"
if (FONT_DIR / "segoeui.ttf").exists() and (FONT_DIR / "segoeuib.ttf").exists():
    pdfmetrics.registerFont(TTFont("SegoeUI", str(FONT_DIR / "segoeui.ttf")))
    pdfmetrics.registerFont(TTFont("SegoeUI-Bold", str(FONT_DIR / "segoeuib.ttf")))
    BASE_FONT = "SegoeUI"
    BOLD_FONT = "SegoeUI-Bold"
else:
    BASE_FONT = "Helvetica"
    BOLD_FONT = "Helvetica-Bold"


def inline_markup(text: str) -> str:
    text = escape(text)
    text = re.sub(r"`([^`]+)`", r'<font name="Courier">\1</font>', text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    return text


def header_footer(canvas, doc):
    canvas.saveState()
    width, height = A4
    canvas.setStrokeColor(colors.HexColor("#D5D9E2"))
    canvas.line(18 * mm, height - 16 * mm, width - 18 * mm, height - 16 * mm)
    canvas.setFont(BASE_FONT, 8)
    canvas.setFillColor(colors.HexColor("#5C6472"))
    canvas.drawString(18 * mm, height - 12 * mm, "SAP ABAP LAB 001 — Manual operativo")
    canvas.drawRightString(width - 18 * mm, 11 * mm, f"Página {doc.page}")
    canvas.restoreState()


def build() -> Path:
    styles = getSampleStyleSheet()
    body = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontName=BASE_FONT,
        fontSize=9.3,
        leading=13.1,
        textColor=colors.HexColor("#20242C"),
        spaceAfter=5,
    )
    h1 = ParagraphStyle(
        "H1",
        parent=styles["Heading1"],
        fontName=BOLD_FONT,
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#0B5CAB"),
        spaceBefore=8,
        spaceAfter=12,
    )
    h2 = ParagraphStyle(
        "H2",
        parent=styles["Heading2"],
        fontName=BOLD_FONT,
        fontSize=13.5,
        leading=17,
        textColor=colors.HexColor("#163B65"),
        spaceBefore=12,
        spaceAfter=7,
        keepWithNext=True,
    )
    h3 = ParagraphStyle(
        "H3",
        parent=styles["Heading3"],
        fontName=BOLD_FONT,
        fontSize=11,
        leading=14,
        textColor=colors.HexColor("#2D4C70"),
        spaceBefore=8,
        spaceAfter=5,
        keepWithNext=True,
    )
    bullet = ParagraphStyle(
        "Bullet",
        parent=body,
        leftIndent=12,
        firstLineIndent=-7,
        bulletIndent=3,
        spaceAfter=3,
    )
    numbered = ParagraphStyle(
        "Numbered",
        parent=body,
        leftIndent=15,
        firstLineIndent=-12,
        spaceAfter=3,
    )
    cover_title = ParagraphStyle(
        "CoverTitle",
        parent=h1,
        alignment=TA_CENTER,
        fontSize=26,
        leading=31,
        spaceAfter=18,
    )
    cover_sub = ParagraphStyle(
        "CoverSub",
        parent=body,
        alignment=TA_CENTER,
        fontSize=12,
        leading=17,
        textColor=colors.HexColor("#4B5565"),
    )

    doc = BaseDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=23 * mm,
        bottomMargin=18 * mm,
        title="Manual operativo SAP ABAP LAB 001",
        author="Hermes Agent",
        subject="Hermes Desktop, Claude Desktop/Code, ARC-1 y skills ABAP",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal")
    doc.addPageTemplates(PageTemplate(id="main", frames=[frame], onPage=header_footer))

    story = [
        Spacer(1, 35 * mm),
        Paragraph("SAP ABAP LAB 001", cover_title),
        Paragraph("Manual operativo de desarrollo agentic ABAP", cover_sub),
        Spacer(1, 8 * mm),
        Paragraph("Hermes Desktop · Claude Code · Claude Desktop · ARC-1", cover_sub),
        Spacer(1, 8 * mm),
        Paragraph("Sistema: SAP S/4HANA 2025 on-premise · Cliente 100", cover_sub),
        Spacer(1, 35 * mm),
        Paragraph("Documento generado desde el workspace versionable. No contiene credenciales.", cover_sub),
        PageBreak(),
    ]

    for raw in SOURCE.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line:
            story.append(Spacer(1, 2.5 * mm))
            continue
        if line.startswith("# "):
            # The cover already contains the document title.
            continue
        if line.startswith("## "):
            story.append(Paragraph(inline_markup(line[3:]), h2))
            continue
        if line.startswith("### "):
            story.append(Paragraph(inline_markup(line[4:]), h3))
            continue
        if line.startswith("- "):
            story.append(Paragraph(inline_markup(line[2:]), bullet, bulletText="•"))
            continue
        match = re.match(r"^(\d+)\.\s+(.*)$", line)
        if match:
            story.append(Paragraph(inline_markup(match.group(2)), numbered, bulletText=match.group(1) + "."))
            continue
        story.append(Paragraph(inline_markup(line), body))

    doc.build(story)
    return OUTPUT


if __name__ == "__main__":
    print(build())
