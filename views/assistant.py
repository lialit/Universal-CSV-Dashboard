import streamlit as st

from app_core.assistant import (
    OVERVIEW_QUESTION,
    answer_guided_question,
    available_questions,
    suggest_follow_up_questions,
)
from app_core.calculation_explainer import (
    calculation_for_question,
    calculation_options,
    explain_calculation,
)
from app_core.claim_guard import review_summary_draft
from app_core.state import require_dataset
from app_core.summary_drafts import (
    AUDIENCES,
    LENGTHS,
    build_summary_draft,
    summary_draft_to_markdown,
    summary_draft_to_text,
    validate_summary_draft,
)
from app_core.theme import render_header


def render_confidence(answer) -> None:
    message = f"{answer.confidence} confidence — {answer.confidence_reason}"
    if answer.confidence == "High":
        st.success(message)
    elif answer.confidence == "Moderate":
        st.info(message)
    else:
        st.warning(message)


@st.cache_data(show_spinner=False)
def cached_guided_answer(dataframe, config, question_key):
    return answer_guided_question(dataframe, config, question_key)


dataframe, config = require_dataset()
metric = str(config["metric_column"])
numeric_columns = [
    column
    for column in (config.get("numeric_columns") or [])
    if column in dataframe.columns
]
numeric_columns = list(dict.fromkeys([metric, *numeric_columns]))

render_header(
    "Analysis Assistant",
    "Ask a supported business question and receive a local, "
    "evidence-linked explanation.",
)

st.success(
    "**Private by design:** this version runs locally. Your CSV and its "
    "values are not sent to an external AI service."
)

control_column, context_column = st.columns([1.4, 1])
with control_column:
    selected_metric = st.selectbox(
        "Metric to explain",
        numeric_columns,
        index=(
            numeric_columns.index(metric)
            if metric in numeric_columns
            else 0
        ),
    )

assistant_config = {
    **config,
    "metric_column": selected_metric,
}
questions = available_questions(dataframe, assistant_config)
question_by_key = {
    question.key: question for question in questions
}
question_keys = list(question_by_key)
target_key = st.session_state.get(
    "assistant_follow_up_target",
    OVERVIEW_QUESTION,
)
if target_key not in question_by_key:
    target_key = OVERVIEW_QUESTION
selector_version = st.session_state.get(
    "assistant_selector_version",
    0,
)

with control_column:
    selected_key = st.selectbox(
        "What would you like to understand?",
        question_keys,
        index=question_keys.index(target_key),
        format_func=lambda key: question_by_key[key].label,
        key=f"assistant_question_selector_{selector_version}",
    )
    selected_question = question_by_key[selected_key]
    st.caption(selected_question.description)

with context_column:
    st.metric(
        "Analysis method",
        "Local rules",
        help=(
            "Deterministic calculations using the configured dataset. "
            "No external model or API is called."
        ),
        border=True,
        width="stretch",
    )
    st.caption(selected_question.availability_reason)

with st.spinner("Calculating a local evidence-linked answer..."):
    answer = cached_guided_answer(
        dataframe,
        assistant_config,
        selected_key,
    )

st.subheader("Assistant answer")
with st.container(border=True):
    st.caption(answer.method.upper())
    st.markdown(f"### {answer.headline}")
    st.write(answer.explanation)
    render_confidence(answer)

evidence_column, guidance_column = st.columns(2)
with evidence_column:
    st.markdown("#### Evidence")
    if answer.evidence:
        for item in answer.evidence:
            st.markdown(f"- {item}")
    else:
        st.info("No evidence was calculated for this question.")

with guidance_column:
    st.markdown("#### Recommended next steps")
    for number, next_step in enumerate(answer.next_steps, start=1):
        st.markdown(f"{number}. {next_step}")

with st.expander("Limitations and safe interpretation", expanded=True):
    for limitation in answer.limitations:
        st.markdown(f"- {limitation}")

with st.expander("How was this calculated?", expanded=False):
    options = calculation_options(dataframe, assistant_config)
    option_by_key = {
        option.key: option for option in options
    }
    option_keys = list(option_by_key)
    recommended_calculation = calculation_for_question(selected_key)
    selected_calculation = st.selectbox(
        "Calculation to explain",
        option_keys,
        index=option_keys.index(recommended_calculation),
        format_func=lambda key: option_by_key[key].label,
        key=(
            f"calculation_explainer_{selected_metric}_"
            f"{selected_key}"
        ),
    )
    calculation = explain_calculation(
        dataframe,
        assistant_config,
        selected_calculation,
    )

    result_column, rows_column, excluded_column = st.columns(3)
    result_column.metric(
        "Result",
        calculation.result,
        border=True,
        width="stretch",
    )
    rows_column.metric(
        "Included rows",
        f"{calculation.included_rows:,}",
        border=True,
        width="stretch",
    )
    excluded_column.metric(
        "Excluded rows",
        f"{calculation.excluded_rows:,}",
        border=True,
        width="stretch",
    )

    st.markdown("#### Formula")
    st.code(calculation.formula, language=None)

    detail_column, field_column = st.columns(2)
    with detail_column:
        st.markdown("#### Aggregation")
        st.write(calculation.aggregation)
    with field_column:
        st.markdown("#### Fields used")
        if calculation.fields:
            st.write(", ".join(calculation.fields))
        else:
            st.write("No fields were used.")

    st.markdown("#### Calculation steps")
    for number, step in enumerate(
        calculation.steps,
        start=1,
    ):
        st.markdown(f"**{number}. {step.label}**")
        st.write(step.detail)

    assumption_column, calculation_limit_column = st.columns(2)
    with assumption_column:
        st.markdown("#### Assumptions")
        if calculation.assumptions:
            for assumption in calculation.assumptions:
                st.markdown(f"- {assumption}")
        else:
            st.write("No additional assumptions.")
    with calculation_limit_column:
        st.markdown("#### Calculation limitations")
        for limitation in calculation.limitations:
            st.markdown(f"- {limitation}")

