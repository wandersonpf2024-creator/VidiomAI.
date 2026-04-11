import streamlit as st
from groq import Groq
import re
from youtube_transcript_api import YouTubeTranscriptApi
import yt_dlp
from moviepy.editor import VideoFileClip
import os

st.set_page_config(page_title="VIDIOM PRO - Download & Corte", layout="wide")

# --- CONFIGURAÇÃO DA IA ---
def setup_groq():
    if "GROQ_API_KEY" not in st.secrets:
        st.error("Configure GROQ_API_KEY nas Secrets!")
        return None
    return Groq(api_key=st.secrets["GROQ_API_KEY"])

client = setup_groq()

# --- FUNÇÕES TÉCNICAS ---
def baixar_e_cortar(url, start_time, end_time, output_name="corte_viral.mp4"):
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': 'video_original.mp4',
        'quiet': True
    }
    
    with st.status("Baixando e Processando Vídeo...", expanded=True) as status:
        # 1. Download
        st.write("📥 Baixando do YouTube (isso pode demorar)...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        # 2. Corte
        st.write("✂️ Cortando o momento viral...")
        video = VideoFileClip("video_original.mp4").subclip(start_time, end_time)
        video.write_videofile(output_name, codec="libx264", audio_codec="aac")
        
        # Limpeza
        video.close()
        os.remove("video_original.mp4")
        status.update(label="Vídeo Pronto!", state="complete")
    
    return output_name

# --- INTERFACE ---
st.title("🎬 VIDIOM AI - O Vídeo Sai Pronto")

url_input = st.text_input("Cole o link do YouTube (Até 20 min):")

if st.button("🚀 GERAR VÍDEO PRONTO"):
    if url_input and client:
        # 1. Pegar Legenda e IA decidir o tempo
        v_id = re.search(r"(?:v=|\/)([a-zA-Z0-9_-]{11})", url_input).group(1)
        try:
            data = YouTubeTranscriptApi.get_transcript(v_id, languages=['pt', 'en'])
            transcricao = " ".join([t['text'] for t in data])
        except:
            transcricao = "Sem legenda."

        prompt = f"Analise e me dê APENAS o tempo de início e fim (em segundos) para um corte viral deste texto: {transcricao[:3000]}. Responda no formato: INICIO:X, FIM:Y"
        
        chat = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile"
        )
        
        # Extrair tempos (Ex: INICIO:10, FIM:40)
        res_ia = chat.choices[0].message.content
        try:
            start = int(re.search(r"INICIO:(\d+)", res_ia).group(1))
            end = int(re.search(r"FIM:(\d+)", res_ia).group(1))
            
            # 2. Baixar e Cortar de verdade
            nome_arquivo = baixar_e_cortar(url_input, start, end)
            
            # 3. Mostrar o Vídeo e Botão de Download
            with open(nome_arquivo, "rb") as file:
                st.video(file)
                st.download_button("📥 BAIXAR VÍDEO CORTADO", file, file_name="meu_corte.mp4")
        except Exception as e:
            st.error(f"Erro no processamento: {e}")
