from __future__ import annotations

from html import escape
from io import BytesIO
from pathlib import Path
from typing import Mapping

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from app_core.insights import build_business_insights
from app_core.metrics import summarize_metric
from app_core.quality import calculate_quality_score
from app_core.report_themes import ReportTheme, get_report_theme
from app_core.version import PRODUCT_VERSION


def _color(value: str):
    return colors.HexColor(f"#{value}")


def _register_fonts() -> tuple[str, str]:
    candidates = (
        (
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        ),
        (
            "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/arialbd.ttf",
        ),
    )
    for regular_path, bold_path in candidates:
        if Path(regular_path).exists() and Path(bold_path).exists():
            pdfmetrics.registerFont(
                TTFont("DashboardBody", regular_path)
            )
            pdfmetrics.registerFont(
                TTFont("DashboardBold", bold_path)
            )
            return "DashboardBody", "DashboardBold"
    return "Helvetica", "Helvetica-Bold"


def _format_number(value: float) -> str:
    absolute = abs(value)
    if absolute >= 1_000_000_000:
        return f"{value / 1_000_000_000:.1f}B"
    if absolute >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"
    if absolute >= 1_000:
        return f"{value / 1_000:.1f}K"
    return f"{value:,.2f}".rstrip("0").rstrip(".")


def _safe(value: object) -> str:
    return escape(str(value))


def _styles(theme: ReportTheme):
    body_font, bold_font = _register_fonts()
    styles = getSampleStyleSheet()
    return {
        "body_font": body_font,
        "bold_font": bold_font,
        "title": ParagraphStyle(
            "DashboardTitle",
            parent=styles["Title"],
            fontName=bold_font,
            fontSize=25,
            leading=30,
            textColor=_color(theme.text),
            alignment=TA_LEFT,
            spaceAfter=5 * mm,
        ),
        "hero_title": ParagraphStyle(
            "DashboardHeroTitle",
            parent=styles["Title"],
            fontName=bold_font,
            fontSize=24,
            leading=29,
            textColor=_color(theme.title_text),
            alignment=TA_LEFT,
            spaceAfter=3 * mm,
        ),
        "hero_subtitle": ParagraphStyle(
            "DashboardHeroSubtitle",
            parent=styles["BodyText"],
            fontName=body_font,
            fontSize=10.5,
            leading=15,
            textColor=_color(theme.title_text),
        ),
        "subtitle": ParagraphStyle(
            "DashboardSubtitle",
            parent=styles["BodyText"],
            fontName=body_font,
            fontSize=11,
            leading=16,
            textColor=_color(theme.muted),
            spaceAfter=7 * mm,
        ),
        "heading": ParagraphStyle(
            "DashboardHeading",
            parent=styles["Heading2"],
            fontName=bold_font,
            fontSize=16,
            leading=20,
            textColor=_color(theme.text),
            spaceBefore=4 * mm,
            spaceAfter=3 * mm,
        ),
        "card_title": ParagraphStyle(
            "DashboardCardTitle",
            parent=styles["Heading3"],
            fontName=bold_font,
            fontSize=11,
            leading=14,
            textColor=_color(theme.text),
            spaceAfter=2 * mm,
        ),
        "body": ParagraphStyle(
            "DashboardBody",
            parent=styles["BodyText"],
            fontName=body_font,
            fontSize=9,
            leading=13,
            textColor=_color(theme.text),
            spaceAfter=2 * mm,
        ),
        "small": ParagraphStyle(
            "DashboardSmall",
            parent=styles["BodyText"],
            fontName=body_font,
            fontSize=7.5,
            leading=10,
            textColor=_color(theme.muted),
        ),
        "center": ParagraphStyle(
            "DashboardCenter",
            parent=styles["BodyText"],
            fontName=bold_font,
            fontSize=10,
            leading=13,
            textColor=_color(theme.text),
            alignment=TA_CENTER,
        ),
    }


def _hero(styles, theme: ReportTheme) -> Table:
    table = Table(
        [
            [
                Paragraph(
                    "Universal CSV Dashboard",
                    styles["hero_title"],
                )
            ],
            [
                Paragraph(
                    "Executive analysis report with traceable calculations, "
                    "quality context and responsible interpretation.",
                    styles["hero_subtitle"],
                )
            ],
        ],
        colWidths=[174 * mm],
    )
    table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    _color(theme.title_background),
                ),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, 0), 9),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 0),
                ("TOPPADDING", (0, 1), (-1, 1), 0),
                ("BOTTOMPADDING", (0, 1), (-1, 1), 9),
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    _color(theme.border),
                ),
            ]
        )
    )
    return table


