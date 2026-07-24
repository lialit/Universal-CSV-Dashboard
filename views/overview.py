import streamlit as st

from app_core.charts import (
    category_chart,
    time_series_chart,
)
from app_core.executive_summary import (
    SummaryStatement,
    build_executive_summary,
)
from app_core.formatting import compact_number
from app_core.metrics import (
    recent_metric_series,
    summarize_metric,
)
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


dataframe, config = require_dataset()
metric = str(config["metric_column"])
date_column = config.get("date_column")
category_column = config.get("category_column")
aggregation = str(config.get("aggregation", "Sum"))

render_header(
    "Executive Overview",
    (
        "Headline metrics, verified facts and transparent rule-based "
        "interpretations."
    ),
)

filtered = dataframe.copy()
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
    filtered = filtered[
        filtered[category_column]
        .astype("string")
        .isin(selected_categories)
    ]

if filtered.empty:
    st.warning("No rows match the selected filters.")
    st.stop()

metric_summary = summarize_metric(filtered, metric)
sparkline = recent_metric_series(
    filtered,
    date_column,
    metric,
)
metric_columns = st.columns(5)

metric_columns[0].metric(
    f"Total {metric}",
    compact_number(metric_summary.total),
    chart_data=sparkline,
    chart_type="area",
    border=True,
    width="stretch",
    height="stretch",
)
metric_columns[1].metric(
    f"Average {metric}",
    compact_number(metric_summary.average),
    border=True,
    width="stretch",
    height="stretch",
)
metric_columns[2].metric(
    f"Median {metric}",
    compact_number(metric_summary.median),
    border=True,
    width="stretch",
    height="stretch",
)
metric_columns[3].metric(
    "Rows",
    f"{len(filtered):,}",
    border=True,
    width="stretch",
    height="stretch",
)
metric_columns[4].metric(
    "Columns",
    f"{len(filtered.columns):,}",
    border=True,
    width="stretch",
    height="stretch",
)

st.subheader("Executive summary")
summary = build_executive_summary(filtered, config)
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
        (
            "No material pattern crossed the current interpretation "
            "thresholds."
        ),
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
    (
        "Facts are calculated directly from the selected data. "
        "Interpretations are deterministic rules, not causal claims or "
        "AI-generated conclusions."
    )
)

st.write("")

if date_column and category_column:
    left_chart, right_chart = st.columns(2)

    with left_chart:
        st.plotly_chart(
            time_series_chart(
                filtered,
                date_column,
                metric,
                aggregation,
            ),
            width="stretch",
        )

    with right_chart:
        st.plotly_chart(
            category_chart(
                filtered,
                category_column,
                metric,
                aggregation,
            ),
            width="stretch",
        )
elif date_column:
    st.plotly_chart(
        time_series_chart(
            filtered,
            date_column,
            metric,
            aggregation,
        ),
        width="stretch",
    )
elif category_column:
    st.plotly_chart(
        category_chart(
            filtered,
            category_column,
            metric,
            aggregation,
        ),
        width="stretch",
    )

with st.expander("Filtered data preview"):
    st.dataframe(
        filtered.head(200),
        width="stretch",
        hide_index=True,
    )
