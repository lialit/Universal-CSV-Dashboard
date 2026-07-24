import pandas as pd
import pytest

from app_core.summary_drafts import (
    AUDIENCES,
    LENGTHS,
    build_summary_draft,
    summary_draft_to_markdown,
    summary_draft_to_text,
    validate_summary_draft,
)


def sample_dataframe() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "date": pd.date_range("2026-01-01", periods=40),
            "region": ["North"] * 30 + ["South"] * 10,
            "sales": [10.0] * 20 + [20.0] * 19 + [500.0],
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


def test_draft_separates_facts_and_interpretations() -> None:
    draft = build_summary_draft(
        sample_dataframe(),
        sample_config(),
    )

    assert draft.facts
    assert draft.interpretations
    assert all(
        claim.claim_type == "Verified fact"
        for claim in draft.facts
    )
    assert all(
        claim.claim_type == "Interpretation"
        for claim in draft.interpretations
    )


def test_every_claim_is_evidence_linked() -> None:
    draft = build_summary_draft(
        sample_dataframe(),
        sample_config(),
        length="Detailed",
    )

    assert draft.evidence_count == draft.claim_count
    assert all(
        claim.evidence
        for claim in (*draft.facts, *draft.interpretations)
    )
    assert validate_summary_draft(draft) == ()


def test_interpretations_keep_confidence_and_boundary() -> None:
    draft = build_summary_draft(
        sample_dataframe(),
        sample_config(),
    )

    assert all(
        claim.confidence
        for claim in draft.interpretations
    )
    assert all(
        claim.boundary
        for claim in draft.interpretations
    )


def test_brief_draft_is_shorter_than_detailed() -> None:
    brief = build_summary_draft(
        sample_dataframe(),
        sample_config(),
        length="Brief",
    )
    detailed = build_summary_draft(
        sample_dataframe(),
        sample_config(),
        length="Detailed",
    )

    assert len(brief.facts) <= 2
    assert len(brief.interpretations) <= 1
    assert len(brief.limitations) <= 2
    assert brief.claim_count < detailed.claim_count


@pytest.mark.parametrize("audience", AUDIENCES)
@pytest.mark.parametrize("length", LENGTHS)
def test_supported_profiles_render(
    audience: str,
    length: str,
) -> None:
    draft = build_summary_draft(
        sample_dataframe(),
        sample_config(),
        audience=audience,
        length=length,
    )

    assert draft.audience == audience
    assert draft.length == length
    assert "No external AI service" in draft.method_note


def test_markdown_contains_source_labels_and_boundaries() -> None:
    draft = build_summary_draft(
        sample_dataframe(),
        sample_config(),
    )
    markdown = summary_draft_to_markdown(draft)

    assert "# Evidence-Based Analysis Summary" in markdown
    assert "[F1]" in markdown
    assert "[I1]" in markdown
    assert "Evidence:" in markdown
    assert "Interpretation boundary:" in markdown
    assert "## Limitations" in markdown


def test_plain_text_does_not_use_markdown_headings() -> None:
    draft = build_summary_draft(
        sample_dataframe(),
        sample_config(),
    )
    text = summary_draft_to_text(draft)

    assert "# " not in text
    assert "VERIFIED FACTS" in text
    assert "METHOD NOTE" in text


def test_draft_is_deterministic() -> None:
    first = build_summary_draft(
        sample_dataframe(),
        sample_config(),
    )
    second = build_summary_draft(
        sample_dataframe(),
        sample_config(),
    )

    assert first == second
    assert summary_draft_to_markdown(first) == (
        summary_draft_to_markdown(second)
    )


def test_missing_dimensions_remain_visible_as_limitations() -> None:
    dataframe = sample_dataframe()[["sales"]]
    config = {
        "metric_column": "sales",
        "numeric_columns": ["sales"],
    }
    draft = build_summary_draft(
        dataframe,
        config,
        length="Detailed",
    )

    assert any(
        "Time trends" in limitation
        for limitation in draft.limitations
    )
    assert any(
        "Segment-level" in limitation
        for limitation in draft.limitations
    )


def test_invalid_profile_is_rejected() -> None:
    with pytest.raises(ValueError, match="Unsupported audience"):
        build_summary_draft(
            sample_dataframe(),
            sample_config(),
            audience="Invented",
        )

    with pytest.raises(ValueError, match="Unsupported draft length"):
        build_summary_draft(
            sample_dataframe(),
            sample_config(),
            length="Endless",
        )
