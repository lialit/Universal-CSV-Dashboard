import pandas as pd
import streamlit as st
from app_core.state import require_dataset
from app_core.theme import render_header
from app_core.charts import distribution_chart,correlation_chart
df,cfg=require_dataset(); nums=[c for c in cfg.get('numeric_columns',[]) if c in df.columns]; metric=str(cfg['metric_column'])
render_header("Data Analysis","Explore distributions, descriptive statistics and correlations.")
selected=st.selectbox("Metric to analyze",nums,index=nums.index(metric) if metric in nums else 0); l,r=st.columns([1.4,1])
with l: st.plotly_chart(distribution_chart(df,selected),width="stretch")
with r: st.dataframe(df[nums].apply(pd.to_numeric,errors='coerce').describe().T,width="stretch")
if len(nums)>=2: st.plotly_chart(correlation_chart(df,nums),width="stretch")
else: st.info("Map at least two numeric columns to display a correlation matrix.")
