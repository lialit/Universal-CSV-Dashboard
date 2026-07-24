import streamlit as st

from app_core.exports import build_excel_report
from app_core.state import FILE_NAME_KEY, require_dataset
from app_core.theme import render_header


dataframe, config = require_dataset()
source_name = st.session_state.get(FILE_NAME_KEY) or "uploaded.csv"

render_header(
    "Export & Share",
    "Create a traceable Excel report with data, configuration, quality "
    "context and evidence-linked insights.",
)

summary = st.columns(4)
summary[0].metric(
    "Rows",
    f"{len(dataframe):,}",
    border=True,
    width="stretch",
)
summary[1].metric(
    "Columns",
    f"{len(dataframe.columns):,}",
    border=True,
    width="stretch",
)
summary[2].metric(
    "Primary metric",
    str(config.get("metric_column", "—")),
    border=True,
    width="stretch",
)
summary[3].metric(
    "Format",
    "Excel (.xlsx)",
    border=True,
    width="stretch",
)

st.subheader("Workbook contents")
st.markdown(
    """
- **Overview** — source metadata and formula-driven KPI summary.
- **Data Quality** — score components, issues and recommended actions.
- **Business Insights** — observations, evidence, confidence and limitations.
- **Configuration** — selected fields, aggregation, KPI and chart choices.
- **Data** — the complete prepared dataset used by the application.
- **Methodology** — calculation rules and responsible-use notes.
"""
)

st.warning(
    "The exported workbook contains the complete prepared dataset. "
    "Review its sensitivity before sharing it with another person."
)

try:
    with st.spinner("Preparing Excel workbook..."):
        workbook_bytes = build_excel_report(
            dataframe,
            config,
            source_name,
        )
except ValueError as error:
    st.error(str(error))
else:
    export_name = source_name.rsplit(".", 1)[0] + "_analysis.xlsx"
    st.download_button(
        "Download Excel analysis",
        data=workbook_bytes,
        file_name=export_name,
        mime=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        ),
        type="primary",
        width="stretch",
    )
    st.caption(
        f"Workbook size: {len(workbook_bytes) / 1024:.1f} KB. "
        "The source CSV is not modified."
    )
