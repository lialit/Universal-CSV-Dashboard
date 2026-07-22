import streamlit as st
from app_core.state import require_dataset
from app_core.theme import render_header
from app_core.metrics import summarize_metric,recent_metric_series
from app_core.formatting import compact_number
from app_core.charts import time_series_chart,category_chart
df,cfg=require_dataset(); metric=str(cfg['metric_column']); date=cfg.get('date_column'); category=cfg.get('category_column'); agg=str(cfg.get('aggregation','Sum'))
render_header("Executive Overview","Headline metrics and automatically generated business views.")
filtered=df.copy(); box=st.sidebar.container(border=True); box.markdown("### Dashboard filters")
if date:
    valid=filtered[date].dropna()
    if not valid.empty:
        mn,mx=valid.min().date(),valid.max().date(); chosen=box.date_input("Date range",value=(mn,mx),min_value=mn,max_value=mx)
        if isinstance(chosen,tuple) and len(chosen)==2: filtered=filtered[filtered[date].dt.date.between(*chosen)]
if category:
    values=sorted(filtered[category].astype('string').dropna().unique().tolist()); selected=box.multiselect(category,values,default=values); filtered=filtered[filtered[category].astype('string').isin(selected)]
if filtered.empty: st.warning("No rows match the selected filters."); st.stop()
s=summarize_metric(filtered,metric); spark=recent_metric_series(filtered,date,metric); c=st.columns(5)
c[0].metric(f"Total {metric}",compact_number(s.total),chart_data=spark,chart_type="area",border=True,width="stretch",height="stretch"); c[1].metric(f"Average {metric}",compact_number(s.average),border=True,width="stretch",height="stretch"); c[2].metric(f"Median {metric}",compact_number(s.median),border=True,width="stretch",height="stretch"); c[3].metric("Rows",f"{len(filtered):,}",border=True,width="stretch",height="stretch"); c[4].metric("Columns",f"{len(filtered.columns):,}",border=True,width="stretch",height="stretch")
st.write("")
if date and category:
    l,r=st.columns(2)
    with l: st.plotly_chart(time_series_chart(filtered,date,metric,agg),width="stretch")
    with r: st.plotly_chart(category_chart(filtered,category,metric,agg),width="stretch")
elif date: st.plotly_chart(time_series_chart(filtered,date,metric,agg),width="stretch")
elif category: st.plotly_chart(category_chart(filtered,category,metric,agg),width="stretch")
with st.expander("Filtered data preview"): st.dataframe(filtered.head(200),width="stretch",hide_index=True)
