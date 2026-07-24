from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Mapping

import pandas as pd

from app_core.quality import calculate_quality_score


@dataclass(frozen=True)
class SummaryStatement:
    """One evidence-linked statement in the executive summary."""

    title: str
    text: str
    evidence: str


@dataclass(frozen=True)
class ExecutiveSummary:
    """Rule-based overview of a configured dataset."""

    headline: str
    facts: tuple[SummaryStatement, ...]
    interpretations: tuple[SummaryStatement, ...]
    limitations: tuple[SummaryStatement, ...]
    next_steps: tuple[str, ...]


def _format_number(value: float) -> str:
    if not math.isfinite(value):
        return "—"

    absolute = abs(value)

    if absolute >= 1_000_000_000:
        return f"{value / 1_000_000_000:.1f}B"
    if absolute >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"
    if absolute >= 1_000:
        return f"{value / 1_000:.1f}K"

    return f"{value:,.2f}".rstrip("0").rstrip(".")


def _configured_column(
    dataframe: pd.DataFrame,
    config: Mapping[str, object],
    key: str,
) -> str | None:
    value = config.get(key)

    if isinstance(value, str) and value in dataframe.columns:
        return value

    return None


def _metric_series(
    dataframe: pd.DataFrame,
    metric_column: str,
) -> pd.Series:
    return pd.to_numeric(
        dataframe[metric_column],
        errors="coerce",
    )


def _date_fact(
    dataframe: pd.DataFrame,
    date_column: str,
) -> SummaryStatement | None:
    dates = pd.to_datetime(
        dataframe[date_column],
        errors="coerce",
    ).dropna()

    if dates.empty:
        return None

    start = dates.min()
    end = dates.max()
    distinct_days = int(dates.dt.normalize().nunique())

    return SummaryStatement(
        title="Date coverage",
        text=(
            f"The data runs from {start:%Y-%m-%d} to "
            f"{end:%Y-%m-%d} across {distinct_days:,} distinct days."
        ),
        evidence=(
            f"Minimum and maximum valid values in '{date_column}'."
        ),
    )


def _category_fact(
    dataframe: pd.DataFrame,
    category_column: str,
) -> SummaryStatement | None:
    categories = dataframe[category_column].dropna().astype("string")

    if categories.empty:
        return None

    counts = categories.value_counts()
    top_category = str(counts.index[0])
    top_count = int(counts.iloc[0])
    share = top_count / len(categories)

    return SummaryStatement(
        title="Category coverage",
        text=(
            f"'{category_column}' contains {len(counts):,} unique values. "
            f"The most frequent value is '{top_category}' "
            f"({top_count:,} rows, {share:.1%})."
        ),
        evidence=(
            f"Non-null value counts in '{category_column}'."
        ),
    )


def _distribution_interpretation(
    metric: pd.Series,
    metric_column: str,
) -> SummaryStatement | None:
    valid = metric.dropna()

    if len(valid) < 5:
        return None

    average = float(valid.mean())
    median = float(valid.median())
    scale = max(abs(median), abs(average), 1e-12)
    difference = (average - median) / scale

    if abs(difference) < 0.25:
        return None

    direction = "above" if difference > 0 else "below"

    return SummaryStatement(
        title="Uneven metric distribution",
        text=(
            f"The average {metric_column} is materially {direction} "
            "the median. A relatively small number of extreme values may "
            "be influencing the average."
        ),
        evidence=(
            f"Average: {_format_number(average)}; "
            f"median: {_format_number(median)}."
        ),
    )


