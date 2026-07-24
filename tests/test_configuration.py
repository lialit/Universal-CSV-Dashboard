import json

from app_core.configuration import (
    CONFIG_SCHEMA_VERSION,
    configuration_for_export,
    validate_configuration,
)


COLUMNS = ["date", "region", "sales", "orders"]


def saved_configuration() -> dict:
    return {
        "schema_version": 1,
        "source_columns": COLUMNS,
        "date_column": "date",
        "metric_column": "sales",
        "numeric_columns": ["sales", "orders"],
        "category_column": "region",
        "aggregation": "Sum",
        "report_theme": "Dark",
        "kpi_cards": ["Total", "Average"],
        "chart_types": ["Time series", "Distribution"],
    }


def test_valid_configuration_is_restored():
    result = validate_configuration(
        json.dumps(saved_configuration()).encode(),
        COLUMNS,
    )

    assert result.is_valid
    assert result.config["metric_column"] == "sales"
    assert result.config["numeric_columns"] == ["sales", "orders"]
    assert result.config["report_theme"] == "Dark"
    assert result.errors == ()


def test_missing_primary_metric_fails_safely():
    result = validate_configuration(
        saved_configuration(),
        ["date", "region", "orders"],
    )

    assert not result.is_valid
    assert result.config == {}
    assert "primary metric" in result.errors[0]


def test_missing_optional_columns_are_cleared():
    result = validate_configuration(
        saved_configuration(),
        ["sales", "orders"],
    )

    assert result.is_valid
    assert result.config["date_column"] is None
    assert result.config["category_column"] is None
    assert result.warnings


def test_invalid_json_returns_readable_error():
    result = validate_configuration(b"{not-json}", COLUMNS)

    assert not result.is_valid
    assert "valid UTF-8 JSON" in result.errors[0]


def test_newer_schema_version_is_rejected():
    config = saved_configuration()
    config["schema_version"] = CONFIG_SCHEMA_VERSION + 1

    result = validate_configuration(config, COLUMNS)

    assert not result.is_valid
    assert "newer than" in result.errors[0]


def test_unsupported_selections_are_removed():
    config = saved_configuration()
    config["kpi_cards"].append("Magic KPI")
    config["chart_types"].append("Causal chart")

    result = validate_configuration(config, COLUMNS)

    assert result.is_valid
    assert "Magic KPI" not in result.config["kpi_cards"]
    assert "Causal chart" not in result.config["chart_types"]
    assert len(result.warnings) == 2


def test_export_includes_version_and_source_schema():
    runtime = {
        "metric_column": "sales",
        "aggregation": "Sum",
    }

    exported = configuration_for_export(runtime, COLUMNS)

    assert exported["schema_version"] == CONFIG_SCHEMA_VERSION
    assert exported["source_columns"] == COLUMNS
    assert exported["metric_column"] == "sales"


def test_unsupported_report_theme_uses_safe_default():
    config = saved_configuration()
    config["report_theme"] = "Invisible"

    result = validate_configuration(config, COLUMNS)

    assert result.is_valid
    assert result.config["report_theme"] == "Corporate"
    assert any("report theme" in warning for warning in result.warnings)
