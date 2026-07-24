from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Mapping

import pandas as pd

from app_core.executive_summary import build_executive_summary
from app_core.insights import BusinessInsight, build_business_insights
from app_core.quality import calculate_quality_score


OVERVIEW_QUESTION = "overview"
METRIC_QUESTION = "metric"
TREND_QUESTION = "trend"
SEGMENT_QUESTION = "segment"
RELIABILITY_QUESTION = "reliability"


@dataclass(frozen=True)
class GuidedQuestion:
    """One supported question in the local analysis assistant."""

    key: str
    label: str
    description: str
    available: bool
    availability_reason: str


@dataclass(frozen=True)
class AssistantAnswer:
    """A cautious answer linked to observable evidence."""

    question: str
    headline: str
    explanation: str
    evidence: tuple[str, ...]
    confidence: str
    confidence_reason: str
    limitations: tuple[str, ...]
    next_steps: tuple[str, ...]
    method: str = "Local deterministic analysis"


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


def available_questions(
    dataframe: pd.DataFrame,
    config: Mapping[str, object],
) -> tuple[GuidedQuestion, ...]:
    """Return the supported questions and explain any unavailable option."""

    metric = _configured_column(dataframe, config, "metric_column")
    date = _configured_column(dataframe, config, "date_column")
    category = _configured_column(dataframe, config, "category_column")

    return (
        GuidedQuestion(
            key=OVERVIEW_QUESTION,
            label="What should I know first?",
            description=(
                "Summarize the primary facts, material patterns and "
                "limitations."
            ),
            available=metric is not None,
            availability_reason=(
                "Available for the configured primary metric."
                if metric
                else "Select a valid primary metric first."
            ),
        ),
        GuidedQuestion(
            key=METRIC_QUESTION,
            label="How is the primary metric performing?",
            description=(
                "Explain the total, average, median and completeness."
            ),
            available=metric is not None,
            availability_reason=(
                "Available for the configured primary metric."
                if metric
                else "Select a valid primary metric first."
            ),
        ),
        GuidedQuestion(
            key=TREND_QUESTION,
            label="What changed over time?",
            description=(
                "Compare the first and second halves of the selected period."
            ),
            available=metric is not None and date is not None,
            availability_reason=(
                "Available for the configured metric and date."
                if metric and date
                else "Configure both a metric and a date column."
            ),
        ),
        GuidedQuestion(
            key=SEGMENT_QUESTION,
            label="Which segment matters most?",
            description=(
                "Identify the leading category and explain its contribution."
            ),
            available=metric is not None and category is not None,
            availability_reason=(
                "Available for the configured metric and category."
                if metric and category
                else "Configure both a metric and a category column."
            ),
        ),
        GuidedQuestion(
            key=RELIABILITY_QUESTION,
            label="Can I trust this analysis?",
            description=(
                "Explain technical data quality and analytical limitations."
            ),
            available=True,
            availability_reason=(
                "Available from the local Data Quality Score."
            ),
        ),
    )


def _unavailable_answer(
    question: GuidedQuestion,
) -> AssistantAnswer:
    return AssistantAnswer(
        question=question.label,
        headline="This question needs additional configuration.",
        explanation=question.availability_reason,
        evidence=(),
        confidence="Unavailable",
        confidence_reason=(
            "The required columns are not configured in the current dataset."
        ),
        limitations=(
            "No analytical conclusion was generated.",
        ),
        next_steps=(
            "Open Upload & Configure and complete the missing field mapping.",
        ),
    )