def _category_interpretation(
    dataframe: pd.DataFrame,
    metric: pd.Series,
    metric_column: str,
    category_column: str,
) -> SummaryStatement | None:
    prepared = pd.DataFrame(
        {
            "category": dataframe[category_column].astype("string"),
            "metric": metric,
        }
    ).dropna()

    if prepared.empty or (prepared["metric"] < 0).any():
        return None

    grouped = (
        prepared.groupby("category", dropna=False)["metric"]
        .sum()
        .sort_values(ascending=False)
    )
    total = float(grouped.sum())

    if grouped.empty or total <= 0:
        return None

    top_category = str(grouped.index[0])
    top_value = float(grouped.iloc[0])
    share = top_value / total

    if share < 0.40:
        return None

    return SummaryStatement(
        title="Category concentration",
        text=(
            f"'{top_category}' contributes {share:.1%} of total "
            f"{metric_column}. Results may be concentrated in one segment."
        ),
        evidence=(
            f"{_format_number(top_value)} of "
            f"{_format_number(total)} total {metric_column}."
        ),
    )


def _time_interpretation(
    dataframe: pd.DataFrame,
    metric: pd.Series,
    metric_column: str,
    date_column: str,
) -> SummaryStatement | None:
    prepared = pd.DataFrame(
        {
            "date": pd.to_datetime(
                dataframe[date_column],
                errors="coerce",
            ),
            "metric": metric,
        }
    ).dropna()

    if prepared.empty:
        return None

    daily = (
        prepared.assign(
            date=prepared["date"].dt.normalize()
        )
        .groupby("date")["metric"]
        .sum()
        .sort_index()
    )

    if len(daily) < 6:
        return None

    midpoint = len(daily) // 2
    first_average = float(daily.iloc[:midpoint].mean())
    second_average = float(daily.iloc[midpoint:].mean())

    if abs(first_average) < 1e-12:
        return None

    change = (second_average - first_average) / abs(first_average)

    if abs(change) < 0.20:
        return None

    direction = "higher" if change > 0 else "lower"

    return SummaryStatement(
        title="Period comparison",
        text=(
            f"Average daily {metric_column} in the second half of the "
            f"selected period is {abs(change):.1%} {direction} than in "
            "the first half."
        ),
        evidence=(
            f"First-half daily average: "
            f"{_format_number(first_average)}; second-half: "
            f"{_format_number(second_average)}."
        ),
    )


