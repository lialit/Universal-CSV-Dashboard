from __future__ import annotations

from dataclasses import dataclass, replace
import math
from typing import Mapping

import pandas as pd

from app_core.quality import calculate_quality_score


@dataclass(frozen=True)
class BusinessInsight:
    """One traceable observation and its cautious interpretation."""

    insight_type: str
    title: str
    observation: str
    interpretation: str
    evidence: str
    limitation: str
    next_question: str
    confidence: str = "Moderate"
    confidence_reason: str = (
        "Reliability context has not been calculated."
    )


@dataclass(frozen=True)
class BusinessInsightsReport:
    """Evidence-linked insights for one configured dataframe."""

    insights: tuple[BusinessInsight, ...]
    questions: tuple[str, ...]
    limitations: tuple[str, ...]
    quality_score: float
    quality_status: str


def _configured_column(
    dataframe: pd.DataFrame,
    config: Mapping[str, object],
    key: str,
) -> str | None:
    value = config.get(key)
    if isinstance(value, str) and value in dataframe.columns:
        return value
    return None


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


def _confidence_context(
    valid_count: int,
    total_count: int,
    quality_score: float,
) -> tuple[str, str]:
    completeness = (
        valid_count / total_count
        if total_count
        else 0.0
    )

    if valid_count < 30 or completeness < 0.80 or quality_score < 60:
        label = "Low"
    else:
        score = 0
        score += 2 if valid_count >= 100 else 1
        score += 2 if completeness >= 0.98 else 1
        score += 2 if quality_score >= 90 else 1
        label = "High" if score == 6 else "Moderate"

    reason = (
        f"Based on {valid_count:,} usable values "
        f"({completeness:.1%} metric completeness) and a "
        f"{quality_score:.1f}/100 Data Quality Score."
    )
    return label, reason