with st.expander("Draft an evidence-based summary", expanded=False):
    draft_control_column, detail_control_column = st.columns(2)
    with draft_control_column:
        draft_audience = st.selectbox(
            "Audience",
            AUDIENCES,
            key=f"summary_audience_{selected_metric}",
        )
    with detail_control_column:
        draft_length = st.selectbox(
            "Detail level",
            LENGTHS,
            index=LENGTHS.index("Standard"),
            key=f"summary_length_{selected_metric}",
        )

    draft = build_summary_draft(
        dataframe,
        assistant_config,
        audience=draft_audience,
        length=draft_length,
    )
    validation_issues = validate_summary_draft(draft)
    claim_review = review_summary_draft(draft)
    markdown_draft = summary_draft_to_markdown(draft)
    text_draft = summary_draft_to_text(draft)

    draft_metrics = st.columns(4)
    draft_metrics[0].metric(
        "Evidence-linked claims",
        draft.evidence_count,
        border=True,
        width="stretch",
    )
    draft_metrics[1].metric(
        "Interpretations",
        len(draft.interpretations),
        border=True,
        width="stretch",
    )
    draft_metrics[2].metric(
        "Limitations",
        len(draft.limitations),
        border=True,
        width="stretch",
    )
    draft_metrics[3].metric(
        "Claim safety",
        claim_review.status,
        help=f"Safety score: {claim_review.score}/100",
        border=True,
        width="stretch",
    )

    if validation_issues:
        st.warning(
            "The draft needs review before sharing: "
            + " ".join(validation_issues)
        )
    else:
        st.success(
            "Every included claim has evidence and all interpretations "
            "retain confidence and limitation context."
        )

    st.markdown(markdown_draft)

    st.markdown("#### Pre-share Claim Guard")
    guard_columns = st.columns(4)
    guard_columns[0].metric(
        "Safety score",
        f"{claim_review.score}/100",
        border=True,
        width="stretch",
    )
    guard_columns[1].metric(
        "Status",
        claim_review.status,
        border=True,
        width="stretch",
    )
    guard_columns[2].metric(
        "Issues",
        len(claim_review.issues),
        border=True,
        width="stretch",
    )
    guard_columns[3].metric(
        "High-risk",
        claim_review.high_risk_count,
        border=True,
        width="stretch",
    )

    if claim_review.status == "Ready":
        st.success(
            "Ready to share. No unsupported claim pattern was detected."
        )
    elif claim_review.status == "Review":
        st.warning(
            "Review the flagged wording before sharing this summary."
        )
    else:
        st.error(
            "Sharing is blocked until the high-risk claims are resolved."
        )

    if claim_review.issues:
        for issue in claim_review.issues:
            with st.container(border=True):
                st.markdown(
                    f"**{issue.severity}: {issue.title}**"
                )
                st.write(issue.matched_text)
                st.caption(issue.explanation)
                st.info(f"Safer wording: {issue.safe_rewrite}")
    else:
        st.caption(
            "Checked causal language, predictions, certainty, directive "
            "recommendations, invented context and safety structure."
        )

    downloads_disabled = (
        bool(validation_issues)
        or not claim_review.ready_for_export
    )
    markdown_column, text_column = st.columns(2)
    with markdown_column:
        st.download_button(
            "Download Markdown",
            data=markdown_draft.encode("utf-8"),
            file_name="evidence_based_summary.md",
            mime="text/markdown",
            disabled=downloads_disabled,
            width="stretch",
        )
    with text_column:
        st.download_button(
            "Download plain text",
            data=text_draft.encode("utf-8"),
            file_name="evidence_based_summary.txt",
            mime="text/plain",
            disabled=downloads_disabled,
            width="stretch",
        )

follow_ups = suggest_follow_up_questions(
    dataframe,
    assistant_config,
    current_question_key=selected_key,
)
st.subheader("Suggested follow-up questions")
if follow_ups:
    follow_up_columns = st.columns(len(follow_ups))
    for column, follow_up in zip(
        follow_up_columns,
        follow_ups,
        strict=True,
    ):
        with column:
            with st.container(border=True):
                st.caption(follow_up.source.upper())
                st.markdown(f"**{follow_up.label}**")
                st.write(follow_up.rationale)
                if st.button(
                    "Ask next",
                    key=(
                        f"follow_up_{selected_metric}_"
                        f"{selected_key}_{follow_up.question_key}"
                    ),
                    width="stretch",
                ):
                    st.session_state[
                        "assistant_follow_up_target"
                    ] = follow_up.question_key
                    st.session_state[
                        "assistant_selector_version"
                    ] = selector_version + 1
                    st.rerun()
else:
    st.info(
        "No additional supported question is available for the current "
        "configuration."
    )

st.caption(
    "The assistant distinguishes calculation from interpretation. "
    "It does not infer causes, invent missing business context or replace "
    "human judgment."
)
