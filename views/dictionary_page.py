import streamlit as st
from services.translator import WORD_DICTIONARY
from styles.style_loader import load_css


def render_dictionary_page():
    load_css()

    st.markdown('<div class="main-title">단어 사전 📘</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-text">한국어 → 영어 중간표현으로 바뀌는 기본 단어 사전입니다.</div>',
        unsafe_allow_html=True
    )

    search = st.text_input("단어 검색", placeholder="예: 안녕, 졸려, 바나나")

    rows = []
    for ko, en in WORD_DICTIONARY.items():
        if not search or search in ko or search.lower() in en.lower():
            rows.append({"한국어": ko, "영어 중간표현": en})

    if rows:
        st.dataframe(rows, use_container_width=True)
    else:
        st.warning("검색 결과가 없습니다.")