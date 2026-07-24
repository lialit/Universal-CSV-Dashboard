import pytest

from app_core.report_themes import (
    DEFAULT_REPORT_THEME,
    REPORT_THEMES,
    REPORT_THEME_NAMES,
    get_report_theme,
)


def test_expected_report_themes_are_available():
    assert REPORT_THEME_NAMES == (
        "Light",
        "Corporate",
        "Dark",
    )
    assert set(REPORT_THEME_NAMES) == set(REPORT_THEMES)


def test_default_report_theme_is_corporate():
    theme = get_report_theme(None)

    assert DEFAULT_REPORT_THEME == "Corporate"
    assert theme.name == "Corporate"
    assert theme.title_background == "102348"


def test_unknown_report_theme_fails_safely():
    with pytest.raises(ValueError, match="Unknown report theme"):
        get_report_theme("Invisible")
