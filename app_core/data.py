from io import BytesIO
import pandas as pd
import streamlit as st
@st.cache_data(show_spinner="Reading CSV...")
def read_csv_file(file_bytes):
    for enc in ("utf-8","utf-8-sig","cp1252","latin-1"):
        for sep in (",",";","\t"):
            try:
                df=pd.read_csv(BytesIO(file_bytes),encoding=enc,sep=sep)
                if df.shape[1]>1: return df
            except Exception: pass
    raise ValueError("The CSV could not be read with the supported encoding and separator combinations.")
def prepare_dataframe(df,date_column,numeric_columns):
    result=df.copy()
    if date_column: result[date_column]=pd.to_datetime(result[date_column],errors="coerce")
    for col in numeric_columns: result[col]=pd.to_numeric(result[col],errors="coerce")
    return result.convert_dtypes()
