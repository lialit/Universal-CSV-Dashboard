import streamlit as st

from app_core.charts import missing_values_chart
from app_core.quality import (
    calculate_quality_score,
    quality_checks_table,
    quality_summary,
)
from app_core.state import require_dataset
from app_core.theme import render_header


@st.cache_data(show_spinner=False)
def cached_quality_report(dataframe):
    return calculate_quality_score(dataframe)


@st.cache_data(show_spinner=False)
def cached_quality_summary(dataframe):
    return quality_summary(dataframe)


@st.cache_data(show_spinner=False)
def cached_cleaned_csv(dataframe):
    return dataframe.drop_duplicates().to_csv(index=False).encode("utf-8")


dataframe, _ = require_dataset()

render_header(
    "Data Quality",
    (
        "Understand the reliability of the dataset before interpreting "
        "its results."
    ),
)

with st.spinner("Checking completeness, duplicates and type validity..."):
    report = cached_quality_report(dataframe)

status_messages = {
    "Excellent": st.success,
    "Good": st.info,
    "Needs attention": st.warning,
    "Critical": st.error,
}

score_column, rows_column, columns_column, issues_column = st.columns(4)

score_column.metric(
    "Data Quality Score",
    f"{report.score:.1f}/100",
    border=True,
    width="stretch",
)
rows_column.metric(
    "Rows",
    f"{report.rows:,}",
    border=True,
    width="stretch",
)
columns_column.metric(
    "Columns",
    f"{report.columns:,}",
    border=True,
    width="stretch",
)
issues_column.metric(
    "Detected issues",
    f"{report.issue_count:,}",
    border=True,
    width="stretch",
)

st.progress(
    report.score / 100,
    text=f"Overall status: {report.status}",
)

status_messages[report.status](
    (
        f"**{report.status}.** The score combines completeness (50%), "
        "duplicate-free rows (30%) and type validity (20%)."
    )
)

st.subheader("Score breakdown")

breakdown_columns = st.columns(len(report.checks))

for column, check in zip(
    breakdown_columns,
    report.checks,
    strict=True,
):
    column.metric(
        check.name,
        f"{check.score:.1f}/100",
        help=(
            f"Weight: {check.weight:.0%}. "
            f"{check.explanation}"
        ),
        border=True,
        width="stretch",
    )

with st.expander("How the score was calculated", expanded=True):
    checks = quality_checks_table(report)
    st.dataframe(
        checks.style.format(
            {
                "Score": "{:.1f}",
                "Weight": "{:.0%}",
                "Weighted points": "{:.1f}",
            }
        ),
        width="stretch",
        hide_index=True,
    )

st.subheader("Missing values")

if report.missing_cells:
    st.plotly_chart(
        missing_values_chart(dataframe),
        width="stretch",
    )
else:
    st.success(
        "No missing values were detected in the current dataset."
    )

st.subheader("Column-level quality")
with st.spinner("Preparing column-level quality details..."):
    column_summary = cached_quality_summary(dataframe)
st.dataframe(
    column_summary.style.format(
        {"Missing %": "{:.2f}%"}
    ),
    width="stretch",
    hide_index=True,
)

st.caption(
    (
        "The score describes observable technical quality. It does not prove "
        "that the data is accurate, unbiased or suitable for a business "
        "decision."
    )
)

with st.spinner("Preparing the de-duplicated download..."):
    cleaned_csv = cached_cleaned_csv(dataframe)

st.download_button(
    "Download de-duplicated CSV",
    data=cleaned_csv,
    file_name="cleaned_data.csv",
    mime="text/csv",
    width="stretch",
)
