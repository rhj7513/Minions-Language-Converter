import streamlit as st
from pathlib import Path


def load_css(file_name: str = "main.css"):
    css_path = Path(__file__).parent / file_name

    if css_path.exists():
        with open(css_path, "r", encoding="utf-8") as f:
            css = f.read()

        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)