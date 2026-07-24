import streamlit as st

from app_core.exports import build_excel_report
from app_core.pdf_exports import build_pdf_report
from app_core.state import FILE_NAME_KEY, require_dataset
from app_core.theme import render_header


dataframe, config = require_dataset()
source_name = st.session_state.get(FILE_NAME_KEY) or "uploaded.csv"

render_header(
    "Export & Share",
    "Create traceable Excel and executive PDF reports with quality "
    "context, evidence and visible limitations.",
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
    "Formats",
    "Excel + PDF",
    border=True,
    width="stretch",
)

excel_tab, pdf_tab = st.tabs(
    ["Excel workbook", "Executive PDF"]
)

with excel_tab:
    st.subheader("Structured Excel analysis")
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
        "The Excel workbook contains the complete prepared dataset. "
        "Review its sensitivity before sharing it."
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
        export_name = (
            source_name.rsplit(".", 1)[0]
            + "_analysis.xlsx"
        )
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

with pdf_tab:
    st.subheader("Executive PDF report")
    st.markdown(
        """
- Executive KPI snapshot and analysis scope.
- Data Quality Score and detected issue count.
- Evidence-linked business insights with confidence and limitations.
- Suggested next analytical questions.
- Methodology and responsible-use notes.
"""
    )
    st.info(
        "The PDF does not include the complete row-level dataset. "
        "It is designed for concise review and safer sharing."
    )
    try:
        with st.spinner("Preparing executive PDF..."):
            pdf_bytes = build_pdf_report(
                dataframe,
                config,
                source_name,
            )
    except ValueError as error:
        st.error(str(error))
    else:
        pdf_name = (
            source_name.rsplit(".", 1)[0]
            + "_executive_report.pdf"
        )
        st.download_button(
            "Download executive PDF",
            data=pdf_bytes,
            file_name=pdf_name,
            mime="application/pdf",
            type="primary",
            width="stretch",
        )
        st.caption(
            f"PDF size: {len(pdf_bytes) / 1024:.1f} KB. "
            "Generated locally from the current analysis."
        )
