from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ReportTheme:
    """Cross-format colors and presentation metadata."""

    name: str
    description: str
    page_background: str
    surface: str
    surface_alt: str
    title_background: str
    title_text: str
    accent: str
    accent_text: str
    accent_soft: str
    text: str
    muted: str
    border: str
    success_soft: str
    warning_soft: str
    excel_table_style: str


REPORT_THEMES = {
    "Light": ReportTheme(
        name="Light",
        description="Airy neutral report with restrained blue accents.",
        page_background="FFFFFF",
        surface="FFFFFF",
        surface_alt="F5F7FB",
        title_background="F5F7FB",
        title_text="102348",
        accent="3867E8",
        accent_text="FFFFFF",
        accent_soft="EAF0FF",
        text="334155",
        muted="64748B",
        border="D9E2F1",
        success_soft="DFF4E5",
        warning_soft="FFF1D6",
        excel_table_style="TableStyleMedium2",
    ),
    "Corporate": ReportTheme(
        name="Corporate",
        description="Brand-forward navy and blue presentation.",
        page_background="FFFFFF",
        surface="FFFFFF",
        surface_alt="F4F7FB",
        title_background="102348",
        title_text="FFFFFF",
        accent="3867E8",
        accent_text="FFFFFF",
        accent_soft="EAF0FF",
        text="334155",
        muted="64748B",
        border="D9E2F1",
        success_soft="DFF4E5",
        warning_soft="FFF1D6",
        excel_table_style="TableStyleMedium2",
    ),
    "Dark": ReportTheme(
        name="Dark",
        description="High-contrast dark presentation for screen review.",
        page_background="111827",
        surface="1F2937",
        surface_alt="273449",
        title_background="0B1220",
        title_text="F8FAFC",
        accent="60A5FA",
        accent_text="0B1220",
        accent_soft="1E3A5F",
        text="F8FAFC",
        muted="CBD5E1",
        border="475569",
        success_soft="164E3B",
        warning_soft="5A3D12",
        excel_table_style="TableStyleMedium4",
    ),
}

REPORT_THEME_NAMES = tuple(REPORT_THEMES)
DEFAULT_REPORT_THEME = "Corporate"


def get_report_theme(name: str | None) -> ReportTheme:
    """Return a known theme or fail with a user-readable error."""

    selected = name or DEFAULT_REPORT_THEME
    if selected not in REPORT_THEMES:
        supported = ", ".join(REPORT_THEME_NAMES)
        raise ValueError(
            f"Unknown report theme '{selected}'. Supported themes: "
            f"{supported}."
        )
    return REPORT_THEMES[selected]
