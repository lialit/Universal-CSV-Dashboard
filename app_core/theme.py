import streamlit as st


def apply_theme() -> None:
    st.markdown(
        """
        <style>
        .stApp {
            background: #F5F7FA;
        }
        .block-container {
            max-width: 1500px;
            padding-top: 1.4rem;
            padding-bottom: 2.5rem;
        }
        [data-testid='stSidebar'] {
            background: #FFF;
            border-right: 1px solid #E6EBF2;
        }
        h1, h2, h3 {
            color: #102348;
        }
        .page-title {
            color: #102348;
            font-size: 2.2rem;
            line-height: 1.15;
            font-weight: 780;
            margin: 0;
        }
        .page-subtitle {
            color: #64748B;
            font-size: 1rem;
            margin: .35rem 0 1.3rem;
        }
        div[data-testid='stMetric'],
        div[data-testid='stPlotlyChart'] {
            background: #FFF;
            border: 1px solid #E4EAF2;
            border-radius: 16px;
            box-shadow: 0 5px 15px rgba(15, 35, 68, .04);
        }

        @media (max-width: 900px) {
            .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
                padding-top: 1rem;
            }
            .page-title {
                font-size: 1.8rem;
            }
            div[data-testid='stHorizontalBlock'] {
                flex-wrap: wrap;
                gap: .75rem;
            }
            div[data-testid='column'] {
                min-width: min(100%, 280px) !important;
                flex: 1 1 280px !important;
            }
        }

        @media (max-width: 560px) {
            .page-title {
                font-size: 1.55rem;
            }
            .page-subtitle {
                font-size: .95rem;
            }
            div[data-testid='column'] {
                min-width: 100% !important;
                flex-basis: 100% !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header(title: str, subtitle: str) -> None:
    st.markdown(
        f'<p class="page-title">{title}</p>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<p class="page-subtitle">{subtitle}</p>',
        unsafe_allow_html=True,
    )
