import streamlit as st

from app_core.theme import apply_theme


st.set_page_config(
    page_title="CSV Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)
apply_theme()

pages = {
    "Dashboard": [
        st.Page(
            "views/start.py",
            title="Start Here",
            icon=":material/rocket_launch:",
            default=True,
        ),
        st.Page(
            "views/upload.py",
            title="Upload & Configure",
            icon=":material/upload_file:",
        ),
        st.Page(
            "views/overview.py",
            title="Executive Overview",
            icon=":material/dashboard:",
        ),
        st.Page(
            "views/analysis.py",
            title="Business Insights",
            icon=":material/insights:",
        ),
        st.Page(
            "views/assistant.py",
            title="Analysis Assistant",
            icon=":material/assistant:",
        ),
        st.Page(
            "views/quality.py",
            title="Data Quality",
            icon=":material/fact_check:",
        ),
    ],
    "Share": [
        st.Page(
            "views/export.py",
            title="Export & Share",
            icon=":material/ios_share:",
        ),
    ],
    "Product": [
        st.Page(
            "views/about.py",
            title="About This Template",
            icon=":material/info:",
        )
    ],
}

st.navigation(
    pages,
    position="sidebar",
    expanded=True,
).run()
