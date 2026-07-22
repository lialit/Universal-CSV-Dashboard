import streamlit as st
DATA_KEY="analytics_dataframe"; CONFIG_KEY="analytics_config"; FILE_NAME_KEY="analytics_file_name"
def initialize_state():
    st.session_state.setdefault(DATA_KEY,None); st.session_state.setdefault(CONFIG_KEY,{}); st.session_state.setdefault(FILE_NAME_KEY,None)
def save_dataset(df,name): st.session_state[DATA_KEY]=df; st.session_state[FILE_NAME_KEY]=name
def save_config(config): st.session_state[CONFIG_KEY]=config
def get_dataset(): return st.session_state.get(DATA_KEY)
def get_config(): return st.session_state.get(CONFIG_KEY,{})
def require_dataset():
    initialize_state(); df=get_dataset(); config=get_config()
    if df is None or df.empty:
        st.warning("Upload and configure a CSV file on the **Upload & Configure** page first."); st.stop()
    return df,config
