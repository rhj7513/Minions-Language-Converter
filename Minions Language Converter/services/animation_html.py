import base64
from pathlib import Path


def image_to_base64(path: str) -> str:
    data = Path(path).read_bytes()
    return base64.b64encode(data).decode("utf-8")


def audio_to_base64(audio_bytes: bytes) -> str:
    return base64.b64encode(audio_bytes).decode("utf-8")


def build_minion_talking_html(audio_bytes: bytes, closed_img_path: str, open_img_path: str) -> str:
    audio_b64 = audio_to_base64(audio_bytes)
    closed_b64 = image_to_base64(closed_img_path)
    open_b64 = image_to_base64(open_img_path)

    return f"""
    <div style="text-align:center; padding: 16px;">
        <img id="minion" src="data:image/png;base64,{closed_b64}" style="width:260px; border-radius:16px;" />
        <br><br>
        <button onclick="playAudio()" style="padding:10px 16px; border:none; border-radius:10px; cursor:pointer;">
            🔊 음성 듣기
        </button>
        <audio id="audio" src="data:audio/mp3;base64,{audio_b64}"></audio>
    </div>

    <script>
    const audio = document.getElementById("audio");
    const img = document.getElementById("minion");
    const closedSrc = "data:image/png;base64,{closed_b64}";
    const openSrc = "data:image/png;base64,{open_b64}";
    let timer = null;
    let opened = false;

    function playAudio() {{
        if (timer) clearInterval(timer);

        audio.currentTime = 0;
        audio.play();

        timer = setInterval(() => {{
            opened = !opened;
            img.src = opened ? openSrc : closedSrc;
        }}, 160);
    }}

    audio.onended = () => {{
        if (timer) clearInterval(timer);
        img.src = closedSrc;
    }};
    </script>
    """