def _page_footer(canvas, document) -> None:
    canvas.saveState()
    width, height = A4
    theme = document.report_theme
    body_font, _ = _register_fonts()
    canvas.setFillColor(_color(theme.page_background))
    canvas.rect(0, 0, width, height, fill=1, stroke=0)
    canvas.setStrokeColor(_color(theme.border))
    canvas.line(
        document.leftMargin,
        14 * mm,
        width - document.rightMargin,
        14 * mm,
    )
    canvas.setFont(body_font, 7)
    canvas.setFillColor(_color(theme.muted))
    canvas.drawString(
        document.leftMargin,
        9 * mm,
        "Universal CSV Dashboard - generated locally",
    )
    canvas.drawRightString(
        width - document.rightMargin,
        9 * mm,
        f"Page {document.page}",
    )
    canvas.restoreState()


def _metadata_table(
    dataframe: pd.DataFrame,
    config: Mapping[str, object],
    source_name: str,
    styles,
    theme: ReportTheme,
) -> Table:
    date_column = config.get("date_column")
    if isinstance(date_column, str) and date_column in dataframe.columns:
        dates = pd.to_datetime(
            dataframe[date_column],
            errors="coerce",
        ).dropna()
        date_range = (
            f"{dates.min():%Y-%m-%d} to {dates.max():%Y-%m-%d}"
            if not dates.empty
            else "No valid dates"
        )
    else:
        date_range = "Not configured"

    data = [
        [
            Paragraph("<b>Source file</b>", styles["body"]),
            Paragraph(_safe(source_name), styles["body"]),
            Paragraph("<b>Date range</b>", styles["body"]),
            Paragraph(_safe(date_range), styles["body"]),
        ],
        [
            Paragraph("<b>Rows</b>", styles["body"]),
            Paragraph(f"{len(dataframe):,}", styles["body"]),
            Paragraph("<b>Columns</b>", styles["body"]),
            Paragraph(f"{len(dataframe.columns):,}", styles["body"]),
        ],
        [
            Paragraph("<b>Primary metric</b>", styles["body"]),
            Paragraph(
                _safe(config.get("metric_column", "Not configured")),
                styles["body"],
            ),
            Paragraph("<b>Aggregation</b>", styles["body"]),
            Paragraph(
                _safe(config.get("aggregation", "Sum")),
                styles["body"],
            ),
        ],
        [
            Paragraph("<b>Product version</b>", styles["body"]),
            Paragraph(_safe(PRODUCT_VERSION), styles["body"]),
            Paragraph("<b>Export type</b>", styles["body"]),
            Paragraph("Executive PDF", styles["body"]),
        ],
        [
            Paragraph("<b>Report theme</b>", styles["body"]),
            Paragraph(_safe(theme.name), styles["body"]),
            Paragraph("<b>Generated locally</b>", styles["body"]),
            Paragraph("Yes", styles["body"]),
        ],
    ]
    table = Table(
        data,
        colWidths=[33 * mm, 55 * mm, 32 * mm, 55 * mm],
        hAlign="LEFT",
    )
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), _color(theme.surface_alt)),
                ("BOX", (0, 0), (-1, -1), 0.5, _color(theme.border)),
                ("INNERGRID", (0, 0), (-1, -1), 0.25, _color(theme.border)),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return table


def _kpi_table(
    dataframe: pd.DataFrame,
    metric: str,
    styles,
    theme: ReportTheme,
) -> Table:
    summary = summarize_metric(dataframe, metric)
    data = [
        [
            Paragraph("TOTAL", styles["center"]),
            Paragraph("AVERAGE", styles["center"]),
            Paragraph("MEDIAN", styles["center"]),
            Paragraph("NON-NULL", styles["center"]),
        ],
        [
            Paragraph(_format_number(summary.total), styles["center"]),
            Paragraph(_format_number(summary.average), styles["center"]),
            Paragraph(_format_number(summary.median), styles["center"]),
            Paragraph(f"{summary.non_null_count:,}", styles["center"]),
        ],
    ]
    table = Table(
        data,
        colWidths=[43.5 * mm] * 4,
        hAlign="LEFT",
    )
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), _color(theme.accent_soft)),
                ("BACKGROUND", (0, 1), (-1, 1), _color(theme.surface)),
                ("BOX", (0, 0), (-1, -1), 0.6, _color(theme.accent)),
                ("INNERGRID", (0, 0), (-1, -1), 0.35, _color(theme.border)),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    return table


