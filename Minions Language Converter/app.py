import streamlit as st
from views.translator_page import render_translator_page
from views.dictionary_page import render_dictionary_page

st.set_page_config(
    page_title="한국어 → 미니언 번역기",
    page_icon="🍌",
    layout="wide",
)

pg = st.navigation(
    [
        st.Page(render_translator_page, title="번역기", icon="🍌", default=True),
        st.Page(render_dictionary_page, title="단어 사전", icon="📘"),
    ],
    position="top",
)

pg.run()