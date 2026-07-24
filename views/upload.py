import json

import streamlit as st

from app_core.data import prepare_dataframe, read_csv_file
from app_core.recommendations import (
    KPI_OPTIONS,
    recommend_analysis,
    recommendations_table,
)
from app_core.smart_detection import detect_dataset, detection_table
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
    "Upload & Configure",
    "Upload a CSV and let the Smart Detection Engine "
    "prepare a dashboard configuration automatically.",
)

uploaded_file = st.file_uploader(
    "Upload CSV",
    type=["csv"],
    max_upload_size=200,
    help=(
        "Supported delimiters: comma, semicolon and tab. "
        "Common encodings are detected automatically."
    ),
)

if uploaded_file is not None:
    try:
        raw_dataframe = read_csv_file(uploaded_file.getvalue())
    except ValueError as error:
        st.error(str(error))
        st.stop()

    st.success(
        f"Loaded {len(raw_dataframe):,} rows and "
        f"{len(raw_dataframe.columns):,} columns."
    )

    with st.spinner("Analyzing dataset structure..."):
        detection = detect_dataset(raw_dataframe)

    st.subheader("Smart suggestions")
    summary_columns = st.columns(4)
    summary_columns[0].metric(
        "Date",
        detection.date_column or "Not detected",
        border=True,
        width="stretch",
    )
    summary_columns[1].metric(
        "Primary metric",
        detection.metric_column or "Not detected",
        border=True,
        width="stretch",
    )
    summary_columns[2].metric(
        "Category",
        detection.category_column or "Not detected",
        border=True,
        width="stretch",
    )
    summary_columns[3].metric(
        "Numeric columns",
        str(len(detection.numeric_columns)),
        border=True,
        width="stretch",
    )

    with st.expander("Why these columns were suggested"):
        st.dataframe(
            detection_table(detection).style.format(
                {"Confidence": "{:.0%}"}
            ),
            width="stretch",
            hide_index=True,
        )

    with st.expander("Data preview", expanded=True):
        st.dataframe(
            raw_dataframe.head(100),
            width="stretch",
            hide_index=True,
        )

    columns = raw_dataframe.columns.tolist()
    date_column = st.selectbox(
        "Date or timestamp column",
        options=[None, *columns],
        index=(
            columns.index(detection.date_column) + 1
            if detection.date_column in columns
            else 0
        ),
        format_func=lambda value: (
            "No date column" if value is None else value
        ),
    )

    metric_options = (
        list(detection.numeric_columns)
        or raw_dataframe.select_dtypes(
            include="number"
        ).columns.tolist()
        or columns
    )
    metric_column = st.selectbox(
        "Primary numeric metric",
        options=metric_options,
        index=(
            metric_options.index(detection.metric_column)
            if detection.metric_column in metric_options
            else 0
        ),
    )

    additional_numeric_options = [
        column for column in columns if column != metric_column
    ]
    suggested_additional = [
        column
        for column in detection.numeric_columns
        if column != metric_column
    ][:6]
    additional_numeric = st.multiselect(
        "Additional numeric columns",
        options=additional_numeric_options,
        default=suggested_additional,
    )

    category_column = st.selectbox(
        "Primary category column",
        options=[None, *columns],
        index=(
            columns.index(detection.category_column) + 1
            if detection.category_column in columns
            else 0
        ),
        format_func=lambda value: (
            "No category column" if value is None else value
        ),
    )
    aggregation = st.selectbox(
        "Default aggregation",
        options=["Sum", "Mean", "Median", "Count"],
    )

    numeric_columns = list(
        dict.fromkeys([metric_column, *additional_numeric])
    )
    prepared = prepare_dataframe(
        raw_dataframe,
        date_column=date_column,
        numeric_columns=numeric_columns,
    )

    draft_config = {
        "date_column": date_column,
        "metric_column": metric_column,
        "numeric_columns": numeric_columns,
        "category_column": category_column,
        "aggregation": aggregation,
    }
    recommendations = recommend_analysis(prepared, draft_config)

    st.subheader("Dashboard composition")
    st.caption(
        "Recommended from the selected fields. You remain in control "
        "and can change the final dashboard."
    )

    kpi_cards = st.multiselect(
        "KPI cards",
        options=KPI_OPTIONS,
        default=recommendations.kpis,
        max_selections=3,
    )
    chart_types = st.multiselect(
        "Dashboard charts",
        options=recommendations.available_charts,
        default=recommendations.charts,
        max_selections=4,
    )

    with st.expander("Why this composition was recommended"):
        st.dataframe(
            recommendations_table(recommendations),
            width="stretch",
            hide_index=True,
        )

    config_json = {
        **draft_config,
        "kpi_cards": kpi_cards,
        "chart_types": chart_types,
    }
    left, right = st.columns(2)

    with left:
        accept_clicked = st.button(
            "Accept smart configuration",
            type="primary",
            width="stretch",
        )

    with right:
        st.download_button(
            "Download configuration JSON",
            data=json.dumps(config_json, indent=2),
            file_name="dashboard_config.json",
            mime="application/json",
            width="stretch",
        )

    if accept_clicked:
        save_dataset(prepared, uploaded_file.name)
        save_config(config_json)
        st.success(
            "Configuration saved. Open "
            "**Executive Overview** in the sidebar."
        )

elif get_dataset() is not None:
    config = get_config()
    st.info(
        "A dataset is already loaded for this session. "
        f"Primary metric: "
        f"**{config.get('metric_column', '—')}**."
    )
