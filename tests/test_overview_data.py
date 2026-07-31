from datetime import date

import pandas as pd

from app_core.overview_data import (
    build_overview_kpis,
    category_filter_is_full_range,
    category_options,
    date_bounds,
    date_filter_is_full_range,
)


def sample_dataframe() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "date": pd.to_datetime(["2026-01-01", "2026-01-02"]),
            "region": ["South", "North"],
            "sales": [10, 20],
        }
    )


def test_filter_metadata_is_deterministic() -> None:
    dataframe = sample_dataframe()

    assert date_bounds(dataframe, "date") == (
        date(2026, 1, 1),
        date(2026, 1, 2),
    )
    assert category_options(dataframe, "region") == ("North", "South")


def test_full_range_filters_are_recognized_without_dataframe_copy() -> None:
    bounds = (date(2026, 1, 1), date(2026, 1, 2))

    assert date_filter_is_full_range(bounds, bounds)
    assert category_filter_is_full_range(
        ["North", "South"],
        ("North", "South"),
    )


def test_overview_kpis_are_built_once_as_reusable_payload() -> None:
    dataframe = sample_dataframe()
    config = {
        "date_column": "date",
        "metric_column": "sales",
        "numeric_columns": ["sales"],
        "kpi_cards": ["Total", "Average", "Median"],
    }

    payload = build_overview_kpis(dataframe, config, "sales")

    assert payload.selected == ("Total", "Average", "Median")
    assert payload.values["Total"] == 30
    assert payload.values["Average"] == 15
