import pandas as pd
import streamlit as st

from app_core.charts import correlation_chart, distribution_chart
from app_core.insights import build_business_insights
from app_core.state import require_dataset
from app_core.theme import render_header


def render_insight_card(insight) -> None:
    with st.container(border=True):
        st.caption(insight.insight_type.upper())
        st.markdown(f"### {insight.title}")
        st.markdown(f"**Observation:** {insight.observation}")
        st.write(insight.interpretation)
        st.caption(f"Evidence: {insight.evidence}")
        confidence_message = (
            f"{insight.confidence} confidence — "
            f"{insight.confidence_reason}"
        )
        if insight.confidence == "High":
            st.success(confidence_message)
        elif insight.confidence == "Moderate":
            st.info(confidence_message)
        else:
            st.warning(confidence_message)
        st.warning(f"Limitation: {insight.limitation}")


dataframe, config = require_dataset()
metric = str(config["metric_column"])
numeric_columns = [
    column
    for column in (config.get("numeric_columns") or [])
    if column in dataframe.columns
]
numeric_columns = list(
    dict.fromkeys([metric, *numeric_columns])
)

render_header(
    "Business Insights",
    "Evidence-linked trends, contributions, anomalies and relationships.",
)

selected_metric = st.selectbox(
    "Metric to analyze",
    numeric_columns,
    index=(
        numeric_columns.index(metric)
        if metric in numeric_columns
        else 0
    ),
)
insight_config = {
    **config,
    "metric_column": selected_metric,
}
report = build_business_insights(dataframe, insight_config)

summary_columns = st.columns(4)
summary_columns[0].metric(
    "Insights detected",
    len(report.insights),
    border=True,
    width="stretch",
)
summary_columns[1].metric(
    "Metric analyzed",
    selected_metric,
    border=True,
    width="stretch",
)
summary_columns[2].metric(
    "Data quality",
    f"{report.quality_score:.1f}/100",
    help=report.quality_status,
    border=True,
    width="stretch",
)
summary_columns[3].metric(
    "Method",
    "Rule-based",
    border=True,
    width="stretch",
)

st.subheader("What deserves attention")
if report.insights:
    for start in range(0, len(report.insights), 2):
        columns = st.columns(2)
        for offset, insight in enumerate(
            report.insights[start : start + 2]
        ):
            with columns[offset]:
                render_insight_card(insight)
else:
    st.info(
        "No material pattern crossed the current thresholds. "
        "Try another metric or review the available exploratory charts."
    )

with st.expander("Suggested next analytical questions", expanded=True):
    for number, question in enumerate(report.questions, start=1):
        st.markdown(f"{number}. {question}")

if report.limitations:
    with st.expander("Analysis limitations"):
        for limitation in report.limitations:
            st.markdown(f"- {limitation}")

st.caption(
    "Insights are deterministic screening rules. They describe patterns in "
    "the selected data and do not establish causes or business impact. "
    "Confidence labels describe evidence reliability, not statistical "
    "certainty."
)

st.subheader("Explore the evidence")
left_chart, right_table = st.columns([1.4, 1])
with left_chart:
    st.plotly_chart(
        distribution_chart(dataframe, selected_metric),
        width="stretch",
    )
with right_table:
    st.dataframe(
        dataframe[numeric_columns]
        .apply(pd.to_numeric, errors="coerce")
        .describe()
        .T,
        width="stretch",
    )

if len(numeric_columns) >= 2:
    st.plotly_chart(
        correlation_chart(dataframe, numeric_columns),
        width="stretch",
    )
else:
    st.info(
        "Map at least two numeric columns to display a correlation matrix."
    )
