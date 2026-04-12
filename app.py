import streamlit as st
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import tempfile
import os
from datetime import date
from groq import Groq

# ==============================
# CONFIG
# ==============================
st.set_page_config(page_title="TikTok Caption AI", layout="centered")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.title("🎬 TikTok Style Captions")

# ==============================
# CONTROLE DE USO
# ==============================
today = str(date.today())

if "usage" not in st.session_state:
    st.session_state.usage = {}

if today not in st.session_state.usage:
    st.session_state.usage = {today: 0}

limit = 3
used = st.session_state.usage[today]

st.write(f"Free usage: {used}/{limit}")

# ==============================
# UPLOAD
# ==============================
video = st.file_uploader("Upload video", type=["mp4", "mov"])

if video:
    st.video(video)

    if st.button("🚀 Generate TikTok Captions"):

        if used >= limit:
            st.error("Limit reached")
        else:
            st.info("Processing...")

            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                tmp.write(video.read())
                video_path = tmp.name

            try:
                clip = VideoFileClip(video_path)

                # extrair áudio
                audio_path = video_path + ".mp3"
                clip.audio.write_audiofile(audio_path)

                # ==============================
                # TRANSCRIÇÃO COM TIMESTAMPS
                # ==============================
                with open(audio_path, "rb") as f:
                    transcription = client.audio.transcriptions.create(
                        file=f,
                        model="whisper-large-v3",
                        response_format="verbose_json"
                    )

                words = []
                for seg in transcription.segments:
                    for w in seg["words"]:
                        words.append(w)

                full_text = [w["word"] for w in words]

                text_clips = []

                for i, word in enumerate(words):
                    start = word["start"]
                    end = word["end"]

                    # montar frase com palavra destacada
                    styled_text = ""
                    for j, w in enumerate(full_text):
                        if j == i:
                            styled_text += f"<span foreground='yellow'>{w}</span> "
                        else:
                            styled_text += f"<span foreground='white'>{w}</span> "

                    txt_clip = (
                        TextClip(
                            styled_text,
                            fontsize=60,
                            method='caption',
                            size=(clip.w - 100, None),
                            align='center'
                        )
                        .set_position(("center", "bottom"))
                        .set_start(start)
                        .set_duration(end - start)
                    )

                    text_clips.append(txt_clip)

                final = CompositeVideoClip([clip] + text_clips)

                output = video_path + "_tiktok.mp4"
                final.write_videofile(output, fps=24)

                st.success("✅ Done!")

                st.video(output)

                with open(output, "rb") as f:
                    st.download_button(
                        "⬇️ Download Video",
                        f,
                        file_name="tiktok_caption.mp4"
                    )

                st.session_state.usage[today] += 1

            except Exception as e:
                st.error("Error processing")

            finally:
                if os.path.exists(video_path):
                    os.remove(video_path)
