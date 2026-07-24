import json

import pandas as pd

from app_core.project_state import (
    PROJECT_FORMAT,
    PROJECT_SCHEMA_VERSION,
    build_project_state,
    is_project_state,
    project_state_to_json,
    validate_project_state,
)


def sample_dataframe() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "date": pd.date_range("2026-01-01", periods=4),
            "region": ["North", "South", "North", "South"],
            "sales": [100.0, 120.0, 115.0, 130.0],
            "orders": [10, 12, 11, 13],
        }
    )


def sample_config() -> dict:
    return {
        "date_column": "date",
        "metric_column": "sales",
        "numeric_columns": ["sales", "orders"],
        "category_column": "region",
        "aggregation": "Sum",
        "kpi_cards": ["Total", "Average"],
        "chart_types": ["Time series", "Distribution"],
    }


def sample_project() -> dict:
    return build_project_state(
        sample_dataframe(),
        sample_config(),
        "retail_липень.csv",
    )


def test_project_contains_configuration_but_not_raw_data():
    project = sample_project()

    assert project["format"] == PROJECT_FORMAT
    assert project["configuration"]["metric_column"] == "sales"
    assert project["privacy"]["contains_raw_data"] is False
    assert "data" not in project
    assert "records" not in project


def test_project_json_is_readable_and_supports_unicode():
    content = project_state_to_json(
        sample_dataframe(),
        sample_config(),
        "продажі_липень.csv",
    )
    parsed = json.loads(content)

    assert parsed["source"]["file_name"] == "продажі_липень.csv"
    assert is_project_state(content)


def test_valid_project_restores_runtime_configuration():
    result = validate_project_state(
        sample_project(),
        sample_dataframe(),
        "retail_липень.csv",
    )

    assert result.is_valid
    assert result.config["metric_column"] == "sales"
    assert result.config["numeric_columns"] == ["sales", "orders"]
    assert result.errors == ()


def test_different_source_name_and_row_count_are_visible_warnings():
    dataframe = pd.concat(
        [sample_dataframe(), sample_dataframe().iloc[:1]],
        ignore_index=True,
    )
    result = validate_project_state(
        sample_project(),
        dataframe,
        "replacement.csv",
    )

    assert result.is_valid
    assert any("created for" in warning for warning in result.warnings)
    assert any("row count changed" in warning for warning in result.warnings)


def test_changed_column_type_is_visible_warning():
    dataframe = sample_dataframe()
    dataframe["orders"] = dataframe["orders"].astype(str)

    result = validate_project_state(
        sample_project(),
        dataframe,
        "retail_липень.csv",
    )

    assert result.is_valid
    assert any("column type" in warning for warning in result.warnings)


def test_missing_primary_metric_fails_safely():
    dataframe = sample_dataframe().drop(columns=["sales"])

    result = validate_project_state(
        sample_project(),
        dataframe,
        "retail_липень.csv",
    )

    assert not result.is_valid
    assert result.config == {}
    assert any("primary metric" in error for error in result.errors)


def test_newer_project_schema_is_rejected():
    project = sample_project()
    project["schema_version"] = PROJECT_SCHEMA_VERSION + 1

    result = validate_project_state(
        project,
        sample_dataframe(),
        "retail_липень.csv",
    )

    assert not result.is_valid
    assert any("newer than" in error for error in result.errors)


def test_non_project_json_is_rejected():
    result = validate_project_state(
        {"metric_column": "sales"},
        sample_dataframe(),
        "retail_липень.csv",
    )

    assert not result.is_valid
    assert "not a Universal CSV Dashboard project" in result.errors[0]
