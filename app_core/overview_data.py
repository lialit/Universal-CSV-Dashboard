"""Data preparation helpers for the Executive Overview page."""

from dataclasses import dataclass
from datetime import date

from app_core.metrics import recent_metric_series, summarize_metric
from app_core.recommendations import recommend_analysis


@dataclass(frozen=True)
class OverviewKpis:
    selected: tuple[str, ...]
    values: dict[str, float | int]
    sparkline: object


def date_bounds(dataframe, date_column: str | None):
    if not date_column:
        return None
    valid_dates = dataframe[date_column].dropna()
    if valid_dates.empty:
        return None
    return valid_dates.min().date(), valid_dates.max().date()


def category_options(
    dataframe,
    category_column: str | None,
) -> tuple[str, ...]:
    if not category_column:
        return ()
    return tuple(
        sorted(
            dataframe[category_column]
            .astype("string")
            .dropna()
            .unique()
            .tolist()
        )
    )


def date_filter_is_full_range(
    selected_dates: tuple[date, date],
    bounds: tuple[date, date],
) -> bool:
    return selected_dates == bounds


def category_filter_is_full_range(
    selected_categories,
    available_categories,
) -> bool:
    return tuple(selected_categories) == tuple(available_categories)


def build_overview_kpis(dataframe, config, metric: str) -> OverviewKpis:
    metric_summary = summarize_metric(dataframe, metric)
    sparkline = recent_metric_series(
        dataframe,
        config.get("date_column"),
        metric,
    )
    fallback = recommend_analysis(dataframe, config)
    selected = (
        config["kpi_cards"]
        if "kpi_cards" in config
        else list(fallback.kpis)
    )

    values = {
        "Total": metric_summary.total,
        "Average": metric_summary.average,
        "Median": metric_summary.median,
        "Minimum": metric_summary.minimum,
        "Maximum": metric_summary.maximum,
        "Non-null count": metric_summary.non_null_count,
    }
    selected = tuple(item for item in selected if item in values)[:3]
    return OverviewKpis(
        selected=selected,
        values=values,
        sparkline=sparkline,
    )