def build_executive_summary(
    dataframe: pd.DataFrame,
    config: Mapping[str, object],
) -> ExecutiveSummary:
    """Build a transparent summary from observable dataset evidence."""

    rows, columns = dataframe.shape
    metric_column = _configured_column(
        dataframe,
        config,
        "metric_column",
    )
    date_column = _configured_column(
        dataframe,
        config,
        "date_column",
    )
    category_column = _configured_column(
        dataframe,
        config,
        "category_column",
    )
    quality = calculate_quality_score(dataframe)

    facts: list[SummaryStatement] = [
        SummaryStatement(
            title="Dataset structure",
            text=(
                f"The current selection contains {rows:,} rows and "
                f"{columns:,} columns."
            ),
            evidence="Dataframe shape after the active filters.",
        ),
        SummaryStatement(
            title="Technical quality",
            text=(
                f"The rule-based Data Quality Score is "
                f"{quality.score:.1f}/100 ({quality.status})."
            ),
            evidence=(
                f"{quality.missing_cells:,} missing cells, "
                f"{quality.duplicate_rows:,} duplicate rows and "
                f"{quality.invalid_type_cells:,} invalid-type cells."
            ),
        ),
    ]
    interpretations: list[SummaryStatement] = []
    limitations: list[SummaryStatement] = []
    next_steps: list[str] = []

    if metric_column is None:
        limitations.append(
            SummaryStatement(
                title="Primary metric unavailable",
                text=(
                    "A reliable metric summary cannot be generated until "
                    "a valid primary metric is selected."
                ),
                evidence="No configured metric column exists in the data.",
            )
        )

        return ExecutiveSummary(
            headline=(
                f"{rows:,} rows were loaded, but the primary metric "
                "configuration needs attention."
            ),
            facts=tuple(facts),
            interpretations=(),
            limitations=tuple(limitations),
            next_steps=(
                "Return to Upload & Configure and select a primary metric.",
            ),
        )

    metric = _metric_series(dataframe, metric_column)
    valid_metric = metric.dropna()
    missing_metric = int(metric.isna().sum())

    if valid_metric.empty:
        limitations.append(
            SummaryStatement(
                title="Metric contains no usable values",
                text=(
                    f"'{metric_column}' cannot support numerical analysis "
                    "in the current selection."
                ),
                evidence=(
                    f"0 of {rows:,} values parsed as numeric."
                ),
            )
        )
    else:
        total = float(valid_metric.sum())
        average = float(valid_metric.mean())
        median = float(valid_metric.median())

        facts.append(
            SummaryStatement(
                title="Primary metric",
                text=(
                    f"Total {metric_column} is {_format_number(total)}, "
                    f"with an average of {_format_number(average)} and "
                    f"a median of {_format_number(median)}."
                ),
                evidence=(
                    f"{len(valid_metric):,} numeric values in "
                    f"'{metric_column}'."
                ),
            )
        )

        distribution = _distribution_interpretation(
            metric,
            metric_column,
        )
        if distribution:
            interpretations.append(distribution)

    if date_column:
        date_fact = _date_fact(dataframe, date_column)
        if date_fact:
            facts.append(date_fact)

        if not valid_metric.empty:
            time_interpretation = _time_interpretation(
                dataframe,
                metric,
                metric_column,
                date_column,
            )
            if time_interpretation:
                interpretations.append(time_interpretation)

        next_steps.append(
            "Review the time-series chart for peaks, gaps and changes."
        )
    else:
        limitations.append(
            SummaryStatement(
                title="No date dimension",
                text=(
                    "Time trends and period comparisons are not available."
                ),
                evidence="No valid date column is configured.",
            )
        )

    if category_column:
        category_fact = _category_fact(
            dataframe,
            category_column,
        )
        if category_fact:
            facts.append(category_fact)

        if not valid_metric.empty:
            category_interpretation = _category_interpretation(
                dataframe,
                metric,
                metric_column,
                category_column,
            )
            if category_interpretation:
                interpretations.append(category_interpretation)

        next_steps.append(
            f"Compare {metric_column} across '{category_column}' values."
        )
    else:
        limitations.append(
            SummaryStatement(
                title="No category dimension",
                text=(
                    "Segment-level comparisons are not available."
                ),
                evidence="No valid category column is configured.",
            )
        )

    if missing_metric:
        limitations.append(
            SummaryStatement(
                title="Incomplete primary metric",
                text=(
                    f"{missing_metric:,} rows are excluded from numerical "
                    f"summaries of '{metric_column}'."
                ),
                evidence=(
                    f"{missing_metric:,} values did not contain a valid "
                    "number."
                ),
            )
        )

    if quality.score < 90:
        limitations.append(
            SummaryStatement(
                title="Data quality requires review",
                text=(
                    "Technical quality issues may affect the reliability "
                    "of the summary."
                ),
                evidence=(
                    f"Data Quality Score: {quality.score:.1f}/100."
                ),
            )
        )
        next_steps.append(
            "Open Data Quality and review the detected issues."
        )

    if rows < 30:
        limitations.append(
            SummaryStatement(
                title="Small sample",
                text=(
                    "Patterns in this selection may not be stable or "
                    "representative."
                ),
                evidence=f"Only {rows:,} rows are currently selected.",
            )
        )

    next_steps.append(
        "Confirm that the selected metric, dimensions and aggregation "
        "match the business question."
    )

    return ExecutiveSummary(
        headline=(
            f"{rows:,} rows were analyzed with '{metric_column}' as the "
            f"primary metric. Technical quality is "
            f"{quality.status.lower()} ({quality.score:.1f}/100)."
        ),
        facts=tuple(facts),
        interpretations=tuple(interpretations),
        limitations=tuple(limitations),
        next_steps=tuple(dict.fromkeys(next_steps)),
    )
