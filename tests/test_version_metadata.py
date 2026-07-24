from io import BytesIO

from openpyxl import load_workbook
import pandas as pd
from pypdf import PdfReader

from app_core.exports import build_excel_report
from app_core.pdf_exports import build_pdf_report
from app_core.project_state import build_project_state
from app_core.version import PRODUCT_VERSION, __version__


def sample_dataframe() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "date": pd.date_range("2026-01-01", periods=4),
            "region": ["North", "South", "North", "South"],
            "sales": [100.0, 120.0, 115.0, 130.0],
        }
    )


def sample_config() -> dict[str, object]:
    return {
        "date_column": "date",
        "category_column": "region",
        "metric_column": "sales",
        "numeric_columns": ["sales"],
        "aggregation": "Sum",
    }


def test_version_is_single_release_candidate_value() -> None:
    assert PRODUCT_VERSION == __version__
    assert PRODUCT_VERSION == "1.0.0-rc.1"


def test_project_state_uses_canonical_product_version() -> None:
    project = build_project_state(
        sample_dataframe(),
        sample_config(),
        "sample.csv",
    )

    assert project["product_version"] == PRODUCT_VERSION


def test_excel_export_contains_canonical_product_version() -> None:
    content = build_excel_report(
        sample_dataframe(),
        sample_config(),
        "sample.csv",
    )
    workbook = load_workbook(BytesIO(content), data_only=False)

    assert workbook["Overview"]["E6"].value == "Product version"
    assert workbook["Overview"]["F6"].value == PRODUCT_VERSION


def test_pdf_export_contains_canonical_product_version() -> None:
    content = build_pdf_report(
        sample_dataframe(),
        sample_config(),
        "sample.csv",
    )
    reader = PdfReader(BytesIO(content))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)

    assert "Product version" in text
    assert PRODUCT_VERSION in text
