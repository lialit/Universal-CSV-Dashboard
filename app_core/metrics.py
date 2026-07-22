from dataclasses import dataclass
import pandas as pd
@dataclass(frozen=True)
class MetricSummary: total:float; average:float; median:float; minimum:float; maximum:float; non_null_count:int
def summarize_metric(df,col):
    s=pd.to_numeric(df[col],errors="coerce")
    return MetricSummary(float(s.sum()),float(s.mean()),float(s.median()),float(s.min()),float(s.max()),int(s.notna().sum()))
def recent_metric_series(df,date_column,metric_column,periods=30):
    if not date_column: return pd.to_numeric(df[metric_column],errors="coerce").dropna().tail(periods).astype(float).tolist()
    return df.dropna(subset=[date_column]).set_index(date_column)[metric_column].apply(pd.to_numeric,errors="coerce").resample("D").sum().tail(periods).astype(float).tolist()
