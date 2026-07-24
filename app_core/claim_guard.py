from __future__ import annotations

from dataclasses import dataclass
import re

from app_core.summary_drafts import (
    SummaryDraft,
    summary_draft_to_markdown,
    validate_summary_draft,
)


@dataclass(frozen=True)
class ClaimIssue:
    """One potentially unsupported or unsafe statement."""

    code: str
    severity: str
    title: str
    matched_text: str
    explanation: str
    safe_rewrite: str


@dataclass(frozen=True)
class ClaimReview:
    """Pre-share safety review for an analytical text."""

    status: str
    score: int
    issues: tuple[ClaimIssue, ...]
    checks: tuple[str, ...]

    @property
    def high_risk_count(self) -> int:
        return sum(
            issue.severity == "High"
            for issue in self.issues
        )

    @property
    def ready_for_export(self) -> bool:
        return self.status != "Blocked"


CAUSAL_PATTERN = re.compile(
    r"\b(?:caused?|causes?|causing|because of|due to|led to|"
    r"resulted in|drives?|driven by)\b",
    flags=re.IGNORECASE,
)
CERTAINTY_PATTERN = re.compile(
    r"\b(?:proves?|guaranteed|definitely|certainly|"
    r"without doubt|always|never)\b",
    flags=re.IGNORECASE,
)
PREDICTION_PATTERN = re.compile(
    r"\b(?:will|is certain to|is expected to)\s+"
    r"(?:increase|decrease|grow|fall|improve|decline|"
    r"rise|drop|worsen)\b",
    flags=re.IGNORECASE,
)
PRESCRIPTION_PATTERN = re.compile(
    r"\b(?:must|should)\s+"
    r"(?:increase|decrease|reduce|raise|cut|stop|invest|"
    r"spend|hire|fire|buy|sell|launch|cancel)\b",
    flags=re.IGNORECASE,
)
UNSUPPORTED_CONTEXT_PATTERN = re.compile(
    r"\b(?:target|budget|forecast|goal)\s+"
    r"(?:is|will be|equals?)\b",
    flags=re.IGNORECASE,
)
SAFE_QUALIFIERS = (
    "does not",
    "do not",
    "did not",
    "cannot",
    "can't",
    "not automatically",
    "no evidence",
    "without establishing",
    "not prove",
)


def _sentences(text: str) -> tuple[str, ...]:
    values = re.split(r"(?<=[.!?])\s+|\n+", text)
    return tuple(
        value.strip(" \t-*#")
        for value in values
        if value.strip(" \t-*#")
    )


def _is_qualified(sentence: str) -> bool:
    lower = sentence.lower()
    return any(
        qualifier in lower
        for qualifier in SAFE_QUALIFIERS
    )


def _issue(
    code: str,
    severity: str,
    title: str,
    matched_text: str,
    explanation: str,
    safe_rewrite: str,
) -> ClaimIssue:
    return ClaimIssue(
        code=code,
        severity=severity,
        title=title,
        matched_text=matched_text,
        explanation=explanation,
        safe_rewrite=safe_rewrite,
    )


def _language_issues(text: str) -> list[ClaimIssue]:
    issues: list[ClaimIssue] = []
    for sentence in _sentences(text):
        qualified = _is_qualified(sentence)
        is_question = sentence.rstrip().endswith("?")

        if (
            CAUSAL_PATTERN.search(sentence)
            and not qualified
            and not is_question
        ):
            issues.append(
                _issue(
                    "UNSUPPORTED_CAUSALITY",
                    "High",
                    "Causal claim without causal evidence",
                    sentence,
                    (
                        "The current analysis can detect association and "
                        "change, but it does not identify causes."
                    ),
                    (
                        "Replace causal wording with 'is associated with', "
                        "'coincides with' or a question for further analysis."
                    ),
                )
            )

        if CERTAINTY_PATTERN.search(sentence) and not qualified:
            issues.append(
                _issue(
                    "EXCESSIVE_CERTAINTY",
                    "High",
                    "Overly certain wording",
                    sentence,
                    (
                        "Analytical screening does not support absolute "
                        "certainty."
                    ),
                    (
                        "Use 'suggests', 'may indicate' or state the observed "
                        "value without a certainty claim."
                    ),
                )
            )

        if PREDICTION_PATTERN.search(sentence) and not qualified:
            issues.append(
                _issue(
                    "UNSUPPORTED_PREDICTION",
                    "High",
                    "Prediction without a forecasting basis",
                    sentence,
                    (
                        "The current assistant describes historical data and "
                        "does not run a forecasting model."
                    ),
                    (
                        "Describe the observed period only, or label the "
                        "future statement as an untested scenario."
                    ),
                )
            )

        if PRESCRIPTION_PATTERN.search(sentence) and not qualified:
            issues.append(
                _issue(
                    "DIRECTIVE_RECOMMENDATION",
                    "Medium",
                    "Directive action without decision context",
                    sentence,
                    (
                        "The dataset does not contain the full costs, risks or "
                        "operational constraints required for this directive."
                    ),
                    (
                        "Frame the action as a question to investigate and "
                        "name the additional evidence required."
                    ),
                )
            )

        if (
            UNSUPPORTED_CONTEXT_PATTERN.search(sentence)
            and not qualified
        ):
            issues.append(
                _issue(
                    "INVENTED_BUSINESS_CONTEXT",
                    "High",
                    "Target, budget or forecast lacks a cited source",
                    sentence,
                    (
                        "Targets, budgets and forecasts are not inferred from "
                        "the uploaded data."
                    ),
                    (
                        "Remove the value or cite the external business source "
                        "that defines it."
                    ),
                )
            )

    return issues


