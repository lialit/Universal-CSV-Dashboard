import pandas as pd

from app_core.insights import build_business_insights


def configured_dataframe(rows: int) -> tuple[pd.DataFrame, dict]:
    dataframe = pd.DataFrame(
        {
            "date": pd.date_range("2026-01-01", periods=rows),
            "region": ["North", "South"] * (rows // 2)
            + (["North"] if rows % 2 else []),
            "sales": [float(index + 1) for index in range(rows)],
            "orders": [float(index + 1) for index in range(rows)],
        }
    )
    config = {
        "date_column": "date",
        "category_column": "region",
        "metric_column": "sales",
        "numeric_columns": ["sales", "orders"],
    }
    return dataframe, config


def test_large_complete_dataset_gets_high_confidence():
    dataframe, config = configured_dataframe(120)

    report = build_business_insights(dataframe, config)

    assert report.insights
    assert all(
        insight.confidence == "High"
        for insight in report.insights
    )


def test_medium_dataset_gets_moderate_confidence():
    dataframe, config = configured_dataframe(40)

    report = build_business_insights(dataframe, config)

    assert report.insights
    assert all(
        insight.confidence == "Moderate"
        for insight in report.insights
    )


def test_small_dataset_is_capped_at_low_confidence():
    dataframe, config = configured_dataframe(10)

    report = build_business_insights(dataframe, config)

    assert report.insights
    assert all(
        insight.confidence == "Low"
        for insight in report.insights
    )


def test_low_metric_completeness_is_low_confidence():
    dataframe, config = configured_dataframe(120)
    dataframe.loc[:29, "sales"] = None

    report = build_business_insights(dataframe, config)

    assert report.insights
    assert all(
        insight.confidence == "Low"
        for insight in report.insights
    )


def test_confidence_reason_exposes_inputs():
    dataframe, config = configured_dataframe(40)

    report = build_business_insights(dataframe, config)
    reason = report.insights[0].confidence_reason

    assert "40 usable values" in reason
    assert "100.0% metric completeness" in reason
    assert "Data Quality Score" in reason


def test_report_exposes_data_quality_context():
    dataframe, config = configured_dataframe(40)

    report = build_business_insights(dataframe, config)

    assert report.quality_score == 100.0
    assert report.quality_status == "Excellent"


def test_invalid_metric_still_returns_quality_context():
    dataframe, _ = configured_dataframe(10)

    report = build_business_insights(
        dataframe,
        {"metric_column": "unknown"},
    )

    assert report.insights == ()
    assert report.quality_score == 100.0
    assert report.quality_status == "Excellent"