def _overview_answer(
    dataframe: pd.DataFrame,
    config: Mapping[str, object],
    question: GuidedQuestion,
) -> AssistantAnswer:
    summary = build_executive_summary(dataframe, config)
    report = build_business_insights(dataframe, config)
    evidence = tuple(
        f"{statement.title}: {statement.text} Evidence: {statement.evidence}"
        for statement in summary.facts
    )
    material_patterns = tuple(
        statement.text for statement in summary.interpretations
    )
    if material_patterns:
        explanation = " ".join(material_patterns)
    else:
        explanation = (
            "The current rules did not detect a material pattern above their "
            "configured thresholds. The verified facts remain available "
            "below."
        )

    limitations = tuple(
        statement.text for statement in summary.limitations
    ) + report.limitations
    if not limitations:
        limitations = (
            "The explanation describes patterns in the selected data. It "
            "does not establish causes, targets or business impact.",
        )
    confidence = (
        report.insights[0].confidence
        if report.insights
        else ("Low" if len(dataframe) < 30 else "Moderate")
    )
    confidence_reason = (
        report.insights[0].confidence_reason
        if report.insights
        else (
            f"Based on {len(dataframe):,} rows and a "
            f"{report.quality_score:.1f}/100 Data Quality Score."
        )
    )

    return AssistantAnswer(
        question=question.label,
        headline=summary.headline,
        explanation=explanation,
        evidence=evidence,
        confidence=confidence,
        confidence_reason=confidence_reason,
        limitations=tuple(dict.fromkeys(limitations)),
        next_steps=summary.next_steps,
    )


def _metric_answer(
    dataframe: pd.DataFrame,
    config: Mapping[str, object],
    question: GuidedQuestion,
) -> AssistantAnswer:
    metric_column = str(config["metric_column"])
    metric = pd.to_numeric(
        dataframe[metric_column],
        errors="coerce",
    )
    valid = metric.dropna()

    if valid.empty:
        return AssistantAnswer(
            question=question.label,
            headline=f"'{metric_column}' contains no usable numeric values.",
            explanation=(
                "The metric cannot be summarized until valid numbers are "
                "available."
            ),
            evidence=(
                f"0 of {len(metric):,} rows parsed as numeric.",
            ),
            confidence="Low",
            confidence_reason="No usable metric observations are available.",
            limitations=(
                "No performance conclusion was generated.",
            ),
            next_steps=(
                "Review the metric mapping and source values.",
            ),
        )

    total = float(valid.sum())
    average = float(valid.mean())
    median = float(valid.median())
    completeness = len(valid) / len(metric) if len(metric) else 0.0
    difference = average - median
    scale = max(abs(average), abs(median), 1e-12)

    if abs(difference) / scale >= 0.25:
        direction = "above" if difference > 0 else "below"
        explanation = (
            f"The average is materially {direction} the median, so extreme "
            "values may be influencing the typical-looking result."
        )
    else:
        explanation = (
            "The average and median are reasonably close, so the central "
            "values do not show a strong imbalance by this screening rule."
        )

    quality = calculate_quality_score(dataframe)
    confidence = (
        "Low"
        if len(valid) < 30 or completeness < 0.80 or quality.score < 60
        else "High"
        if len(valid) >= 100 and completeness >= 0.98 and quality.score >= 90
        else "Moderate"
    )

    return AssistantAnswer(
        question=question.label,
        headline=(
            f"Total {metric_column} is {_format_number(total)} across "
            f"{len(valid):,} usable rows."
        ),
        explanation=explanation,
        evidence=(
            f"Average: {_format_number(average)}.",
            f"Median: {_format_number(median)}.",
            f"Metric completeness: {completeness:.1%}.",
        ),
        confidence=confidence,
        confidence_reason=(
            f"Based on {len(valid):,} usable values, {completeness:.1%} "
            f"metric completeness and a {quality.score:.1f}/100 Data "
            "Quality Score."
        ),
        limitations=(
            "Totals and averages describe the selected rows only.",
            "No target, budget or prior comparable period was provided.",
        ),
        next_steps=(
            "Compare the metric over time and across the configured category.",
            "Confirm that the selected aggregation matches the business use.",
        ),
    )


