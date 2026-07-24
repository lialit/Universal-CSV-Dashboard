import streamlit as st

from app_core.assistant import (
    answer_guided_question,
    available_questions,
)
from app_core.state import require_dataset
from app_core.theme import render_header


def render_confidence(answer) -> None:
    message = f"{answer.confidence} confidence — {answer.confidence_reason}"
    if answer.confidence == "High":
        st.success(message)
    elif answer.confidence == "Moderate":
        st.info(message)
    else:
        st.warning(message)


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
labels = [question.label for question in questions]

with control_column:
    selected_label = st.selectbox(
        "What would you like to understand?",
        labels,
    )
    selected_question = next(
        question
        for question in questions
        if question.label == selected_label
    )
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

answer = answer_guided_question(
    dataframe,
    assistant_config,
    selected_question.key,
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

st.caption(
    "The assistant distinguishes calculation from interpretation. "
    "It does not infer causes, invent missing business context or replace "
    "human judgment."
)
