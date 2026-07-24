from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Callable, Mapping

import pandas as pd

from app_core.quality import calculate_quality_score


TOTAL_CALCULATION = "total"
AVERAGE_CALCULATION = "average"
MEDIAN_CALCULATION = "median"
QUALITY_CALCULATION = "data_quality"
PERIOD_CHANGE_CALCULATION = "period_change"
CATEGORY_SHARE_CALCULATION = "category_share"
OUTLIER_CALCULATION = "outlier_screen"
CORRELATION_CALCULATION = "correlation"


@dataclass(frozen=True)
class CalculationOption:
    """One calculation the interface can explain."""

    key: str
    label: str
    available: bool
    availability_reason: str


@dataclass(frozen=True)
class CalculationStep:
    """One human-readable step in a transparent calculation."""

    label: str
    detail: str


@dataclass(frozen=True)
class CalculationExplanation:
    """A complete, auditable explanation of one calculation."""

    key: str
    title: str
    result: str
    formula: str
    fields: tuple[str, ...]
    aggregation: str
    included_rows: int
    excluded_rows: int
    steps: tuple[CalculationStep, ...]
    assumptions: tuple[str, ...]
    limitations: tuple[str, ...]
    available: bool = True


def _configured_column(
    dataframe: pd.DataFrame,
    config: Mapping[str, object],
    key: str,
) -> str | None:
    value = config.get(key)
    if isinstance(value, str) and value in dataframe.columns:
        return value
    return None


def _numeric_columns(
    dataframe: pd.DataFrame,
    config: Mapping[str, object],
) -> list[str]:
    metric = _configured_column(dataframe, config, "metric_column")
    columns = [
        column
        for column in (config.get("numeric_columns") or [])
        if isinstance(column, str) and column in dataframe.columns
    ]
    if metric:
        columns = [metric, *columns]
    return list(dict.fromkeys(columns))


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


def calculation_options(
    dataframe: pd.DataFrame,
    config: Mapping[str, object],
) -> tuple[CalculationOption, ...]:
    """Return all explainable calculations with availability context."""

    metric = _configured_column(dataframe, config, "metric_column")
    date = _configured_column(dataframe, config, "date_column")
    category = _configured_column(dataframe, config, "category_column")
    numeric_columns = _numeric_columns(dataframe, config)

    metric_reason = (
        "Available for the configured primary metric."
        if metric
        else "Select a valid primary metric."
    )
    return (
        CalculationOption(
            TOTAL_CALCULATION,
            "Total primary metric",
            metric is not None,
            metric_reason,
        ),
        CalculationOption(
            AVERAGE_CALCULATION,
            "Average primary metric",
            metric is not None,
            metric_reason,
        ),
        CalculationOption(
            MEDIAN_CALCULATION,
            "Median primary metric",
            metric is not None,
            metric_reason,
        ),
        CalculationOption(
            QUALITY_CALCULATION,
            "Data Quality Score",
            True,
            "Available from the current dataframe.",
        ),
        CalculationOption(
            PERIOD_CHANGE_CALCULATION,
            "First-half vs second-half change",
            metric is not None and date is not None,
            (
                "Available for the configured metric and date."
                if metric and date
                else "Configure both a metric and a date column."
            ),
        ),
        CalculationOption(
            CATEGORY_SHARE_CALCULATION,
            "Leading category contribution",
            metric is not None and category is not None,
            (
                "Available for the configured metric and category."
                if metric and category
                else "Configure both a metric and a category column."
            ),
        ),
        CalculationOption(
            OUTLIER_CALCULATION,
            "Unusual values (1.5×IQR)",
            metric is not None,
            metric_reason,
        ),
        CalculationOption(
            CORRELATION_CALCULATION,
            "Strongest numeric correlation",
            metric is not None and len(numeric_columns) >= 2,
            (
                "Available for at least two configured numeric fields."
                if metric and len(numeric_columns) >= 2
                else "Configure at least two numeric fields."
            ),
        ),
    )


