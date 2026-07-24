import pandas as pd
import pytest

from app_core.calculation_explainer import (
    AVERAGE_CALCULATION,
    CATEGORY_SHARE_CALCULATION,
    CORRELATION_CALCULATION,
    MEDIAN_CALCULATION,
    OUTLIER_CALCULATION,
    PERIOD_CHANGE_CALCULATION,
    QUALITY_CALCULATION,
    TOTAL_CALCULATION,
    calculation_for_question,
    calculation_options,
    explain_calculation,
)


def sample_dataframe() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "date": pd.date_range("2026-01-01", periods=10),
            "region": ["North"] * 8 + ["South"] * 2,
            "sales": [10.0] * 5 + [20.0] * 4 + [100.0],
            "orders": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0],
        }
    )


def sample_config() -> dict[str, object]:
    return {
        "date_column": "date",
        "category_column": "region",
        "metric_column": "sales",
        "numeric_columns": ["sales", "orders"],
    }


@pytest.mark.parametrize(
    ("calculation_key", "expected_result"),
    [
        (TOTAL_CALCULATION, "230"),
        (AVERAGE_CALCULATION, "23"),
        (MEDIAN_CALCULATION, "15"),
    ],
)
def test_metric_calculations_are_transparent(
    calculation_key: str,
    expected_result: str,
) -> None:
    explanation = explain_calculation(
        sample_dataframe(),
        sample_config(),
        calculation_key,
    )

    assert explanation.result == expected_result
    assert explanation.included_rows == 10
    assert explanation.excluded_rows == 0
    assert explanation.formula
    assert explanation.steps


def test_quality_calculation_discloses_weights() -> None:
    explanation = explain_calculation(
        sample_dataframe(),
        sample_config(),
        QUALITY_CALCULATION,
    )

    assert explanation.result == "100.0/100 (Excellent)"
    assert "50%" in explanation.formula
    assert "30%" in explanation.formula
    assert "20%" in explanation.formula
    assert len(explanation.steps) == 3


def test_period_change_discloses_split_and_aggregation() -> None:
    explanation = explain_calculation(
        sample_dataframe(),
        sample_config(),
        PERIOD_CHANGE_CALCULATION,
    )

    assert explanation.result == "+260.0%"
    assert explanation.aggregation == (
        "Daily sum, then half-period mean"
    )
    assert any(
        "first half contains 5 dates" in step.detail
        for step in explanation.steps
    )


def test_category_share_names_leader_and_fields() -> None:
    explanation = explain_calculation(
        sample_dataframe(),
        sample_config(),
        CATEGORY_SHARE_CALCULATION,
    )

    assert explanation.result == "South: 52.2%"
    assert explanation.fields == ("region", "sales")
    assert "Sum by category" == explanation.aggregation


def test_outlier_calculation_shows_bounds() -> None:
    explanation = explain_calculation(
        sample_dataframe(),
        sample_config(),
        OUTLIER_CALCULATION,
    )

    assert explanation.result == "1 values (10.0%)"
    assert "1.5×IQR" in explanation.formula
    assert any(
        "flagged" in step.detail
        for step in explanation.steps
    )


def test_correlation_reports_pairwise_rows_and_limitation() -> None:
    explanation = explain_calculation(
        sample_dataframe(),
        sample_config(),
        CORRELATION_CALCULATION,
    )

    assert explanation.result.startswith("orders: r = ")
    assert explanation.included_rows == 10
    assert any(
        "does not prove causation" in limitation
        for limitation in explanation.limitations
    )


def test_missing_configuration_is_explained_safely() -> None:
    dataframe = sample_dataframe()[["sales"]]
    config = {
        "metric_column": "sales",
        "numeric_columns": ["sales"],
    }
    options = {
        option.key: option
        for option in calculation_options(dataframe, config)
    }

    assert not options[PERIOD_CHANGE_CALCULATION].available
    explanation = explain_calculation(
        dataframe,
        config,
        PERIOD_CHANGE_CALCULATION,
    )
    assert not explanation.available
    assert explanation.result == "Not available"
    assert "date column" in explanation.steps[0].detail


def test_question_mapping_selects_relevant_calculation() -> None:
    assert calculation_for_question("trend") == (
        PERIOD_CHANGE_CALCULATION
    )
    assert calculation_for_question("segment") == (
        CATEGORY_SHARE_CALCULATION
    )
    assert calculation_for_question("reliability") == (
        QUALITY_CALCULATION
    )


def test_unknown_calculation_is_rejected() -> None:
    with pytest.raises(ValueError, match="Unsupported calculation"):
        explain_calculation(
            sample_dataframe(),
            sample_config(),
            "invented",
        )