def _structure_issues(text: str) -> list[ClaimIssue]:
    issues: list[ClaimIssue] = []
    lower = text.lower()

    if not text.strip():
        return [
            _issue(
                "EMPTY_TEXT",
                "High",
                "No text to review",
                "",
                "The Claim Guard cannot review an empty summary.",
                "Generate or paste a summary before sharing.",
            )
        ]

    if "evidence:" not in lower:
        issues.append(
            _issue(
                "MISSING_EVIDENCE",
                "Medium",
                "No explicit evidence references",
                "Whole document",
                (
                    "A reader cannot trace analytical claims back to a "
                    "calculation or observed value."
                ),
                (
                    "Add an Evidence line after each important fact and "
                    "interpretation."
                ),
            )
        )

    if "limitation" not in lower:
        issues.append(
            _issue(
                "MISSING_LIMITATIONS",
                "High",
                "Limitations are not visible",
                "Whole document",
                (
                    "The summary presents conclusions without showing where "
                    "the available data may be insufficient."
                ),
                (
                    "Add a visible Limitations section before sharing."
                ),
            )
        )

    has_interpretation = (
        "interpretation" in lower
        or re.search(r"\[I\d+\]", text) is not None
    )
    if has_interpretation and "confidence:" not in lower:
        issues.append(
            _issue(
                "MISSING_CONFIDENCE",
                "Medium",
                "Interpretations lack confidence context",
                "Whole document",
                (
                    "Interpretive claims need a visible reliability context."
                ),
                (
                    "Add a Confidence line based on usable rows, "
                    "completeness and Data Quality Score."
                ),
            )
        )

    if (
        re.search(r"\[I\d+\]", text)
        and "interpretation boundary:" not in lower
    ):
        issues.append(
            _issue(
                "MISSING_BOUNDARY",
                "Medium",
                "Interpretation boundaries are missing",
                "Whole document",
                (
                    "The reader cannot see what the interpretation does not "
                    "establish."
                ),
                (
                    "Add an Interpretation boundary line to every "
                    "interpretive claim."
                ),
            )
        )

    return issues


def _deduplicate(
    issues: list[ClaimIssue],
) -> tuple[ClaimIssue, ...]:
    unique: dict[tuple[str, str], ClaimIssue] = {}
    for issue in issues:
        unique.setdefault(
            (issue.code, issue.matched_text),
            issue,
        )
    return tuple(unique.values())


def review_claims(text: str) -> ClaimReview:
    """Review analytical text for unsupported claim patterns."""

    issues = _deduplicate(
        [
            *_language_issues(text),
            *_structure_issues(text),
        ]
    )
    deductions = {
        "High": 25,
        "Medium": 10,
        "Low": 5,
    }
    score = max(
        0,
        100 - sum(
            deductions[issue.severity]
            for issue in issues
        ),
    )
    if any(issue.severity == "High" for issue in issues):
        status = "Blocked"
    elif issues:
        status = "Review"
    else:
        status = "Ready"

    return ClaimReview(
        status=status,
        score=score,
        issues=issues,
        checks=(
            "Causal language",
            "Forecast and certainty language",
            "Directive recommendations",
            "Invented targets, budgets or forecasts",
            "Evidence, confidence and limitation structure",
        ),
    )


def review_summary_draft(
    draft: SummaryDraft,
) -> ClaimReview:
    """Review both draft structure and its rendered shareable text."""

    review = review_claims(summary_draft_to_markdown(draft))
    validation_issues = validate_summary_draft(draft)
    if not validation_issues:
        return review

    added = [
        _issue(
            "STRUCTURED_DRAFT_VALIDATION",
            "High",
            "Structured draft validation failed",
            validation_issue,
            (
                "A required evidence, confidence, boundary or limitation "
                "field is missing."
            ),
            "Regenerate the draft and retain all safety fields.",
        )
        for validation_issue in validation_issues
    ]
    issues = _deduplicate([*review.issues, *added])
    score = max(
        0,
        review.score - 25 * len(added),
    )
    return ClaimReview(
        status="Blocked",
        score=score,
        issues=issues,
        checks=review.checks,
    )
