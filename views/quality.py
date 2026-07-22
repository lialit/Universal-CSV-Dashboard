import streamlit as st
from app_core.state import require_dataset
from app_core.theme import render_header
from app_core.quality import quality_summary,duplicate_count
from app_core.charts import missing_values_chart
df,_=require_dataset(); render_header("Data Quality","Inspect missing values, duplicate rows and column-level quality.")
dup=duplicate_count(df); missing=int(df.isna().sum().sum()); total=df.shape[0]*df.shape[1]; rate=missing/total if total else 0; c=st.columns(4)
c[0].metric("Rows",f"{len(df):,}",border=True,width="stretch"); c[1].metric("Columns",f"{len(df.columns):,}",border=True,width="stretch"); c[2].metric("Duplicate rows",f"{dup:,}",border=True,width="stretch"); c[3].metric("Missing cells",f"{rate:.2%}",border=True,width="stretch")
st.plotly_chart(missing_values_chart(df),width="stretch"); st.dataframe(quality_summary(df).style.format({'Missing %':'{:.2f}%'}),width="stretch",hide_index=True)
st.download_button("Download de-duplicated CSV",data=df.drop_duplicates().to_csv(index=False).encode('utf-8'),file_name='cleaned_data.csv',mime='text/csv',width="stretch")
