import streamlit as st

from app_core.charts import (
    category_chart,
    correlation_chart,
    distribution_chart,
    time_series_chart,
)
from app_core.executive_summary import (
    SummaryStatement,
    build_executive_summary,
)
from app_core.formatting import compact_number
from app_core.metrics import recent_metric_series, summarize_metric
from app_core.recommendations import recommend_analysis
from app_core.session_cache import session_result, stable_mapping_key
from app_core.state import require_dataset
from app_core.theme import render_header


def render_statements(
    title: str,
    statements: tuple[SummaryStatement, ...],
    empty_message: str,
) -> None:
    st.markdown(f"#### {title}")
    if not statements:
        st.info(empty_message)
        return

    for statement in statements:
        with st.container(border=True):
            st.markdown(f"**{statement.title}**")
            st.write(statement.text)
            st.caption(f"Evidence: {statement.evidence}")


def render_kpis(dataframe, config, metric: str) -> None:
    metric_summary = summarize_metric(dataframe, metric)
    sparkline = recent_metric_series(
        dataframe,
        config.get("date_column"),
        metric,
    )
    fallback = recommend_analysis(dataframe, config)
    selected = (
        config["kpi_cards"]
        if "kpi_cards" in config
        else list(fallback.kpis)
    )

    values = {
        "Total": metric_summary.total,
        "Average": metric_summary.average,
        "Median": metric_summary.median,
        "Minimum": metric_summary.minimum,
        "Maximum": metric_summary.maximum,
        "Non-null count": metric_summary.non_null_count,
    }
    selected = [item for item in selected if item in values][:3]
    columns = st.columns(len(selected) + 2)

    for index, item in enumerate(selected):
        kwargs = {}
        if item == "Total":
            kwargs = {
                "chart_data": sparkline,
                "chart_type": "area",
            }
        columns[index].metric(
            f"{item} {metric}",
            compact_number(values[item]),
            border=True,
            width="stretch",
            height="stretch",
            **kwargs,
        )

    columns[-2].metric(
        "Rows",
        f"{len(dataframe):,}",
        border=True,
        width="stretch",
        height="stretch",
    )
    columns[-1].metric(
        "Columns",
        f"{len(dataframe.columns):,}",
        border=True,
        width="stretch",
        height="stretch",
    )


def build_charts(dataframe, config, metric: str):
    aggregation = str(config.get("aggregation", "Sum"))
    date_column = config.get("date_column")
    category_column = config.get("category_column")
    fallback = recommend_analysis(dataframe, config)
    selected = (
        config["chart_types"]
        if "chart_types" in config
        else list(fallback.charts)
    )
    charts = []

    for chart_type in selected:
        if chart_type == "Time series" and date_column:
            charts.append(
                time_series_chart(
                    dataframe,
                    date_column,
                    metric,
                    aggregation,
                )
            )
        elif chart_type == "Category comparison" and category_column:
            charts.append(
                category_chart(
                    dataframe,
                    category_column,
                    metric,
                    aggregation,
                )
            )
        elif chart_type == "Distribution":
            charts.append(distribution_chart(dataframe, metric))
        elif chart_type == "Correlation matrix":
            numeric_columns = [
                column
                for column in config.get("numeric_columns", [])
                if column in dataframe.columns
            ]
            numeric_columns = list(
                dict.fromkeys([metric, *numeric_columns])
            )
            if len(numeric_columns) >= 2:
                charts.append(
                    correlation_chart(dataframe, numeric_columns)
                )

    return charts


dataframe, config = require_dataset()
metric = str(config["metric_column"])
date_column = config.get("date_column")
category_column = config.get("category_column")

render_header(
    "Executive Overview",
    "Headline metrics, verified facts and transparent rule-based "
    "interpretations.",
)

filtered = dataframe.copy()
filter_key = []
filter_box = st.sidebar.container(border=True)
filter_box.markdown("### Dashboard filters")

if date_column:
    valid_dates = filtered[date_column].dropna()
    if not valid_dates.empty:
        minimum_date = valid_dates.min().date()
        maximum_date = valid_dates.max().date()
        selected_dates = filter_box.date_input(
            "Date range",
            value=(minimum_date, maximum_date),
            min_value=minimum_date,
            max_value=maximum_date,
        )
        if (
            isinstance(selected_dates, tuple)
            and len(selected_dates) == 2
        ):
            filter_key.append(
                ("dates", *(item.isoformat() for item in selected_dates))
            )
            filtered = filtered[
                filtered[date_column].dt.date.between(
                    *selected_dates
                )
            ]

if category_column:
    category_values = sorted(
        filtered[category_column]
        .astype("string")
        .dropna()
        .unique()
        .tolist()
    )
    selected_categories = filter_box.multiselect(
        category_column,
        category_values,
        default=category_values,
    )
    filter_key.append(("categories", *selected_categories))
    filtered = filtered[
        filtered[category_column]
        .astype("string")
        .isin(selected_categories)
    ]

if filtered.empty:
    st.warning("No rows match the selected filters.")
    st.stop()

render_kpis(filtered, config, metric)

st.subheader("Executive summary")
with st.spinner("Calculating the executive summary..."):
    summary = session_result(
        dataframe,
        (
            "executive-summary",
            tuple(filter_key),
            stable_mapping_key(config),
        ),
        lambda: build_executive_summary(filtered, config),
    )
st.info(summary.headline)
facts_column, interpretation_column = st.columns(2)

with facts_column:
    render_statements(
        "Verified facts",
        summary.facts,
        "No verified facts are available.",
    )

with interpretation_column:
    render_statements(
        "Rule-based interpretations",
        summary.interpretations,
        "No material pattern crossed the current interpretation "
        "thresholds.",
    )

with st.expander("Limitations and recommended next steps"):
    limitation_column, next_step_column = st.columns(2)
    with limitation_column:
        render_statements(
            "Limitations",
            summary.limitations,
            "No material limitations were detected by the current rules.",
        )
    with next_step_column:
        st.markdown("#### Recommended next steps")
        for number, next_step in enumerate(
            summary.next_steps,
            start=1,
        ):
            st.markdown(f"{number}. {next_step}")

st.caption(
    "Facts are calculated directly from the selected data. "
    "Interpretations are deterministic rules, not causal claims or "
    "AI-generated conclusions."
)
st.write("")

with st.spinner("Preparing the charts..."):
    charts = session_result(
        dataframe,
        (
            "overview-charts",
            tuple(filter_key),
            metric,
            stable_mapping_key(config),
        ),
        lambda: build_charts(filtered, config, metric),
    )
for start in range(0, len(charts), 2):
    row = st.columns(2)
    for offset, figure in enumerate(charts[start : start + 2]):
        with row[offset]:
            st.plotly_chart(figure, width="stretch")

with st.expander("Filtered data preview"):
    st.dataframe(
        filtered.head(200),
        width="stretch",
        hide_index=True,
    )
