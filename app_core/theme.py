import streamlit as st
def apply_theme():
    st.markdown("""<style>.stApp{background:#F5F7FA}.block-container{max-width:1500px;padding-top:1.4rem;padding-bottom:2.5rem}[data-testid='stSidebar']{background:#FFF;border-right:1px solid #E6EBF2}h1,h2,h3{color:#102348}.page-title{color:#102348;font-size:2.2rem;line-height:1.15;font-weight:780;margin:0}.page-subtitle{color:#64748B;font-size:1rem;margin:.35rem 0 1.3rem}div[data-testid='stMetric'],div[data-testid='stPlotlyChart']{background:#FFF;border:1px solid #E4EAF2;border-radius:16px;box-shadow:0 5px 15px rgba(15,35,68,.04)}</style>""",unsafe_allow_html=True)
def render_header(title,subtitle):
    st.markdown(f'<p class="page-title">{title}</p>',unsafe_allow_html=True); st.markdown(f'<p class="page-subtitle">{subtitle}</p>',unsafe_allow_html=True)