def _time_insight(
    dataframe: pd.DataFrame,
    metric_column: str,
    date_column: str,
) -> BusinessInsight | None:
    prepared = pd.DataFrame(
        {
            "date": pd.to_datetime(
                dataframe[date_column],
                errors="coerce",
            ),
            "metric": pd.to_numeric(
                dataframe[metric_column],
                errors="coerce",
            ),
        }
    ).dropna()

    if prepared.empty:
        return None

    daily = (
        prepared.assign(date=prepared["date"].dt.normalize())
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
    if abs(change) < 0.10:
        return None

    direction = "higher" if change > 0 else "lower"
    interpretation = (
        "Recent performance is stronger than the earlier period."
        if change > 0
        else "Recent performance is weaker than the earlier period."
    )

    return BusinessInsight(
        insight_type="Trend",
        title="Material period change",
        observation=(
            f"Average daily {metric_column} in the second half is "
            f"{abs(change):.1%} {direction} than in the first half."
        ),
        interpretation=interpretation,
        evidence=(
            f"First-half daily average: {_format_number(first_average)}; "
            f"second-half: {_format_number(second_average)} across "
            f"{len(daily):,} days."
        ),
        limitation=(
            "This comparison describes the selected period only. It does "
            "not establish seasonality or explain what caused the change."
        ),
        next_question=(
            "Which dates or business segments contributed most to this change?"
        ),
    )


def _category_insight(
    dataframe: pd.DataFrame,
    metric_column: str,
    category_column: str,
) -> BusinessInsight | None:
    prepared = pd.DataFrame(
        {
            "category": dataframe[category_column].astype("string"),
            "metric": pd.to_numeric(
                dataframe[metric_column],
                errors="coerce",
            ),
        }
    ).dropna()

    if prepared.empty or (prepared["metric"] < 0).any():
        return None

    grouped = (
        prepared.groupby("category")["metric"]
        .sum()
        .sort_values(ascending=False)
    )
    total = float(grouped.sum())
    if grouped.empty or total <= 0:
        return None

    top_category = str(grouped.index[0])
    top_value = float(grouped.iloc[0])
    share = top_value / total

    if share >= 0.40:
        interpretation = (
            "Results are concentrated in one segment, so changes in that "
            "segment may have an outsized effect on the total."
        )
    else:
        interpretation = (
            "No single segment dominates the selected metric at the current "
            "40% concentration threshold."
        )

    return BusinessInsight(
        insight_type="Contribution",
        title="Leading category contribution",
        observation=(
            f"'{top_category}' contributes {share:.1%} of total "
            f"{metric_column}."
        ),
        interpretation=interpretation,
        evidence=(
            f"{_format_number(top_value)} from '{top_category}' out of "
            f"{_format_number(total)} across {len(grouped):,} categories."
        ),
        limitation=(
            "Contribution is based on summed values and does not account for "
            "segment size, margin, targets or other business context."
        ),
        next_question=(
            f"Is '{top_category}' large because of volume, performance or "
            "another underlying factor?"
        ),
    )


def _outlier_insight(
    dataframe: pd.DataFrame,
    metric_column: str,
) -> BusinessInsight | None:
    metric = pd.to_numeric(
        dataframe[metric_column],
        errors="coerce",
    ).dropna()

    if len(metric) < 8:
        return None

    first_quartile = float(metric.quantile(0.25))
    third_quartile = float(metric.quantile(0.75))
    iqr = third_quartile - first_quartile
    if iqr <= 0:
        return None

    lower_bound = first_quartile - 1.5 * iqr
    upper_bound = third_quartile + 1.5 * iqr
    outliers = metric[(metric < lower_bound) | (metric > upper_bound)]
    if outliers.empty:
        return None

    share = len(outliers) / len(metric)
    return BusinessInsight(
        insight_type="Anomaly",
        title="Unusual metric values",
        observation=(
            f"{len(outliers):,} {metric_column} values ({share:.1%}) fall "
            "outside the standard 1.5×IQR range."
        ),
        interpretation=(
            "These rows deserve review because they may represent exceptional "
            "events, data issues or legitimately extreme performance."
        ),
        evidence=(
            f"Expected IQR range: {_format_number(lower_bound)} to "
            f"{_format_number(upper_bound)}; observed range: "
            f"{_format_number(float(metric.min()))} to "
            f"{_format_number(float(metric.max()))}."
        ),
        limitation=(
            "IQR is a statistical screening rule. A flagged value is not "
            "automatically an error or a harmful business event."
        ),
        next_question=(
            "Do the flagged rows share a date, category or operational event?"
        ),
    )


def _correlation_insight(
    dataframe: pd.DataFrame,
    config: Mapping[str, object],
    metric_column: str,
) -> BusinessInsight | None:
    numeric_columns = [
        column
        for column in (config.get("numeric_columns") or [])
        if isinstance(column, str) and column in dataframe.columns
    ]
    numeric_columns = list(
        dict.fromkeys([metric_column, *numeric_columns])
    )

    if len(numeric_columns) < 2:
        return None

    numeric = dataframe[numeric_columns].apply(
        pd.to_numeric,
        errors="coerce",
    )
    correlations = numeric.corr()[metric_column].drop(
        labels=[metric_column],
        errors="ignore",
    ).dropna()

    if correlations.empty:
        return None

    related_column = str(correlations.abs().idxmax())
    coefficient = float(correlations[related_column])
    if abs(coefficient) < 0.50:
        return None

    direction = "positive" if coefficient > 0 else "negative"
    paired_rows = int(
        numeric[[metric_column, related_column]].dropna().shape[0]
    )

    return BusinessInsight(
        insight_type="Relationship",
        title="Strong numeric association",
        observation=(
            f"'{related_column}' has a {direction} correlation of "
            f"{coefficient:.2f} with {metric_column}."
        ),
        interpretation=(
            "The two fields tend to move together in the selected data and "
            "may be useful for further investigation."
        ),
        evidence=(
            f"Pearson correlation calculated from {paired_rows:,} rows with "
            "both values present."
        ),
        limitation=(
            "Correlation does not prove causation and may reflect shared "
            "drivers, time effects, aggregation or chance."
        ),
        next_question=(
            f"Does the relationship between '{related_column}' and "
            f"{metric_column} remain after controlling for date or category?"
        ),
    )


def build_business_insights(
    dataframe: pd.DataFrame,
    config: Mapping[str, object],
) -> BusinessInsightsReport:
    """Generate cautious, evidence-linked observations."""

    quality = calculate_quality_score(dataframe)
    metric_column = _configured_column(
        dataframe,
        config,
        "metric_column",
    )
    if metric_column is None:
        return BusinessInsightsReport(
            insights=(),
            questions=(
                "Which numeric column represents the primary business metric?",
            ),
            limitations=(
                "A valid primary metric is required before insights can be "
                "calculated.",
            ),
            quality_score=quality.score,
            quality_status=quality.status,
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
    metric = pd.to_numeric(
        dataframe[metric_column],
        errors="coerce",
    )
    insights: list[BusinessInsight] = []
    limitations: list[str] = []

    if date_column:
        time_insight = _time_insight(
            dataframe,
            metric_column,
            date_column,
        )
        if time_insight:
            insights.append(time_insight)
    else:
        limitations.append(
            "Trend and period-change insights require a configured date column."
        )

    if category_column:
        category_insight = _category_insight(
            dataframe,
            metric_column,
            category_column,
        )
        if category_insight:
            insights.append(category_insight)
    else:
        limitations.append(
            "Contribution insights require a configured category column."
        )

    outlier_insight = _outlier_insight(
        dataframe,
        metric_column,
    )
    if outlier_insight:
        insights.append(outlier_insight)

    correlation_insight = _correlation_insight(
        dataframe,
        config,
        metric_column,
    )
    if correlation_insight:
        insights.append(correlation_insight)

    missing_metric = int(metric.isna().sum())
    if missing_metric:
        limitations.append(
            f"{missing_metric:,} rows have no usable '{metric_column}' value "
            "and are excluded from numerical calculations."
        )

    if len(metric.dropna()) < 30:
        limitations.append(
            "The current sample contains fewer than 30 usable metric values; "
            "patterns may be unstable."
        )

    confidence, confidence_reason = _confidence_context(
        valid_count=int(metric.notna().sum()),
        total_count=len(metric),
        quality_score=quality.score,
    )
    insights = [
        replace(
            insight,
            confidence=confidence,
            confidence_reason=confidence_reason,
        )
        for insight in insights
    ]

    questions = tuple(
        dict.fromkeys(
            insight.next_question for insight in insights
        )
    )
    if not questions:
        questions = (
            "Would a different metric, date range or category reveal a more "
            "material pattern?",
        )

    return BusinessInsightsReport(
        insights=tuple(insights),
        questions=questions,
        limitations=tuple(dict.fromkeys(limitations)),
        quality_score=quality.score,
        quality_status=quality.status,
    )
