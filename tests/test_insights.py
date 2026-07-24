import pandas as pd

from app_core.insights import build_business_insights


def base_config() -> dict:
    return {
        "date_column": "date",
        "category_column": "region",
        "metric_column": "sales",
        "numeric_columns": ["sales", "orders"],
    }


def test_detects_material_period_change():
    dataframe = pd.DataFrame(
        {
            "date": pd.date_range("2026-01-01", periods=10),
            "region": ["North", "South"] * 5,
            "sales": [10.0] * 5 + [20.0] * 5,
            "orders": list(range(1, 11)),
        }
    )

    report = build_business_insights(dataframe, base_config())

    trend = next(
        insight
        for insight in report.insights
        if insight.insight_type == "Trend"
    )
    assert "100.0% higher" in trend.observation
    assert "does not establish" in trend.limitation


def test_detects_leading_category_contribution():
    dataframe = pd.DataFrame(
        {
            "date": pd.date_range("2026-01-01", periods=10),
            "region": ["North"] * 8 + ["South"] * 2,
            "sales": [10.0] * 10,
            "orders": list(range(1, 11)),
        }
    )

    report = build_business_insights(dataframe, base_config())

    contribution = next(
        insight
        for insight in report.insights
        if insight.insight_type == "Contribution"
    )
    assert "'North' contributes 80.0%" in contribution.observation
    assert "concentrated" in contribution.interpretation


def test_detects_iqr_outlier():
    dataframe = pd.DataFrame(
        {
            "sales": [
                8.0,
                9.0,
                10.0,
                10.0,
                10.0,
                11.0,
                12.0,
                9.0,
                11.0,
                1000.0,
            ],
            "orders": list(range(1, 11)),
        }
    )
    config = {
        "metric_column": "sales",
        "numeric_columns": ["sales", "orders"],
    }

    report = build_business_insights(dataframe, config)

    anomaly = next(
        insight
        for insight in report.insights
        if insight.insight_type == "Anomaly"
    )
    assert "1 sales values" in anomaly.observation
    assert "not automatically an error" in anomaly.limitation


def test_detects_strong_numeric_correlation():
    dataframe = pd.DataFrame(
        {
            "sales": [10.0, 20.0, 30.0, 40.0, 50.0],
            "orders": [1.0, 2.0, 3.0, 4.0, 5.0],
        }
    )
    config = {
        "metric_column": "sales",
        "numeric_columns": ["sales", "orders"],
    }

    report = build_business_insights(dataframe, config)

    relationship = next(
        insight
        for insight in report.insights
        if insight.insight_type == "Relationship"
    )
    assert "1.00" in relationship.observation
    assert "does not prove causation" in relationship.limitation


def test_weak_correlation_is_not_reported():
    dataframe = pd.DataFrame(
        {
            "sales": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
            "orders": [1.0, 0.0, 1.0, 0.0, 1.0, 0.0],
        }
    )
    config = {
        "metric_column": "sales",
        "numeric_columns": ["sales", "orders"],
    }

    report = build_business_insights(dataframe, config)

    assert all(
        insight.insight_type != "Relationship"
        for insight in report.insights
    )


def test_invalid_metric_returns_safe_report():
    dataframe = pd.DataFrame({"sales": [1.0, 2.0]})

    report = build_business_insights(
        dataframe,
        {"metric_column": "unknown"},
    )

    assert report.insights == ()
    assert "valid primary metric" in report.limitations[0]


def test_missing_dimensions_are_reported_as_limitations():
    dataframe = pd.DataFrame(
        {"sales": [1.0, 2.0, 3.0, 4.0, 5.0]}
    )

    report = build_business_insights(
        dataframe,
        {
            "metric_column": "sales",
            "numeric_columns": ["sales"],
        },
    )

    assert any(
        "date column" in limitation
        for limitation in report.limitations
    )
    assert any(
        "category column" in limitation
        for limitation in report.limitations
    )