def calculation_for_question(question_key: str) -> str:
    """Map an assistant question to its most relevant calculation."""

    mapping = {
        "overview": TOTAL_CALCULATION,
        "metric": TOTAL_CALCULATION,
        "trend": PERIOD_CHANGE_CALCULATION,
        "segment": CATEGORY_SHARE_CALCULATION,
        "anomaly": OUTLIER_CALCULATION,
        "relationship": CORRELATION_CALCULATION,
        "reliability": QUALITY_CALCULATION,
    }
    return mapping.get(question_key, TOTAL_CALCULATION)


def _unavailable_explanation(
    option: CalculationOption,
) -> CalculationExplanation:
    return CalculationExplanation(
        key=option.key,
        title=option.label,
        result="Not available",
        formula="Not calculated",
        fields=(),
        aggregation="Not available",
        included_rows=0,
        excluded_rows=0,
        steps=(
            CalculationStep(
                "Configuration required",
                option.availability_reason,
            ),
        ),
        assumptions=(),
        limitations=(
            "No result was generated because required fields are missing.",
        ),
        available=False,
    )


def _metric_explanation(
    dataframe: pd.DataFrame,
    config: Mapping[str, object],
    calculation_key: str,
) -> CalculationExplanation:
    metric_column = str(config["metric_column"])
    metric = pd.to_numeric(
        dataframe[metric_column],
        errors="coerce",
    )
    valid = metric.dropna()
    excluded = len(metric) - len(valid)
    definitions: dict[
        str,
        tuple[
            str,
            str,
            Callable[[pd.Series], float],
            str,
        ],
    ] = {
        TOTAL_CALCULATION: (
            "Total primary metric",
            "SUM(valid metric values)",
            lambda values: float(values.sum()),
            "Sum",
        ),
        AVERAGE_CALCULATION: (
            "Average primary metric",
            "SUM(valid metric values) ÷ COUNT(valid metric values)",
            lambda values: float(values.mean()),
            "Arithmetic mean",
        ),
        MEDIAN_CALCULATION: (
            "Median primary metric",
            "Middle ordered value (or mean of two middle values)",
            lambda values: float(values.median()),
            "Median",
        ),
    }
    title, formula, calculator, aggregation = definitions[calculation_key]

    if valid.empty:
        result = "Not available"
        steps = (
            CalculationStep(
                "Parse values",
                f"0 of {len(metric):,} '{metric_column}' values are numeric.",
            ),
        )
        available = False
    else:
        value = calculator(valid)
        result = _format_number(value)
        steps = (
            CalculationStep(
                "Parse values",
                (
                    f"{len(valid):,} of {len(metric):,} "
                    f"'{metric_column}' values are usable numbers."
                ),
            ),
            CalculationStep(
                f"Apply {aggregation.lower()}",
                f"The calculated result is {result}.",
            ),
        )
        available = True

    return CalculationExplanation(
        key=calculation_key,
        title=title,
        result=result,
        formula=formula,
        fields=(metric_column,),
        aggregation=aggregation,
        included_rows=len(valid),
        excluded_rows=excluded,
        steps=steps,
        assumptions=(
            "Each valid row contributes equally unless the formula states "
            "otherwise.",
            "Non-numeric and missing metric values are excluded.",
        ),
        limitations=(
            "The result describes the active dataframe selection only.",
            "No currency, unit, target or business definition is inferred.",
        ),
        available=available,
    )


def _quality_explanation(
    dataframe: pd.DataFrame,
) -> CalculationExplanation:
    report = calculate_quality_score(dataframe)
    steps = tuple(
        CalculationStep(
            check.name,
            (
                f"{check.score:.1f}/100 × {check.weight:.0%} = "
                f"{check.weighted_points:.1f} weighted points. "
                f"{check.explanation}"
            ),
        )
        for check in report.checks
    )

    return CalculationExplanation(
        key=QUALITY_CALCULATION,
        title="Data Quality Score",
        result=f"{report.score:.1f}/100 ({report.status})",
        formula=(
            "Completeness × 50% + Duplicate-free rows × 30% + "
            "Type validity × 20%"
        ),
        fields=tuple(str(column) for column in dataframe.columns),
        aggregation="Weighted score",
        included_rows=len(dataframe),
        excluded_rows=0,
        steps=steps,
        assumptions=(
            "The three component weights are fixed product rules.",
            "Missingness, duplicates and type consistency are observable "
            "technical checks.",
        ),
        limitations=(
            "Technical quality does not prove factual accuracy.",
            "The score does not measure bias, relevance or fitness for a "
            "specific business decision.",
        ),
    )