def _insight_answer(
    question: GuidedQuestion,
    insight: BusinessInsight | None,
    unavailable_explanation: str,
) -> AssistantAnswer:
    if insight is None:
        return AssistantAnswer(
            question=question.label,
            headline="No material pattern crossed the current threshold.",
            explanation=unavailable_explanation,
            evidence=(
                "The configured deterministic screening rule returned no "
                "material result.",
            ),
            confidence="Moderate",
            confidence_reason=(
                "The answer is based on a transparent threshold, but absence "
                "of a flagged pattern is not proof that no pattern exists."
            ),
            limitations=(
                "A different date range, aggregation or category may produce "
                "a different result.",
            ),
            next_steps=(
                "Review the supporting chart or adjust the active selection.",
            ),
        )

    return AssistantAnswer(
        question=question.label,
        headline=insight.observation,
        explanation=insight.interpretation,
        evidence=(insight.evidence,),
        confidence=insight.confidence,
        confidence_reason=insight.confidence_reason,
        limitations=(insight.limitation,),
        next_steps=(insight.next_question,),
    )


def _reliability_answer(
    dataframe: pd.DataFrame,
    config: Mapping[str, object],
    question: GuidedQuestion,
) -> AssistantAnswer:
    quality = calculate_quality_score(dataframe)
    summary = build_executive_summary(dataframe, config)
    limitations = tuple(
        statement.text for statement in summary.limitations
    )
    detected_issues = (
        quality.missing_cells
        + quality.duplicate_rows
        + quality.invalid_type_cells
    )

    if quality.score >= 90:
        explanation = (
            "The dataset has strong observable technical quality. This "
            "supports calculation reliability, but it does not prove that "
            "the source data is accurate, unbiased or decision-ready."
        )
    elif quality.score >= 70:
        explanation = (
            "The dataset is usable with caution. Review the detected quality "
            "issues before relying on sensitive conclusions."
        )
    else:
        explanation = (
            "Technical quality issues may materially affect the analysis. "
            "Resolve or explicitly accept them before sharing conclusions."
        )

    return AssistantAnswer(
        question=question.label,
        headline=(
            f"Data Quality Score: {quality.score:.1f}/100 "
            f"({quality.status})."
        ),
        explanation=explanation,
        evidence=(
            f"Missing cells: {quality.missing_cells:,}.",
            f"Duplicate rows: {quality.duplicate_rows:,}.",
            f"Invalid-type cells: {quality.invalid_type_cells:,}.",
            f"Detected technical issues: {detected_issues:,}.",
        ),
        confidence="High",
        confidence_reason=(
            "The quality result is calculated directly from observable "
            "missingness, duplicates and type consistency."
        ),
        limitations=tuple(dict.fromkeys((
            "Technical quality does not establish business correctness.",
            *limitations,
        ))),
        next_steps=(
            "Open Data Quality to inspect column-level evidence.",
            "Validate business definitions and source-system accuracy.",
        ),
    )


def answer_guided_question(
    dataframe: pd.DataFrame,
    config: Mapping[str, object],
    question_key: str,
) -> AssistantAnswer:
    """Answer one supported question without sending data externally."""

    questions = {
        question.key: question
        for question in available_questions(dataframe, config)
    }
    if question_key not in questions:
        raise ValueError(f"Unsupported guided question: {question_key}")

    question = questions[question_key]
    if not question.available:
        return _unavailable_answer(question)

    if question_key == OVERVIEW_QUESTION:
        return _overview_answer(dataframe, config, question)
    if question_key == METRIC_QUESTION:
        return _metric_answer(dataframe, config, question)
    if question_key == RELIABILITY_QUESTION:
        return _reliability_answer(dataframe, config, question)

    report = build_business_insights(dataframe, config)
    if question_key == TREND_QUESTION:
        insight = next(
            (
                item
                for item in report.insights
                if item.insight_type == "Trend"
            ),
            None,
        )
        return _insight_answer(
            question,
            insight,
            (
                "The first-versus-second-half comparison did not exceed the "
                "current 10% materiality threshold."
            ),
        )

    insight = next(
        (
            item
            for item in report.insights
            if item.insight_type == "Contribution"
        ),
        None,
    )
    return _insight_answer(
        question,
        insight,
        (
            "No category contribution required a stronger warning under the "
            "current screening rules."
        ),
    )
