import streamlit as st

from app_core.demo import load_demo_project
from app_core.state import (
    get_config,
    get_dataset,
    initialize_state,
    save_config,
    save_dataset,
)
from app_core.theme import render_header


initialize_state()

render_header(
    "Start Here",
    "Reach a useful business dashboard in under 60 seconds.",
)

st.caption(
    "Choose the synthetic demo for an instant product tour, or use your "
    "own CSV. Your uploaded data stays in this Streamlit session."
)

if get_dataset() is not None:
    config = get_config()
    st.success(
        "A dataset is already ready in this session. "
        f"Primary metric: **{config.get('metric_column', '—')}**."
    )
    continue_col, replace_col = st.columns(2)
    with continue_col:
        if st.button(
            "Continue to Executive Overview",
            type="primary",
            width="stretch",
        ):
            st.switch_page("views/overview.py")
    with replace_col:
        if st.button("Load another CSV", width="stretch"):
            st.switch_page("views/upload.py")
    st.stop()

st.subheader("Choose your starting point")
left, right = st.columns(2)

with left:
    with st.container(border=True):
        st.markdown("### Try demo data")
        st.write(
            "Explore a bundled synthetic business dataset with revenue, "
            "orders, margin, regions and sales channels."
        )
        st.caption("No upload, account, or external data required.")
        if st.button(
            "Try demo data",
            type="primary",
            width="stretch",
        ):
            dataframe, config, file_name = load_demo_project()
            save_dataset(dataframe, file_name)
            save_config(config)
            st.switch_page("views/overview.py")

with right:
    with st.container(border=True):
        st.markdown("### Use my CSV")
        st.write(
            "Upload your own CSV, review smart column suggestions and "
            "adjust the dashboard configuration before analysis."
        )
        st.caption("CSV processing remains local to this Streamlit session.")
        if st.button("Use my CSV", width="stretch"):
            st.switch_page("views/upload.py")

st.subheader("How it works")
steps = st.columns(4)
steps[0].markdown("**1. Load**\n\nDemo data or your CSV")
steps[1].markdown("**2. Validate**\n\nReview detected fields")
steps[2].markdown("**3. Explore**\n\nMetrics, insights, quality")
steps[3].markdown("**4. Export**\n\nShare Excel or PDF outputs")

st.info(
    "The bundled demo is synthetic and is safe to use in screenshots, "
    "tests and the future public live demo."
)
