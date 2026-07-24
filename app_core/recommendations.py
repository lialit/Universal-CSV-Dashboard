from dataclasses import dataclass

import pandas as pd


KPI_OPTIONS = (
    "Total",
    "Average",
    "Median",
    "Minimum",
    "Maximum",
    "Non-null count",
)

CHART_OPTIONS = (
    "Time series",
    "Category comparison",
    "Distribution",
    "Correlation matrix",
)


@dataclass(frozen=True)
class RecommendationDetail:
    item: str
    kind: str
    reason: str


@dataclass(frozen=True)
class AnalysisRecommendations:
    kpis: tuple[str, ...]
    charts: tuple[str, ...]
    available_charts: tuple[str, ...]
    details: tuple[RecommendationDetail, ...]


def _valid_column(
    dataframe: pd.DataFrame,
    value: object,
) -> str | None:
    if isinstance(value, str) and value in dataframe.columns:
        return value
    return None


def available_chart_options(
    dataframe: pd.DataFrame,
    config: dict,
) -> tuple[str, ...]:
    metric = _valid_column(
        dataframe,
        config.get("metric_column"),
    )
    if metric is None:
        return ()

    available: list[str] = []

    if _valid_column(dataframe, config.get("date_column")):
        available.append("Time series")

    if _valid_column(
        dataframe,
        config.get("category_column"),
    ):
        available.append("Category comparison")

    available.append("Distribution")

    numeric_columns = [
        column
        for column in config.get("numeric_columns", [])
        if column in dataframe.columns
    ]
    numeric_columns = list(dict.fromkeys([metric, *numeric_columns]))

    if len(numeric_columns) >= 2:
        available.append("Correlation matrix")

    return tuple(available)


def recommend_analysis(
    dataframe: pd.DataFrame,
    config: dict,
) -> AnalysisRecommendations:
    metric = _valid_column(
        dataframe,
        config.get("metric_column"),
    )
    if metric is None:
        return AnalysisRecommendations((), (), (), ())

    series = pd.to_numeric(
        dataframe[metric],
        errors="coerce",
    )
    details: list[RecommendationDetail] = []

    kpis = ["Total", "Average", "Median"]
    details.extend(
        (
            RecommendationDetail(
                "Total",
                "KPI",
                f"Shows the overall scale of {metric}.",
            ),
            RecommendationDetail(
                "Average",
                "KPI",
                f"Shows the typical arithmetic level of {metric}.",
            ),
            RecommendationDetail(
                "Median",
                "KPI",
                "Adds a robust midpoint that is less sensitive to outliers.",
            ),
        )
    )

    if series.isna().any():
        kpis[-1] = "Non-null count"
        details[-1] = RecommendationDetail(
            "Non-null count",
            "KPI",
            (
                f"Highlights how many usable {metric} values remain "
                "after missing or invalid values are excluded."
            ),
        )

    available = available_chart_options(dataframe, config)
    charts: list[str] = []

    chart_reasons = {
        "Time series": (
            "A date column is available, so change over time can be inspected."
        ),
        "Category comparison": (
            "A category column is available, so groups can be compared."
        ),
        "Distribution": (
            f"Shows spread, skew and possible outliers in {metric}."
        ),
        "Correlation matrix": (
            "At least two numeric columns are available for relationship checks."
        ),
    }

    for chart in available:
        if len(charts) >= 3:
            break
        charts.append(chart)
        details.append(
            RecommendationDetail(
                chart,
                "Chart",
                chart_reasons[chart],
            )
        )

    return AnalysisRecommendations(
        tuple(kpis),
        tuple(charts),
        available,
        tuple(details),
    )


def recommendations_table(
    recommendations: AnalysisRecommendations,
) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "Type": detail.kind,
                "Recommended item": detail.item,
                "Why it was selected": detail.reason,
            }
            for detail in recommendations.details
        ]
    )
