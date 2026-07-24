from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

import pandas as pd

from app_core.executive_summary import build_executive_summary
from app_core.insights import build_business_insights


AUDIENCES = (
    "Executive",
    "Business stakeholder",
    "Analyst",
)
LENGTHS = (
    "Brief",
    "Standard",
    "Detailed",
)


@dataclass(frozen=True)
class DraftClaim:
    """One source-linked claim included in a summary draft."""

    claim_id: str
    claim_type: str
    title: str
    text: str
    evidence: str
    confidence: str | None = None
    boundary: str | None = None


@dataclass(frozen=True)
class SummaryDraft:
    """An evidence-based report draft assembled from local calculations."""

    title: str
    audience: str
    length: str
    headline: str
    facts: tuple[DraftClaim, ...]
    interpretations: tuple[DraftClaim, ...]
    limitations: tuple[str, ...]
    next_steps: tuple[str, ...]
    method_note: str

    @property
    def evidence_count(self) -> int:
        return len(self.facts) + len(self.interpretations)

    @property
    def claim_count(self) -> int:
        return self.evidence_count


def _limits_for_length(length: str) -> tuple[int | None, ...]:
    limits: dict[str, tuple[int | None, ...]] = {
        "Brief": (2, 1, 2, 2),
        "Standard": (4, 3, 4, 4),
        "Detailed": (None, None, None, None),
    }
    return limits[length]


def _take(
    values: tuple,
    limit: int | None,
) -> tuple:
    if limit is None:
        return values
    return values[:limit]


def _audience_intro(audience: str) -> str:
    intros = {
        "Executive": (
            "This draft highlights decision-relevant facts, material "
            "patterns and the boundaries of the available evidence."
        ),
        "Business stakeholder": (
            "This draft explains the main results in plain business "
            "language while keeping assumptions and limitations visible."
        ),
        "Analyst": (
            "This draft separates observed values from rule-based "
            "interpretation and retains calculation evidence for review."
        ),
    }
    return intros[audience]


def _build_facts(
    dataframe: pd.DataFrame,
    config: Mapping[str, object],
) -> tuple[DraftClaim, ...]:
    summary = build_executive_summary(dataframe, config)
    return tuple(
        DraftClaim(
            claim_id=f"F{index}",
            claim_type="Verified fact",
            title=statement.title,
            text=statement.text,
            evidence=statement.evidence,
        )
        for index, statement in enumerate(
            summary.facts,
            start=1,
        )
    )


def _build_interpretations(
    dataframe: pd.DataFrame,
    config: Mapping[str, object],
) -> tuple[DraftClaim, ...]:
    report = build_business_insights(dataframe, config)
    return tuple(
        DraftClaim(
            claim_id=f"I{index}",
            claim_type="Interpretation",
            title=insight.title,
            text=f"{insight.observation} {insight.interpretation}",
            evidence=insight.evidence,
            confidence=(
                f"{insight.confidence} — "
                f"{insight.confidence_reason}"
            ),
            boundary=insight.limitation,
        )
        for index, insight in enumerate(
            report.insights,
            start=1,
        )
    )


def _build_limitations(
    dataframe: pd.DataFrame,
    config: Mapping[str, object],
) -> tuple[str, ...]:
    summary = build_executive_summary(dataframe, config)
    report = build_business_insights(dataframe, config)
    limitations = [
        statement.text for statement in summary.limitations
    ]
    limitations.extend(report.limitations)
    limitations.append(
        "Observed technical quality does not prove that source values are "
        "accurate, unbiased or suitable for a specific decision."
    )
    limitations.append(
        "The analysis describes association and distribution; it does not "
        "establish causes."
    )
    return tuple(dict.fromkeys(limitations))


def _build_next_steps(
    dataframe: pd.DataFrame,
    config: Mapping[str, object],
) -> tuple[str, ...]:
    summary = build_executive_summary(dataframe, config)
    report = build_business_insights(dataframe, config)
    steps = list(summary.next_steps)
    steps.extend(
        insight.next_question for insight in report.insights
    )
    return tuple(dict.fromkeys(steps))


def build_summary_draft(
    dataframe: pd.DataFrame,
    config: Mapping[str, object],
    audience: str = "Executive",
    length: str = "Standard",
) -> SummaryDraft:
    """Build a deterministic, source-linked report draft."""

    if audience not in AUDIENCES:
        raise ValueError(f"Unsupported audience: {audience}")
    if length not in LENGTHS:
        raise ValueError(f"Unsupported draft length: {length}")

    summary = build_executive_summary(dataframe, config)
    fact_limit, insight_limit, limitation_limit, step_limit = (
        _limits_for_length(length)
    )
    facts = _take(
        _build_facts(dataframe, config),
        fact_limit,
    )
    interpretations = _take(
        _build_interpretations(dataframe, config),
        insight_limit,
    )
    limitations = _take(
        _build_limitations(dataframe, config),
        limitation_limit,
    )
    next_steps = _take(
        _build_next_steps(dataframe, config),
        step_limit,
    )

    return SummaryDraft(
        title="Evidence-Based Analysis Summary",
        audience=audience,
        length=length,
        headline=summary.headline,
        facts=facts,
        interpretations=interpretations,
        limitations=limitations,
        next_steps=next_steps,
        method_note=(
            f"{_audience_intro(audience)} Generated locally from the active "
            "dataframe using deterministic calculations and screening rules. "
            "No external AI service was used."
        ),
    )