def _period_change_explanation(
    dataframe: pd.DataFrame,
    config: Mapping[str, object],
) -> CalculationExplanation:
    date_column = str(config["date_column"])
    metric_column = str(config["metric_column"])
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
    excluded = len(dataframe) - len(prepared)
    daily = (
        prepared.assign(date=prepared["date"].dt.normalize())
        .groupby("date")["metric"]
        .sum()
        .sort_index()
    )

    if len(daily) < 2:
        return CalculationExplanation(
            key=PERIOD_CHANGE_CALCULATION,
            title="First-half vs second-half change",
            result="Not available",
            formula=(
                "(second-half daily average − first-half daily average) ÷ "
                "|first-half daily average|"
            ),
            fields=(date_column, metric_column),
            aggregation="Daily sum, then half-period mean",
            included_rows=len(prepared),
            excluded_rows=excluded,
            steps=(
                CalculationStep(
                    "Check coverage",
                    "At least two valid dates are required.",
                ),
            ),
            assumptions=(
                "Dates are ordered chronologically before splitting.",
            ),
            limitations=(
                "No period comparison was generated.",
            ),
            available=False,
        )

    midpoint = len(daily) // 2
    first = daily.iloc[:midpoint]
    second = daily.iloc[midpoint:]
    first_average = float(first.mean())
    second_average = float(second.mean())
    if abs(first_average) < 1e-12:
        result = "Not available"
        change_detail = (
            "The first-half average is zero, so a percentage change would "
            "require division by zero."
        )
        available = False
    else:
        change = (
            (second_average - first_average)
            / abs(first_average)
        )
        result = f"{change:+.1%}"
        change_detail = (
            f"({_format_number(second_average)} − "
            f"{_format_number(first_average)}) ÷ "
            f"|{_format_number(first_average)}| = {result}."
        )
        available = True

    return CalculationExplanation(
        key=PERIOD_CHANGE_CALCULATION,
        title="First-half vs second-half change",
        result=result,
        formula=(
            "(second-half daily average − first-half daily average) ÷ "
            "|first-half daily average|"
        ),
        fields=(date_column, metric_column),
        aggregation="Daily sum, then half-period mean",
        included_rows=len(prepared),
        excluded_rows=excluded,
        steps=(
            CalculationStep(
                "Aggregate by day",
                (
                    f"{len(prepared):,} valid rows became "
                    f"{len(daily):,} daily totals."
                ),
            ),
            CalculationStep(
                "Split the ordered dates",
                (
                    f"The first half contains {len(first):,} dates and the "
                    f"second half contains {len(second):,} dates."
                ),
            ),
            CalculationStep(
                "Compare daily averages",
                change_detail,
            ),
        ),
        assumptions=(
            "The metric is summed within each calendar day.",
            "The chronological series is split by number of distinct dates, "
            "not by equal calendar duration.",
        ),
        limitations=(
            "The comparison does not establish seasonality or causation.",
            "Results may change with filters, date coverage or aggregation.",
        ),
        available=available,
    )


