import pandas as pd
def quality_summary(df):
    n=len(df); rows=[]
    for col in df.columns:
        m=int(df[col].isna().sum()); rows.append({"Column":col,"Data type":str(df[col].dtype),"Missing values":m,"Missing %":m/n*100 if n else 0,"Unique values":int(df[col].nunique(dropna=True))})
    return pd.DataFrame(rows)
def duplicate_count(df): return int(df.duplicated().sum())
