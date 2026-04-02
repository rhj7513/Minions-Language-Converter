import streamlit as st
import streamlit.components.v1 as components

from services.translator import run_translation_pipeline
from services.tts_service import text_to_speech_bytes
from services.animation_html import build_minion_talking_html
from styles.style_loader import load_css


def render_translator_page():
    load_css()

    # -----------------------------
    # session_state 초기화
    # -----------------------------
    if "translation_result" not in st.session_state:
        st.session_state.translation_result = None

    if "audio_bytes" not in st.session_state:
        st.session_state.audio_bytes = None

    if "input_text" not in st.session_state:
        st.session_state.input_text = ""

    # -----------------------------
    # 헤더
    # -----------------------------
    st.markdown(
        '<div class="main-title">한국어 → 미니언 번역기 🍌</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="sub-text">한국어 문장을 분석한 뒤 미니언 스타일로 변환합니다.</div>',
        unsafe_allow_html=True
    )
    st.info("이 서비스는 정식 언어 번역기가 아니라 미니언 스타일 변환기입니다.")

    # -----------------------------
    # 좌/우 레이아웃
    # -----------------------------
    left_col, right_col = st.columns([1.05, 0.95], gap="large")

    # =========================================================
    # LEFT: 입력 영역
    # =========================================================
    with left_col:
        example_sentences = [
            "안녕, 오늘 기분이 좋아",
            "나는 바나나가 먹고 싶어",
            "오늘 너무 졸려",
            "너 진짜 웃겨",
        ]

        st.markdown('<div class="section-title">예시 문장</div>', unsafe_allow_html=True)

        ex1, ex2, ex3, ex4 = st.columns(4)

        with ex1:
            if st.button("안녕", use_container_width=True):
                st.session_state.input_text = example_sentences[0]
                st.session_state.translation_result = None
                st.session_state.audio_bytes = None

        with ex2:
            if st.button("바나나", use_container_width=True):
                st.session_state.input_text = example_sentences[1]
                st.session_state.translation_result = None
                st.session_state.audio_bytes = None

        with ex3:
            if st.button("졸려", use_container_width=True):
                st.session_state.input_text = example_sentences[2]
                st.session_state.translation_result = None
                st.session_state.audio_bytes = None

        with ex4:
            if st.button("웃겨", use_container_width=True):
                st.session_state.input_text = example_sentences[3]
                st.session_state.translation_result = None
                st.session_state.audio_bytes = None

        st.markdown('<div class="section-title">문장 입력</div>', unsafe_allow_html=True)

        input_text = st.text_area(
            "한국어 문장을 입력하세요",
            value=st.session_state.input_text,
            height=220,
            placeholder="예: 나는 오늘 너무 졸려",
            label_visibility="collapsed",
        )
        st.session_state.input_text = input_text
        st.caption(f"글자 수: {len(input_text)}자")

        opt1, opt2, opt3 = st.columns([1.15, 1.15, 1])

        with opt1:
            style = st.selectbox(
                "변환 스타일",
                ["기본", "귀엽게", "과장되게", "바나나 많이"],
                index=0,
            )

        with opt2:
            use_fallback = st.checkbox("API 실패 시 fallback 사용", value=True)

        with opt3:
            st.markdown("<br>", unsafe_allow_html=True)
            translate_clicked = st.button("번역하기 🍌", use_container_width=True)

        if translate_clicked:
            if not input_text.strip():
                st.warning("문장을 입력해줘!")
                st.session_state.translation_result = None
                st.session_state.audio_bytes = None
            else:
                with st.spinner("미니언 스타일로 변환 중..."):
                    result = run_translation_pipeline(
                        text=input_text,
                        style=style,
                        use_fallback=use_fallback,
                    )

                st.session_state.translation_result = result
                st.session_state.audio_bytes = None

    # =========================================================
    # RIGHT: 결과 영역
    # =========================================================
    with right_col:
        result = st.session_state.translation_result

        st.markdown('<div class="section-title">결과 화면</div>', unsafe_allow_html=True)

        if result:
            st.markdown(
                f"""
                <div class="result-box">
                    <div class="small-label">MINION OUTPUT</div>
                    <div class="result-text">{result["final_output"]}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown('<div class="section-title">음성 듣기 🔊</div>', unsafe_allow_html=True)

            t1, t2 = st.columns([1, 1])

            with t1:
                tts_lang = st.selectbox(
                    "음성 언어",
                    ["en", "ko"],
                    index=0,
                    help="미니언 느낌은 영어(en)가 더 자연스러움",
                    key="tts_lang_select"
                )

            with t2:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("음성 생성", use_container_width=True, key="tts_generate_button"):
                    st.session_state.audio_bytes = text_to_speech_bytes(
                        text=result["final_output"],
                        lang=tts_lang,
                    )

            if st.session_state.audio_bytes is not None:
                html = build_minion_talking_html(
                    audio_bytes=st.session_state.audio_bytes.getvalue(),
                    closed_img_path="assets/minion_closed.png",
                    open_img_path="assets/minion_open.png",
                )
                components.html(html, height=430, scrolling=False)
            else:
                st.markdown(
                    """
                    <div class="card" style="text-align:center;">
                        <div class="small-label">MINION CHARACTER</div>
                        <p style="margin-top: 10px;">음성을 생성하면 여기서 미니언이 말하기 시작해!</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        else:
            st.markdown(
                """
                <div class="card" style="min-height: 360px; display:flex; align-items:center; justify-content:center; text-align:center;">
                    <div>
                        <div class="small-label">RESULT PREVIEW</div>
                        <p style="font-size: 1.05rem; margin-top: 10px;">
                            왼쪽에서 문장을 입력하고<br>
                            <b>번역하기 🍌</b>를 누르면 결과가 여기에 표시돼.
                        </p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    # =========================================================
    # 하단: 변환 과정
    # =========================================================
    result = st.session_state.translation_result

    if result:
        st.markdown('<div class="section-title">변환 과정</div>', unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("**STEP 1. 원문**")
            st.write(result["original"])
            st.markdown('</div>', unsafe_allow_html=True)

        with c2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("**STEP 2. 전처리 결과**")
            st.write(result["preprocessed"])
            st.markdown('</div>', unsafe_allow_html=True)

        with c3:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("**STEP 3. 핵심 단어**")
            st.write(", ".join(result["keywords"]) if result["keywords"] else "-")
            st.markdown('</div>', unsafe_allow_html=True)

        c4, c5 = st.columns(2)

        with c4:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("**STEP 4. 중간 영어 문장**")
            st.code(result["intermediate_english"], language="text")
            st.markdown('</div>', unsafe_allow_html=True)

        with c5:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("**STEP 5. 미니언 변환 결과**")
            st.code(result["minion_result"], language="text")
            st.markdown('</div>', unsafe_allow_html=True)

        with st.expander("상세 정보 보기"):
            st.json(
                {
                    "style": result["style"],
                    "used_fallback": result["used_fallback"],
                    "status_message": result["status_message"],
                }
            )