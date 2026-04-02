import random

WORD_DICTIONARY = {
    "안녕": "hello",
    "나": "me",
    "나는": "me",
    "너": "you",
    "너는": "you",
    "오늘": "today",
    "좋아": "like",
    "좋아해": "like",
    "사랑해": "love",
    "배고파": "hungry",
    "졸려": "sleepy",
    "웃겨": "funny",
    "고마워": "thank you",
    "바나나": "banana",
    "먹고 싶어": "want banana",
    "먹고싶어": "want banana",
    "진짜": "really",
    "너무": "very",
}

JOSA_LIST = [
    "은", "는", "이", "가", "을", "를", "에", "에서", "에게", "와", "과", "도", "만"
]

MINION_REPLACEMENTS = {
    "hello": "bello",
    "thank you": "tank yu",
    "goodbye": "poopaye",
    "banana": "banana",
    "love": "luv",
    "funny": "haha funny",
}

MINION_EXTRAS = {
    "기본": ["bello", "banana"],
    "귀엽게": ["bello", "heehee", "banana"],
    "과장되게": ["BEEEDO", "BANANAAA", "bello!!"],
    "바나나 많이": ["banana", "banana!!", "bananaaaa"],
}


def preprocess_korean(text: str) -> str:
    text = text.strip()

    replacements = {
        "입니다": "이다",
        "해요": "해",
        "해요!": "해!",
        "예요": "야",
        "이에요": "이다",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text


def extract_keywords(text: str) -> list[str]:
    keywords = []

    multi_word_keys = ["먹고 싶어", "먹고싶어"]
    for key in multi_word_keys:
        if key in text:
            keywords.append(key)

    temp = text
    for key in multi_word_keys:
        temp = temp.replace(key, " ")

    tokens = temp.replace(",", " ").replace(".", " ").replace("!", " ").replace("?", " ").split()

    for token in tokens:
        stripped = token
        for josa in JOSA_LIST:
            if stripped.endswith(josa) and len(stripped) > 1:
                stripped = stripped[: -len(josa)]
                break

        if stripped:
            keywords.append(stripped)

    seen = []
    for k in keywords:
        if k not in seen:
            seen.append(k)

    return seen


def keywords_to_english(keywords: list[str]) -> str:
    converted = []

    for word in keywords:
        if word in WORD_DICTIONARY:
            converted.append(WORD_DICTIONARY[word])
        else:
            converted.append(word)

    return " ".join(converted)


def apply_minion_style(english_text: str, style: str) -> str:
    result = english_text

    # 긴 표현 먼저 치환
    for original, changed in sorted(MINION_REPLACEMENTS.items(), key=lambda x: len(x[0]), reverse=True):
        result = result.replace(original, changed)

    extras = MINION_EXTRAS.get(style, ["bello", "banana"])
    extra_word = random.choice(extras)

    if result.strip():
        result = f"{result}... {extra_word}!"
    else:
        result = extra_word

    return result


def run_translation_pipeline(text: str, style: str, use_fallback: bool) -> dict:
    original = text
    preprocessed = preprocess_korean(text)
    keywords = extract_keywords(preprocessed)
    intermediate_english = keywords_to_english(keywords)

    # 현재는 외부 API 연결 전 MVP라서 fallback처럼 동작
    used_fallback = True if use_fallback else False

    minion_result = apply_minion_style(intermediate_english, style)

    return {
        "original": original,
        "preprocessed": preprocessed,
        "keywords": keywords,
        "intermediate_english": intermediate_english,
        "minion_result": minion_result,
        "final_output": minion_result,
        "style": style,
        "used_fallback": used_fallback,
        "status_message": "현재 버전은 규칙 기반 MVP입니다. 이후 API 연결 가능",
    }