def _category_share_explanation(
    dataframe: pd.DataFrame,
    config: Mapping[str, object],
) -> CalculationExplanation:
    category_column = str(config["category_column"])
    metric_column = str(config["metric_column"])
    prepared = pd.DataFrame(
        {
            "category": dataframe[category_column].astype("string"),
            "metric": pd.to_numeric(
                dataframe[metric_column],
                errors="coerce",
            ),
        }
    ).dropna()
    excluded = len(dataframe) - len(prepared)
    grouped = (
        prepared.groupby("category")["metric"]
        .sum()
        .sort_values(ascending=False)
    )
    total = float(grouped.sum()) if not grouped.empty else 0.0

    if grouped.empty or total <= 0:
        result = "Not available"
        steps = (
            CalculationStep(
                "Check usable values",
                "A positive grouped total is required.",
            ),
        )
        available = False
    else:
        leader = str(grouped.index[0])
        leader_value = float(grouped.iloc[0])
        share = leader_value / total
        result = f"{leader}: {share:.1%}"
        steps = (
            CalculationStep(
                "Group and sum",
                (
                    f"{len(prepared):,} rows were grouped into "
                    f"{len(grouped):,} '{category_column}' values."
                ),
            ),
            CalculationStep(
                "Identify the leader",
                (
                    f"'{leader}' has {_format_number(leader_value)} out of "
                    f"{_format_number(total)} total {metric_column}."
                ),
            ),
            CalculationStep(
                "Calculate contribution",
                (
                    f"{_format_number(leader_value)} ÷ "
                    f"{_format_number(total)} = {share:.1%}."
                ),
            ),
        )
        available = True

    return CalculationExplanation(
        key=CATEGORY_SHARE_CALCULATION,
        title="Leading category contribution",
        result=result,
        formula=(
            "largest category metric sum ÷ total metric sum across categories"
        ),
        fields=(category_column, metric_column),
        aggregation="Sum by category",
        included_rows=len(prepared),
        excluded_rows=excluded,
        steps=steps,
        assumptions=(
            "The metric is additive across categories.",
            "Rows with a missing category or unusable metric are excluded.",
        ),
        limitations=(
            "Contribution does not account for targets, margins or segment "
            "size.",
            "A leading category is not automatically the best-performing one.",
        ),
        available=available,
    )


def _outlier_explanation(
    dataframe: pd.DataFrame,
    config: Mapping[str, object],
) -> CalculationExplanation:
    metric_column = str(config["metric_column"])
    metric = pd.to_numeric(
        dataframe[metric_column],
        errors="coerce",
    )
    valid = metric.dropna()
    excluded = len(metric) - len(valid)

    if len(valid) < 4:
        return CalculationExplanation(
            key=OUTLIER_CALCULATION,
            title="Unusual values (1.5×IQR)",
            result="Not available",
            formula=(
                "values below Q1 − 1.5×IQR or above Q3 + 1.5×IQR"
            ),
            fields=(metric_column,),
            aggregation="Row-level screening",
            included_rows=len(valid),
            excluded_rows=excluded,
            steps=(
                CalculationStep(
                    "Check sample",
                    "At least four usable metric values are required.",
                ),
            ),
            assumptions=(),
            limitations=(
                "No outlier screen was generated.",
            ),
            available=False,
        )

    first_quartile = float(valid.quantile(0.25))
    third_quartile = float(valid.quantile(0.75))
    iqr = third_quartile - first_quartile
    lower = first_quartile - 1.5 * iqr
    upper = third_quartile + 1.5 * iqr
    flagged = valid[(valid < lower) | (valid > upper)]
    share = len(flagged) / len(valid)

    return CalculationExplanation(
        key=OUTLIER_CALCULATION,
        title="Unusual values (1.5×IQR)",
        result=f"{len(flagged):,} values ({share:.1%})",
        formula=(
            "values below Q1 − 1.5×IQR or above Q3 + 1.5×IQR"
        ),
        fields=(metric_column,),
        aggregation="Row-level screening",
        included_rows=len(valid),
        excluded_rows=excluded,
        steps=(
            CalculationStep(
                "Calculate quartiles",
                (
                    f"Q1 = {_format_number(first_quartile)}; "
                    f"Q3 = {_format_number(third_quartile)}."
                ),
            ),
            CalculationStep(
                "Calculate IQR",
                (
                    f"{_format_number(third_quartile)} − "
                    f"{_format_number(first_quartile)} = "
                    f"{_format_number(iqr)}."
                ),
            ),
            CalculationStep(
                "Apply the screening bounds",
                (
                    f"Values below {_format_number(lower)} or above "
                    f"{_format_number(upper)} are flagged."
                ),
            ),
        ),
        assumptions=(
            "The standard 1.5×IQR screening convention is used.",
        ),
        limitations=(
            "A flagged value is not automatically an error.",
            "The rule does not use business thresholds or time context.",
        ),
    )


