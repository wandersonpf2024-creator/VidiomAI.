import streamlit as st
import os
import re

# Importações seguras
try:
    from groq import Groq
    import yt_dlp
    from moviepy.video.io.VideoFileClip import VideoFileClip
    from youtube_transcript_api import YouTubeTranscriptApi
except ImportError:
    st.error("Alguma biblioteca não foi instalada. Verifique o Reboot.")

st.set_page_config(page_title="VIDIOM PRO", layout="wide")

# --- FUNÇÃO DE DOWNLOAD E CORTE ---
def processar_video(url, start, end):
    output_video = "corte_final.mp4"
    
    ydl_opts = {
        'format': 'best[ext=mp4]',
        'outtmpl': 'temp_video.mp4',
        'quiet': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        with VideoFileClip("temp_video.mp4") as video:
            # Garante que o corte não passe do limite do vídeo
            duration = video.duration
            corte = video.subclip(max(0, start), min(end, duration))
            corte.write_videofile(output_video, codec="libx264", audio_codec="aac")
        
        if os.path.exists("temp_video.mp4"):
            os.remove("temp_video.mp4")
        return output_video
    except Exception as e:
        st.error(f"Erro no download/corte: {e}")
        return None

# --- INTERFACE ---
st.title("🎬 VIDIOM AI - Gerador de Clipe Pronto")

url = st.text_input("Link do YouTube (Vídeo de até 20 min):")

if st.button("🚀 GERAR VÍDEO CORTADO"):
    if url:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        
        with st.status("Analisando e Cortando...", expanded=True) as status:
            # 1. Tenta pegar a legenda para a IA decidir o tempo
            try:
                video_id = re.search(r"(?:v=|\/)([a-zA-Z0-9_-]{11})", url).group(1)
                t = YouTubeTranscriptApi.get_transcript(video_id, languages=['pt', 'en'])
                texto = " ".join([i['text'] for i in t])[:3000]
            except:
                texto = "Sem legenda disponível."

            # 2. IA decide o melhor momento (Prompt Curto para não errar)
            prompt = f"Baseado nesse texto, qual o melhor momento de 30 segundos? Responda apenas: INICIO:X, FIM:Y. Texto: {texto}"
            chat = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile"
            )
            
            res = chat.choices[0].message.content
            # Extração simples de números
            tempos = re.findall(r'\d+', res)
            start = int(tempos[0]) if len(tempos) > 0 else 10
            end = int(tempos[1]) if len(tempos) > 1 else 40

            # 3. Processa o vídeo real
            video_pronto = processar_video(url, start, end)

            if video_pronto:
                status.update(label="Vídeo pronto para download!", state="complete")
                with open(video_pronto, "rb") as f:
                    st.video(f)
                    st.download_button("📥 BAIXAR MEU VÍDEO", f, file_name="corte.mp4")
