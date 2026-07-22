import pandas as pd
import plotly.express as px
def layout(fig,height=380):
    fig.update_layout(height=height,margin=dict(l=20,r=20,t=60,b=20),paper_bgcolor="#FFF",plot_bgcolor="#FFF",font=dict(family="Inter, Arial, sans-serif",color="#334155"),title_font=dict(size=17,color="#102348"),legend_title_text="",hoverlabel=dict(bgcolor="#FFF")); fig.update_xaxes(gridcolor="#E8EDF4",zeroline=False); fig.update_yaxes(gridcolor="#E8EDF4",zeroline=False); return fig
def time_series_chart(df,date_column,metric_column,aggregation):
    fn={"Sum":"sum","Mean":"mean","Median":"median","Count":"count"}[aggregation]; g=df.dropna(subset=[date_column]).set_index(date_column).resample("D")[metric_column].agg(fn).reset_index(); fig=px.line(g,x=date_column,y=metric_column,title=f"{aggregation} of {metric_column} over time"); fig.update_traces(line=dict(width=2.5),fill="tozeroy"); return layout(fig)
def category_chart(df,category_column,metric_column,aggregation,limit=15):
    fn={"Sum":"sum","Mean":"mean","Median":"median","Count":"count"}[aggregation]; g=df.groupby(category_column,dropna=False,as_index=False)[metric_column].agg(fn).nlargest(limit,metric_column).sort_values(metric_column); g[category_column]=g[category_column].astype("string").fillna("Missing"); return layout(px.bar(g,x=metric_column,y=category_column,orientation="h",title=f"Top {limit} {category_column} values by {aggregation.lower()} {metric_column}"))
def distribution_chart(df,metric_column): return layout(px.histogram(df,x=metric_column,nbins=35,marginal="box",title=f"Distribution of {metric_column}"))
def missing_values_chart(df):
    g=df.isna().mean().mul(100).sort_values(ascending=False).rename("missing_pct").reset_index().rename(columns={"index": "column"}); return layout(px.bar(g,x="missing_pct",y="column",orientation="h",title="Missing values by column",labels={"missing_pct":"Missing (%)"}),max(380,len(g)*28))
def correlation_chart(df,numeric_columns):
    corr=df[numeric_columns].apply(pd.to_numeric,errors="coerce").corr(); return layout(px.imshow(corr,text_auto=".2f",aspect="auto",title="Numeric correlation matrix",color_continuous_scale="RdBu_r",zmin=-1,zmax=1),max(420,len(numeric_columns)*60))