def validate_summary_draft(
    draft: SummaryDraft,
) -> tuple[str, ...]:
    """Return validation issues that would make a draft unsafe to share."""

    issues: list[str] = []
    claim_ids = [
        claim.claim_id
        for claim in (*draft.facts, *draft.interpretations)
    ]
    if len(claim_ids) != len(set(claim_ids)):
        issues.append("Claim identifiers must be unique.")

    for claim in (*draft.facts, *draft.interpretations):
        if not claim.evidence.strip():
            issues.append(
                f"{claim.claim_id} does not include supporting evidence."
            )
    for claim in draft.interpretations:
        if not claim.boundary:
            issues.append(
                f"{claim.claim_id} does not include an interpretation boundary."
            )
        if not claim.confidence:
            issues.append(
                f"{claim.claim_id} does not include confidence context."
            )

    if not draft.limitations:
        issues.append("At least one limitation must remain visible.")
    if not draft.method_note:
        issues.append("The calculation method must be disclosed.")

    return tuple(issues)


def summary_draft_to_markdown(
    draft: SummaryDraft,
) -> str:
    """Render a summary draft as portable Markdown."""

    lines = [
        f"# {draft.title}",
        "",
        f"**Audience:** {draft.audience}",
        f"**Detail level:** {draft.length}",
        "",
        "## Executive takeaway",
        "",
        draft.headline,
        "",
        "## Verified facts",
        "",
    ]
    if draft.facts:
        for claim in draft.facts:
            lines.extend(
                [
                    (
                        f"- **[{claim.claim_id}] {claim.title}.** "
                        f"{claim.text}"
                    ),
                    f"  - Evidence: {claim.evidence}",
                ]
            )
    else:
        lines.append(
            "No verified metric facts are available for the current "
            "configuration."
        )

    lines.extend(
        [
            "",
            "## Evidence-based interpretations",
            "",
        ]
    )
    if draft.interpretations:
        for claim in draft.interpretations:
            lines.extend(
                [
                    (
                        f"- **[{claim.claim_id}] {claim.title}.** "
                        f"{claim.text}"
                    ),
                    f"  - Evidence: {claim.evidence}",
                    f"  - Confidence: {claim.confidence}",
                    f"  - Interpretation boundary: {claim.boundary}",
                ]
            )
    else:
        lines.append(
            "No material pattern crossed the current deterministic "
            "screening thresholds."
        )

    lines.extend(
        [
            "",
            "## Limitations",
            "",
        ]
    )
    lines.extend(
        f"- [L{index}] {limitation}"
        for index, limitation in enumerate(
            draft.limitations,
            start=1,
        )
    )
    lines.extend(
        [
            "",
            "## Recommended next steps",
            "",
        ]
    )
    if draft.next_steps:
        lines.extend(
            f"{index}. {step}"
            for index, step in enumerate(
                draft.next_steps,
                start=1,
            )
        )
    else:
        lines.append(
            "Confirm the metric configuration and business question."
        )

    lines.extend(
        [
            "",
            "## Method note",
            "",
            draft.method_note,
            "",
        ]
    )
    return "\n".join(lines)


def summary_draft_to_text(
    draft: SummaryDraft,
) -> str:
    """Render a summary draft as plain text without Markdown syntax."""

    lines = [
        draft.title.upper(),
        f"Audience: {draft.audience}",
        f"Detail level: {draft.length}",
        "",
        "EXECUTIVE TAKEAWAY",
        draft.headline,
        "",
        "VERIFIED FACTS",
    ]
    if draft.facts:
        for claim in draft.facts:
            lines.extend(
                [
                    f"[{claim.claim_id}] {claim.title}: {claim.text}",
                    f"Evidence: {claim.evidence}",
                ]
            )
    else:
        lines.append(
            "No verified metric facts are available for the current "
            "configuration."
        )

    lines.extend(["", "EVIDENCE-BASED INTERPRETATIONS"])
    if draft.interpretations:
        for claim in draft.interpretations:
            lines.extend(
                [
                    f"[{claim.claim_id}] {claim.title}: {claim.text}",
                    f"Evidence: {claim.evidence}",
                    f"Confidence: {claim.confidence}",
                    f"Interpretation boundary: {claim.boundary}",
                ]
            )
    else:
        lines.append(
            "No material pattern crossed the current deterministic "
            "screening thresholds."
        )

    lines.extend(["", "LIMITATIONS"])
    lines.extend(
        f"[L{index}] {limitation}"
        for index, limitation in enumerate(
            draft.limitations,
            start=1,
        )
    )
    lines.extend(["", "RECOMMENDED NEXT STEPS"])
    lines.extend(
        f"{index}. {step}"
        for index, step in enumerate(
            draft.next_steps,
            start=1,
        )
    )
    lines.extend(["", "METHOD NOTE", draft.method_note, ""])
    return "\n".join(lines)
