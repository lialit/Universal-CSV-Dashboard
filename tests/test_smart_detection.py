import pandas as pd

from app_core.smart_detection import (
    detect_column,
    detect_dataset,
    normalize_name,
)


def sample_dataframe() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Order Date": [
                "2026-01-01",
                "2026-01-02",
                "2026-01-03",
            ],
            "Revenue": [1200, 1450, 980],
            "Region": ["North", "South", "North"],
            "Order ID": ["A1", "A2", "A3"],
            "Is Promo": [True, False, True],
            "Comment": [
                "Good result",
                "Average",
                "Strong growth",
            ],
        }
    )


def test_normalize_name() -> None:
    assert normalize_name("Order Date") == "order_date"
    assert normalize_name("customer-ID") == "customer_id"


def test_detect_dataset_roles() -> None:
    detection = detect_dataset(sample_dataframe())

    assert detection.date_column == "Order Date"
    assert detection.metric_column == "Revenue"
    assert detection.category_column == "Region"
    assert "Order ID" in detection.identifier_columns
    assert "Is Promo" in detection.boolean_columns


def test_revenue_is_metric() -> None:
    dataframe = sample_dataframe()
    result = detect_column(dataframe, "Revenue")

    assert result.role == "metric"
    assert result.confidence >= 0.8
