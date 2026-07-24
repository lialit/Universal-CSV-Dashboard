import pandas as pd

from app_core.recommendations import (
    available_chart_options,
    recommend_analysis,
    recommendations_table,
)


def sample_dataframe() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "date": pd.date_range("2026-01-01", periods=4),
            "region": ["North", "South", "North", "West"],
            "sales": [10.0, 20.0, 30.0, 40.0],
            "orders": [1, 2, 3, 4],
        }
    )


def sample_config() -> dict:
    return {
        "date_column": "date",
        "category_column": "region",
        "metric_column": "sales",
        "numeric_columns": ["sales", "orders"],
    }


def test_all_chart_types_are_available_with_complete_config():
    options = available_chart_options(
        sample_dataframe(),
        sample_config(),
    )

    assert options == (
        "Time series",
        "Category comparison",
        "Distribution",
        "Correlation matrix",
    )


def test_default_recommendations_are_limited_to_three_charts():
    result = recommend_analysis(
        sample_dataframe(),
        sample_config(),
    )

    assert result.kpis == ("Total", "Average", "Median")
    assert result.charts == (
        "Time series",
        "Category comparison",
        "Distribution",
    )


def test_distribution_is_available_without_dimensions():
    dataframe = sample_dataframe()[["sales", "orders"]]
    config = {
        "metric_column": "sales",
        "numeric_columns": ["sales", "orders"],
    }

    assert available_chart_options(dataframe, config) == (
        "Distribution",
        "Correlation matrix",
    )


def test_correlation_requires_two_numeric_columns():
    dataframe = sample_dataframe()[["sales"]]
    config = {
        "metric_column": "sales",
        "numeric_columns": ["sales"],
    }

    assert available_chart_options(dataframe, config) == (
        "Distribution",
    )


def test_missing_metric_values_recommend_non_null_count():
    dataframe = sample_dataframe()
    dataframe.loc[1, "sales"] = None

    result = recommend_analysis(
        dataframe,
        sample_config(),
    )

    assert result.kpis == (
        "Total",
        "Average",
        "Non-null count",
    )


def test_invalid_metric_returns_empty_recommendations():
    result = recommend_analysis(
        sample_dataframe(),
        {"metric_column": "unknown"},
    )

    assert result.kpis == ()
    assert result.charts == ()
    assert result.available_charts == ()


def test_recommendations_table_explains_every_default():
    result = recommend_analysis(
        sample_dataframe(),
        sample_config(),
    )
    table = recommendations_table(result)

    assert len(table) == len(result.kpis) + len(result.charts)
    assert set(table.columns) == {
        "Type",
        "Recommended item",
        "Why it was selected",
    }