def _quality_summary_table(
    quality,
    styles,
    theme: ReportTheme,
) -> Table:
    data = [
        [
            Paragraph("Data Quality Score", styles["center"]),
            Paragraph("Detected issues", styles["center"]),
        ],
        [
            Paragraph(
                f"{quality.score:.1f}/100 ({_safe(quality.status)})",
                styles["center"],
            ),
            Paragraph(
                f"{quality.issue_count:,}",
                styles["center"],
            ),
        ],
    ]
    table = Table(
        data,
        colWidths=[87 * mm, 87 * mm],
        hAlign="LEFT",
    )
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), _color(theme.success_soft)),
                ("BACKGROUND", (0, 1), (-1, 1), _color(theme.surface_alt)),
                ("BOX", (0, 0), (-1, -1), 0.6, _color(theme.accent)),
                ("INNERGRID", (0, 0), (-1, -1), 0.35, _color(theme.border)),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, 0), 6),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
                ("TOPPADDING", (0, 1), (-1, 1), 8),
                ("BOTTOMPADDING", (0, 1), (-1, 1), 8),
            ]
        )
    )
    return table


def _insight_card(
    insight,
    styles,
    theme: ReportTheme,
) -> KeepTogether:
    confidence_color = {
        "High": _color(theme.success_soft),
        "Moderate": _color(theme.accent_soft),
        "Low": _color(theme.warning_soft),
    }.get(insight.confidence, _color(theme.surface_alt))
    header = Table(
        [
            [
                Paragraph(
                    f"{_safe(insight.insight_type).upper()} - "
                    f"{_safe(insight.title)}",
                    styles["card_title"],
                ),
                Paragraph(
                    f"{_safe(insight.confidence)} confidence",
                    styles["center"],
                ),
            ]
        ],
        colWidths=[130 * mm, 44 * mm],
    )
    header.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, 0), _color(theme.accent_soft)),
                ("BACKGROUND", (1, 0), (1, 0), confidence_color),
                ("BOX", (0, 0), (-1, -1), 0.5, _color(theme.accent)),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    body = Table(
        [
            [
                Paragraph(
                    f"<b>Observation:</b> {_safe(insight.observation)}",
                    styles["body"],
                )
            ],
            [Paragraph(_safe(insight.interpretation), styles["body"])],
            [
                Paragraph(
                    f"<b>Evidence:</b> {_safe(insight.evidence)}",
                    styles["small"],
                )
            ],
            [
                Paragraph(
                    f"<b>Confidence basis:</b> "
                    f"{_safe(insight.confidence_reason)}",
                    styles["small"],
                )
            ],
            [
                Paragraph(
                    f"<b>Limitation:</b> {_safe(insight.limitation)}",
                    styles["small"],
                )
            ],
        ],
        colWidths=[174 * mm],
    )
    body.setStyle(
        TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 0.5, _color(theme.border)),
                ("BACKGROUND", (0, 0), (-1, -1), _color(theme.surface)),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return KeepTogether([header, body, Spacer(1, 4 * mm)])


