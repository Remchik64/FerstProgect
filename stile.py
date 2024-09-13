import streamlit as st

st.markdown("""
<style>
    .reportview-container .main .block-container {
        max-width: 1200px;
        margin-left: auto;
        margin-right: auto;
    }
    .reportview-container .main {
        background-color: #f0f2f6;
        color: #000000;
    }
    .center-button {
        display: flex;
        justify-content: center;
        margin-top: 20px;  /* Отступ сверху */
    }
    .stButton {
        background-color: #2980B9;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;  /* Размер шрифта */
    }
    .stButton:hover {
        background-color: #3498DB;
    }
</style>
""", unsafe_allow_html=True)