def _correlation_explanation(
    dataframe: pd.DataFrame,
    config: Mapping[str, object],
) -> CalculationExplanation:
    metric_column = str(config["metric_column"])
    numeric_columns = _numeric_columns(dataframe, config)
    numeric = dataframe[numeric_columns].apply(
        pd.to_numeric,
        errors="coerce",
    )
    correlations = (
        numeric.corr()[metric_column]
        .drop(labels=[metric_column], errors="ignore")
        .dropna()
    )

    if correlations.empty:
        return CalculationExplanation(
            key=CORRELATION_CALCULATION,
            title="Strongest numeric correlation",
            result="Not available",
            formula="Pearson correlation coefficient (r)",
            fields=tuple(numeric_columns),
            aggregation="Pairwise correlation",
            included_rows=0,
            excluded_rows=len(dataframe),
            steps=(
                CalculationStep(
                    "Check comparable fields",
                    "No valid pairwise correlation could be calculated.",
                ),
            ),
            assumptions=(),
            limitations=(
                "Constant or insufficient numeric values cannot be "
                "correlated.",
            ),
            available=False,
        )

    related_column = str(correlations.abs().idxmax())
    coefficient = float(correlations[related_column])
    paired = numeric[[metric_column, related_column]].dropna()

    return CalculationExplanation(
        key=CORRELATION_CALCULATION,
        title="Strongest numeric correlation",
        result=f"{related_column}: r = {coefficient:.2f}",
        formula=(
            "Pearson r = covariance(X, Y) ÷ "
            "(standard deviation X × standard deviation Y)"
        ),
        fields=(metric_column, related_column),
        aggregation="Pairwise Pearson correlation",
        included_rows=len(paired),
        excluded_rows=len(dataframe) - len(paired),
        steps=(
            CalculationStep(
                "Parse numeric fields",
                (
                    f"{len(numeric_columns):,} configured numeric fields "
                    "were compared with the primary metric."
                ),
            ),
            CalculationStep(
                "Use complete pairs",
                (
                    f"{len(paired):,} rows contain both '{metric_column}' "
                    f"and '{related_column}'."
                ),
            ),
            CalculationStep(
                "Select the strongest absolute coefficient",
                (
                    f"'{related_column}' has the largest |r|: "
                    f"{coefficient:.2f}."
                ),
            ),
        ),
        assumptions=(
            "The relationship is screened as linear.",
            "Pairwise-complete rows are used for each correlation.",
        ),
        limitations=(
            "Correlation does not prove causation.",
            "The coefficient may reflect shared drivers, time effects, "
            "aggregation or chance.",
        ),
    )


def explain_calculation(
    dataframe: pd.DataFrame,
    config: Mapping[str, object],
    calculation_key: str,
) -> CalculationExplanation:
    """Explain one supported calculation with row-level scope context."""

    options = {
        option.key: option
        for option in calculation_options(dataframe, config)
    }
    if calculation_key not in options:
        raise ValueError(
            f"Unsupported calculation: {calculation_key}"
        )
    option = options[calculation_key]
    if not option.available:
        return _unavailable_explanation(option)

    if calculation_key in {
        TOTAL_CALCULATION,
        AVERAGE_CALCULATION,
        MEDIAN_CALCULATION,
    }:
        return _metric_explanation(
            dataframe,
            config,
            calculation_key,
        )
    if calculation_key == QUALITY_CALCULATION:
        return _quality_explanation(dataframe)
    if calculation_key == PERIOD_CHANGE_CALCULATION:
        return _period_change_explanation(dataframe, config)
    if calculation_key == CATEGORY_SHARE_CALCULATION:
        return _category_share_explanation(dataframe, config)
    if calculation_key == OUTLIER_CALCULATION:
        return _outlier_explanation(dataframe, config)
    return _correlation_explanation(dataframe, config)
