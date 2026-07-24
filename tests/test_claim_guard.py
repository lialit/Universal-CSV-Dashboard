import pandas as pd

from app_core.claim_guard import (
    review_claims,
    review_summary_draft,
)
from app_core.summary_drafts import build_summary_draft


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


def safe_text() -> str:
    return """
## Verified facts
[F1] Sales increased by 12%.
Evidence: calculated from 40 usable rows.

## Evidence-based interpretations
[I1] The change may indicate a material period difference.
Evidence: first-half and second-half daily averages.
Confidence: Moderate.
Interpretation boundary: This does not establish causes.

## Limitations
The selected period may not be representative.
"""


def test_safe_text_is_ready() -> None:
    review = review_claims(safe_text())

    assert review.status == "Ready"
    assert review.score == 100
    assert review.issues == ()
    assert review.ready_for_export


def test_generated_draft_passes_guard() -> None:
    draft = build_summary_draft(
        sample_dataframe(),
        sample_config(),
        length="Detailed",
    )
    review = review_summary_draft(draft)

    assert review.status == "Ready"
    assert review.score == 100


def test_unsupported_causal_claim_is_blocked() -> None:
    text = safe_text() + "\nPromotions caused the sales increase."
    review = review_claims(text)

    assert review.status == "Blocked"
    assert any(
        issue.code == "UNSUPPORTED_CAUSALITY"
        for issue in review.issues
    )


def test_causal_disclaimer_is_not_flagged() -> None:
    text = safe_text() + "\nCorrelation does not prove causation."
    review = review_claims(text)

    assert all(
        issue.code not in {
            "UNSUPPORTED_CAUSALITY",
            "EXCESSIVE_CERTAINTY",
        }
        for issue in review.issues
    )


def test_unsupported_prediction_is_blocked() -> None:
    text = safe_text() + "\nSales will increase next quarter."
    review = review_claims(text)

    assert review.status == "Blocked"
    assert any(
        issue.code == "UNSUPPORTED_PREDICTION"
        for issue in review.issues
    )


def test_excessive_certainty_is_blocked() -> None:
    text = safe_text() + "\nThis definitely proves the strategy works."
    review = review_claims(text)

    assert review.status == "Blocked"
    assert any(
        issue.code == "EXCESSIVE_CERTAINTY"
        for issue in review.issues
    )


def test_directive_action_requires_review() -> None:
    text = safe_text() + "\nThe company should increase inventory."
    review = review_claims(text)

    assert review.status == "Review"
    assert any(
        issue.code == "DIRECTIVE_RECOMMENDATION"
        for issue in review.issues
    )
    assert review.ready_for_export


def test_invented_budget_is_blocked() -> None:
    text = safe_text() + "\nThe budget is 2 million dollars."
    review = review_claims(text)

    assert review.status == "Blocked"
    assert any(
        issue.code == "INVENTED_BUSINESS_CONTEXT"
        for issue in review.issues
    )


def test_missing_safety_sections_are_reported() -> None:
    review = review_claims("Sales increased by 12%.")
    codes = {issue.code for issue in review.issues}

    assert review.status == "Blocked"
    assert "MISSING_EVIDENCE" in codes
    assert "MISSING_LIMITATIONS" in codes


def test_missing_interpretation_context_requires_review() -> None:
    text = """
## Interpretation
Sales may be changing.
Evidence: period averages.
## Limitations
The sample is limited.
"""
    review = review_claims(text)

    assert review.status == "Review"
    assert any(
        issue.code == "MISSING_CONFIDENCE"
        for issue in review.issues
    )


def test_review_is_deterministic_and_deduplicated() -> None:
    text = safe_text() + "\nPromotions caused the change."
    first = review_claims(text)
    second = review_claims(text)

    assert first == second
    keys = [
        (issue.code, issue.matched_text)
        for issue in first.issues
    ]
    assert len(keys) == len(set(keys))
