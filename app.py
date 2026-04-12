import streamlit as st
from moviepy.editor import VideoFileClip
import tempfile
import os
from datetime import date
from groq import Groq

# ==============================
# CONFIG
# ==============================
st.set_page_config(page_title="AI Caption Generator", layout="centered")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.title("🎬 AI Caption Generator (Groq)")

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

st.write(f"📊 Free usage: {used}/{limit} today")

# ==============================
# ESTILO
# ==============================
style = st.selectbox(
    "Choose caption style",
    ["Simple", "Bold", "Subtitle", "TikTok Style"]
)

# ==============================
# UPLOAD
# ==============================
video = st.file_uploader("Upload your video", type=["mp4", "mov"])

if video:
    st.video(video)

    if st.button("🚀 Generate Captions"):

        if used >= limit:
            st.error("🚫 Daily limit reached (3 videos)")
        else:
            st.info("Processing...")

            # salvar vídeo
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                tmp.write(video.read())
                video_path = tmp.name

            try:
                clip = VideoFileClip(video_path)

                # extrair áudio
                audio_path = video_path + ".mp3"
                clip.audio.write_audiofile(audio_path)

                # ==============================
                # TRANSCRIÇÃO COM GROQ
                # ==============================
                with open(audio_path, "rb") as f:
                    transcription = client.audio.transcriptions.create(
                        file=f,
                        model="whisper-large-v3"
                    )

                text = transcription.text

                # ==============================
                # ESTILOS
                # ==============================
                if style == "Bold":
                    text = text.upper()

                elif style == "Subtitle":
                    text = "\n".join([f"- {line.strip()}" for line in text.split(".") if line.strip()])

                elif style == "TikTok Style":
                    text = "✨ " + text.replace(".", " 🔥 ")

                st.success("✅ Captions generated!")

                st.text_area("Your captions", text, height=200)

                # download
                st.download_button(
                    "⬇️ Download captions",
                    text,
                    file_name="captions.txt"
                )

                # atualizar uso
                st.session_state.usage[today] += 1

            except Exception as e:
                st.error("Error processing video")

            finally:
                if os.path.exists(video_path):
                    os.remove(video_path)
