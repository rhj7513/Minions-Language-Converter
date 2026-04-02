from gtts import gTTS
from io import BytesIO


def text_to_speech_bytes(text: str, lang: str = "en") -> BytesIO:
    """
    텍스트를 음성으로 변환해서 메모리(BytesIO)에 저장
    """
    audio_buffer = BytesIO()
    tts = gTTS(text=text, lang=lang)
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)
    return audio_buffer