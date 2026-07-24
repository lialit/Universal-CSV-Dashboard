import pandas as pd
import pytest

from app_core.assistant import (
    ANOMALY_QUESTION,
    METRIC_QUESTION,
    OVERVIEW_QUESTION,
    RELIABILITY_QUESTION,
    RELATIONSHIP_QUESTION,
    SEGMENT_QUESTION,
    TREND_QUESTION,
    answer_guided_question,
    available_questions,
    suggest_follow_up_questions,
)


def sample_dataframe() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "date": pd.date_range("2026-01-01", periods=40),
            "region": ["North"] * 30 + ["South"] * 10,
            "sales": [10.0] * 20 + [20.0] * 20,
            "orders": list(range(1, 41)),
        }
    )


def sample_config() -> dict[str, object]:
    return {
        "date_column": "date",
        "category_column": "region",
        "metric_column": "sales",
        "numeric_columns": ["sales", "orders"],
    }


def test_questions_disclose_availability() -> None:
    questions = available_questions(
        sample_dataframe()[["sales"]],
        {"metric_column": "sales"},
    )
    availability = {
        question.key: question.available for question in questions
    }

    assert availability[OVERVIEW_QUESTION]
    assert availability[METRIC_QUESTION]
    assert not availability[TREND_QUESTION]
    assert not availability[SEGMENT_QUESTION]
    assert availability[ANOMALY_QUESTION]
    assert not availability[RELATIONSHIP_QUESTION]
    assert availability[RELIABILITY_QUESTION]


def test_overview_answer_links_evidence_and_limitations() -> None:
    answer = answer_guided_question(
        sample_dataframe(),
        sample_config(),
        OVERVIEW_QUESTION,
    )

    assert "40 rows were analyzed" in answer.headline
    assert answer.evidence
    assert answer.limitations
    assert answer.method == "Local deterministic analysis"


def test_metric_answer_explains_primary_kpis() -> None:
    answer = answer_guided_question(
        sample_dataframe(),
        sample_config(),
        METRIC_QUESTION,
    )

    assert "Total sales is 600" in answer.headline
    assert any("Average: 15" in item for item in answer.evidence)
    assert any("Median: 15" in item for item in answer.evidence)
    assert "100.0%" in answer.confidence_reason


def test_trend_answer_reuses_traceable_business_insight() -> None:
    answer = answer_guided_question(
        sample_dataframe(),
        sample_config(),
        TREND_QUESTION,
    )

    assert "100.0% higher" in answer.headline
    assert answer.evidence
    assert any(
        "does not establish seasonality" in limitation
        for limitation in answer.limitations
    )


def test_segment_answer_names_leading_category() -> None:
    answer = answer_guided_question(
        sample_dataframe(),
        sample_config(),
        SEGMENT_QUESTION,
    )

    assert "'North' contributes" in answer.headline
    assert answer.next_steps


def test_reliability_answer_discloses_scope() -> None:
    answer = answer_guided_question(
        sample_dataframe(),
        sample_config(),
        RELIABILITY_QUESTION,
    )

    assert "Data Quality Score" in answer.headline
    assert any(
        "Technical quality does not establish business correctness"
        in limitation
        for limitation in answer.limitations
    )
    assert answer.confidence == "High"


def test_unavailable_question_fails_safely() -> None:
    answer = answer_guided_question(
        sample_dataframe()[["sales"]],
        {"metric_column": "sales"},
        TREND_QUESTION,
    )

    assert answer.confidence == "Unavailable"
    assert not answer.evidence
    assert "date column" in answer.explanation


def test_unknown_question_is_rejected() -> None:
    with pytest.raises(ValueError, match="Unsupported guided question"):
        answer_guided_question(
            sample_dataframe(),
            sample_config(),
            "invented-question",
        )


def test_suggestions_follow_detected_evidence() -> None:
    suggestions = suggest_follow_up_questions(
        sample_dataframe(),
        sample_config(),
        current_question_key=OVERVIEW_QUESTION,
    )
    keys = [suggestion.question_key for suggestion in suggestions]

    assert keys[:2] == [TREND_QUESTION, SEGMENT_QUESTION]
    assert OVERVIEW_QUESTION not in keys
    assert len(keys) == len(set(keys))
    assert len(keys) <= 3
    assert all(suggestion.rationale for suggestion in suggestions)


def test_low_quality_prioritizes_reliability() -> None:
    dataframe = sample_dataframe()
    dataframe["orders"] = None

    suggestions = suggest_follow_up_questions(
        dataframe,
        sample_config(),
        current_question_key=OVERVIEW_QUESTION,
    )

    assert suggestions[0].question_key == RELIABILITY_QUESTION
    assert "Data Quality Score" in suggestions[0].rationale


def test_non_positive_limit_returns_no_suggestions() -> None:
    suggestions = suggest_follow_up_questions(
        sample_dataframe(),
        sample_config(),
        limit=0,
    )

    assert suggestions == ()


def test_anomaly_question_explains_flagged_values() -> None:
    dataframe = sample_dataframe()
    dataframe.loc[39, "sales"] = 10_000.0

    answer = answer_guided_question(
        dataframe,
        sample_config(),
        ANOMALY_QUESTION,
    )

    assert "outside the standard 1.5×IQR range" in answer.headline
    assert "not automatically an error" in answer.limitations[0]


def test_relationship_question_explains_correlation() -> None:
    answer = answer_guided_question(
        sample_dataframe(),
        sample_config(),
        RELATIONSHIP_QUESTION,
    )

    assert "correlation" in answer.headline
    assert "does not prove causation" in answer.limitations[0]


def test_suggestions_fall_back_to_supported_context() -> None:
    dataframe = pd.DataFrame({"sales": [10.0] * 40})
    config = {
        "metric_column": "sales",
        "numeric_columns": ["sales"],
    }

    suggestions = suggest_follow_up_questions(
        dataframe,
        config,
        current_question_key=OVERVIEW_QUESTION,
    )
    keys = [suggestion.question_key for suggestion in suggestions]

    assert METRIC_QUESTION in keys
    assert TREND_QUESTION not in keys
    assert SEGMENT_QUESTION not in keys