def build_pdf_report(
    dataframe: pd.DataFrame,
    config: Mapping[str, object],
    source_name: str = "uploaded.csv",
    theme_name: str = "Corporate",
) -> bytes:
    """Build a concise executive PDF without exporting raw row-level data."""

    metric = config.get("metric_column")
    if not isinstance(metric, str) or metric not in dataframe.columns:
        raise ValueError(
            "A valid primary metric is required for PDF export."
        )

    theme = get_report_theme(theme_name)
    styles = _styles(theme)
    quality = calculate_quality_score(dataframe)
    insights = build_business_insights(dataframe, config)
    buffer = BytesIO()
    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=21 * mm,
        title="Universal CSV Dashboard - Executive Report",
        author="Universal CSV Dashboard",
    )
    document.report_theme = theme
    story = [
        _hero(styles, theme),
        Spacer(1, 6 * mm),
        _metadata_table(
            dataframe,
            config,
            source_name,
            styles,
            theme,
        ),
        Paragraph("Executive snapshot", styles["heading"]),
        _kpi_table(dataframe, metric, styles, theme),
        Spacer(1, 5 * mm),
        _quality_summary_table(quality, styles, theme),
        Spacer(1, 1 * mm),
        Paragraph(
            "Scope note",
            styles["heading"],
        ),
        Paragraph(
            "This PDF contains summary evidence and methodology only. "
            "It does not contain the complete row-level dataset. "
            "Observations describe the selected data and do not establish "
            "causes or guarantee business outcomes.",
            styles["body"],
        ),
        PageBreak(),
        Paragraph("What deserves attention", styles["title"]),
        Paragraph(
            "Each card separates observation, interpretation, evidence, "
            "confidence basis and limitation.",
            styles["subtitle"],
        ),
    ]

    if insights.insights:
        story.extend(
            _insight_card(insight, styles, theme)
            for insight in insights.insights
        )
    else:
        story.append(
            Paragraph(
                "No material pattern crossed the current rule thresholds.",
                styles["body"],
            )
        )

    story.extend(
        [
            Paragraph("Suggested next questions", styles["heading"]),
            *[
                Paragraph(
                    f"{number}. {_safe(question)}",
                    styles["body"],
                )
                for number, question in enumerate(
                    insights.questions,
                    start=1,
                )
            ],
        ]
    )
    if insights.limitations:
        story.extend(
            [
                Paragraph("Analysis limitations", styles["heading"]),
                *[
                    Paragraph(
                        f"- {_safe(limitation)}",
                        styles["body"],
                    )
                    for limitation in insights.limitations
                ],
            ]
        )

    story.extend(
        [
            PageBreak(),
            Paragraph(
                "Methodology and responsible use",
                styles["title"],
            ),
            Paragraph(
                "The report is deterministic and generated locally from "
                "the configured dataset.",
                styles["subtitle"],
            ),
        ]
    )
    methodology = (
        (
            "Data Quality",
            "Completeness 50%, duplicate-free rows 30%, type validity 20%.",
            "Technical quality does not prove business accuracy.",
        ),
        (
            "Trend",
            "Compares average daily metric in the first and second half.",
            "The comparison does not establish seasonality or causation.",
        ),
        (
            "Anomaly",
            "Flags values outside 1.5 times the interquartile range.",
            "A flagged value is not automatically an error.",
        ),
        (
            "Relationship",
            "Reports Pearson correlation when absolute correlation is at "
            "least 0.50.",
            "Correlation does not prove causation.",
        ),
        (
            "Confidence",
            "Uses sample size, metric completeness and Data Quality Score.",
            "The label describes evidence reliability, not certainty.",
        ),
    )
    table_data = [
        ["Area", "Method", "Important limitation"]
    ]
    for area, method, limitation in methodology:
        table_data.append(
            [
                Paragraph(area, styles["body"]),
                Paragraph(method, styles["body"]),
                Paragraph(limitation, styles["body"]),
            ]
        )
    methodology_table = Table(
        table_data,
        colWidths=[29 * mm, 74 * mm, 71 * mm],
        repeatRows=1,
    )
    methodology_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), _color(theme.accent)),
                ("TEXTCOLOR", (0, 0), (-1, 0), _color(theme.accent_text)),
                ("FONTNAME", (0, 0), (-1, 0), styles["bold_font"]),
                ("FONTSIZE", (0, 0), (-1, 0), 10),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [_color(theme.surface), _color(theme.surface_alt)],
                ),
                ("GRID", (0, 0), (-1, -1), 0.35, _color(theme.border)),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    story.extend(
        [
            methodology_table,
            Spacer(1, 7 * mm),
            Paragraph("Privacy and sharing", styles["heading"]),
            Paragraph(
                "The report is generated in the current Streamlit session. "
                "Review the source name, summaries and insight text before "
                "sharing. Use the Excel export only when recipients also "
                "need row-level data.",
                styles["body"],
            ),
        ]
    )

    document.build(
        story,
        onFirstPage=_page_footer,
        onLaterPages=_page_footer,
    )
    return buffer.getvalue()
