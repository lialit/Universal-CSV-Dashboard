from io import BytesIO

import pandas as pd
from pypdf import PdfReader
import pytest

from app_core.pdf_exports import build_pdf_report


def sample_dataframe() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "date": pd.date_range("2026-01-01", periods=40),
            "region": ["North", "South"] * 20,
            "sales": [float(index + 1) for index in range(40)],
            "orders": [float(index + 1) for index in range(40)],
        }
    )


def sample_config() -> dict:
    return {
        "date_column": "date",
        "category_column": "region",
        "metric_column": "sales",
        "numeric_columns": ["sales", "orders"],
        "aggregation": "Sum",
    }


def pdf_reader(
    dataframe=None,
    config=None,
    source_name="sample.csv",
    theme_name="Corporate",
):
    content = build_pdf_report(
        dataframe if dataframe is not None else sample_dataframe(),
        config if config is not None else sample_config(),
        source_name,
        theme_name,
    )
    return content, PdfReader(BytesIO(content))


def extracted_text(reader: PdfReader) -> str:
    return "\n".join(
        page.extract_text() or ""
        for page in reader.pages
    )


def test_pdf_has_valid_signature_and_multiple_pages():
    content, reader = pdf_reader()

    assert content.startswith(b"%PDF-")
    assert content.rstrip().endswith(b"%%EOF")
    assert len(reader.pages) >= 3


def test_pdf_contains_source_and_metric_context():
    _, reader = pdf_reader()
    text = extracted_text(reader)

    assert "sample.csv" in text
    assert "Primary metric" in text
    assert "sales" in text


def test_pdf_contains_quality_context():
    _, reader = pdf_reader()
    text = extracted_text(reader)

    assert "Data Quality Score" in text
    assert "Detected issues" in text


def test_pdf_contains_insights_and_confidence():
    _, reader = pdf_reader()
    text = extracted_text(reader)

    assert "What deserves attention" in text
    assert "confidence" in text.lower()
    assert "Evidence:" in text
    assert "Limitation:" in text


def test_pdf_contains_responsible_methodology():
    _, reader = pdf_reader()
    text = extracted_text(reader)

    assert "Methodology and responsible use" in text
    assert "Correlation does not prove causation" in text


def test_pdf_supports_unicode_source_names():
    content, reader = pdf_reader(
        source_name="продажі_липень.csv",
    )

    assert content.startswith(b"%PDF-")
    assert len(reader.pages) >= 3


def test_invalid_metric_fails_safely():
    with pytest.raises(ValueError, match="primary metric"):
        build_pdf_report(
            sample_dataframe(),
            {"metric_column": "unknown"},
        )


def test_all_report_themes_are_embedded_in_pdf_metadata():
    for theme_name in ("Light", "Corporate", "Dark"):
        content, reader = pdf_reader(theme_name=theme_name)
        text = extracted_text(reader)

        assert content.startswith(b"%PDF-")
        assert "Report theme" in text
        assert theme_name in text
