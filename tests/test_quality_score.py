import pandas as pd

from app_core.quality import (
    calculate_quality_score,
    quality_checks_table,
    quality_summary,
)


def test_complete_dataset_scores_100() -> None:
    dataframe = pd.DataFrame(
        {
            "date": pd.to_datetime(
                ["2026-01-01", "2026-01-02"]
            ),
            "sales": [10.0, 20.0],
            "region": ["North", "South"],
        }
    )

    report = calculate_quality_score(dataframe)

    assert report.score == 100.0
    assert report.status == "Excellent"
    assert report.issue_count == 0


def test_missing_cell_reduces_completeness_component() -> None:
    dataframe = pd.DataFrame(
        {
            "sales": [10.0, None],
            "region": ["North", "South"],
        }
    )

    report = calculate_quality_score(dataframe)

    assert report.missing_cells == 1
    assert report.checks[0].score == 75.0
    assert report.score == 87.5
    assert report.status == "Good"


def test_duplicate_row_reduces_duplicate_component() -> None:
    dataframe = pd.DataFrame(
        {
            "sales": [10, 10],
            "region": ["North", "North"],
        }
    )

    report = calculate_quality_score(dataframe)

    assert report.duplicate_rows == 1
    assert report.checks[1].score == 50.0
    assert report.score == 85.0


def test_non_finite_numeric_value_reduces_type_validity() -> None:
    dataframe = pd.DataFrame(
        {"sales": [10.0, float("inf")]}
    )

    report = calculate_quality_score(dataframe)

    assert report.invalid_type_cells == 1
    assert report.checks[2].score == 50.0
    assert report.score == 90.0


def test_empty_dataset_is_critical() -> None:
    dataframe = pd.DataFrame(columns=["sales", "region"])

    report = calculate_quality_score(dataframe)

    assert report.score == 0.0
    assert report.status == "Critical"


def test_tables_expose_scoring_and_column_details() -> None:
    dataframe = pd.DataFrame(
        {
            "sales": [10.0, None],
            "region": ["North", "South"],
        }
    )
    report = calculate_quality_score(dataframe)

    checks = quality_checks_table(report)
    columns = quality_summary(dataframe)

    assert checks["Weight"].sum() == 1.0
    assert set(checks["Check"]) == {
        "Completeness",
        "Duplicate-free rows",
        "Type validity",
    }
    assert "Invalid type values" in columns.columns
    assert "Status" in columns.columns
