import streamlit as st

from app_core.session_cache import clear_session_results


DATA_KEY = "analytics_dataframe"
CONFIG_KEY = "analytics_config"
FILE_NAME_KEY = "analytics_file_name"


def initialize_state() -> None:
    st.session_state.setdefault(DATA_KEY, None)
    st.session_state.setdefault(CONFIG_KEY, {})
    st.session_state.setdefault(FILE_NAME_KEY, None)


def save_dataset(df, name) -> None:
    if st.session_state.get(DATA_KEY) is not df:
        clear_session_results()
    st.session_state[DATA_KEY] = df
    st.session_state[FILE_NAME_KEY] = name


def save_config(config) -> None:
    st.session_state[CONFIG_KEY] = config


def get_dataset():
    return st.session_state.get(DATA_KEY)


def get_config():
    return st.session_state.get(CONFIG_KEY, {})


def require_dataset():
    initialize_state()
    dataframe = get_dataset()
    config = get_config()
    if dataframe is None or dataframe.empty:
        st.warning(
            "No dataset is loaded yet. Start with the bundled demo or upload "
            "your own CSV to continue."
        )
        left, right = st.columns(2)
        with left:
            st.page_link(
                "views/start.py",
                label="Go to Start Here",
                icon=":material/rocket_launch:",
                width="stretch",
            )
        with right:
            st.page_link(
                "views/upload.py",
                label="Upload a CSV",
                icon=":material/upload_file:",
                width="stretch",
            )
        st.stop()
    return dataframe, config
