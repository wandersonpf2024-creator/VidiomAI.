import streamlit as st
import os
import re
from groq import Groq
from moviepy.video.io.VideoFileClip import VideoFileClip

# --- CONFIGURAÇÃO ESTÉTICA (CSS MODERNO) ---
st.set_page_config(page_title="VIDIOM AI | Editor Pro", layout="wide")

st.markdown("""
    <style>
    /* 1. Fundo e Fontes */
    .stApp { background-color: #05070a; color: #e2e8f0; }
    
    /* 2. Barra Superior e Títulos */
    .main-title { font-size: 28px; font-weight: 700; margin-bottom: 20px; color: #ffffff; }
    
    /* 3. Estilização do File Uploader (Área de Drag & Drop) */
    div[data-testid="stFileUploader"] {
        background-color: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 30px;
    }

    /* 4. Botão Converter Estilo "Glow" */
    .stButton>button {
        width: 100%;
        background: #ffffff;
        color: #000000 !important;
        border-radius: 50px;
        padding: 12px 24px;
        font-weight: 700;
        border: none;
        transition: 0.3s;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stButton>button:hover {
        background: #f8fafc;
        transform: translateY(-2px);
        box-shadow: 0 10px 20px -10px rgba(255, 255, 255, 0.3);
    }

    /* 5. Seletor de Legenda (Cards) */
    .stSelectbox div[data-baseweb="select"] {
        background-color: #1e293b;
        border-radius: 8px;
    }
    
    /* 6. Inputs de Texto e Sliders */
    .stTextArea textarea { background-color: #0f172a; border: 1px solid #334155; color: white; border-radius: 10px; }
    .stSlider > div > div > div > div { background-color: #6366f1; }
    
    /* Estilo para as opções de legenda mockadas */
    .legenda-box {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 10px;
        text-align: center;
        font-size: 12px;
        cursor: pointer;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE BACKEND ---
def processar_corte(video_path, start, end):
    output = "corte_final.mp4"
    try:
        with VideoFileClip(video_path, audio=True).subclip(start, end) as video:
            video.write_videofile(output, codec="libx264", audio_codec="aac", temp_audiofile='temp-audio.m4a', remove_temp=True, logger=None)
        return output
    except Exception as e:
        st.error(f"Erro: {e}")
        return None

# --- INTERFACE ---
st.markdown('<div class="main-title">🎬 Converta vídeos longos em vídeos curtos</div>', unsafe_allow_html=True)

# Container Principal
with st.container():
    # Topo: Upload simplificado
    video_file = st.file_uploader("", type=["mp4", "mov"])
    
    if video_file:
        with open("video_vidiom.mp4", "wb") as f:
            f.write(video_file.getbuffer())
        
        with VideoFileClip("video_vidiom.mp4") as v:
            duracao_max = int(v.duration)

        # PLAYER DE VÍDEO (Centralizado como na imagem)
        st.video("video_vidiom.mp4")

        st.write("---")
        
        # ÁREA DE SELEÇÃO
        st.markdown("### 🎞️ Selecione a parte que deseja converter")
        tempo = st.slider("", 0, duracao_max, (0, min(60, duracao_max)))
        st.caption(f"Duração selecionada: {tempo[1] - tempo[0]} segundos")

        st.write("---")

        # MODELOS DE LEGENDA (Visual)
        st.markdown("### ✍️ Selecionar modelo de legenda")
        cols = st.columns(6)
        with cols[0]: st.button("Default", key="l1")
        with cols[1]: st.button("Glow", key="l2")
        with cols[2]: st.button("Impact", key="l3")
        with cols[3]: st.button("Cyber", key="l4")
        with cols[4]: st.button("Retro", key="l5")
        with cols[5]: st.button("Clean", key="l6")

        st.write("---")

        # DURAÇÃO E CONVERSÃO
        col_txt, col_btn = st.columns([2, 1])
        
        with col_txt:
            contexto = st.text_area("O que acontece no vídeo? (IA Context)", placeholder="Explique para a IA o que focar...")
        
        with col_btn:
            st.write("##") # Espaçador
            if st.button("✨ Converter"):
                with st.status("Gerando seu corte viral...", expanded=True):
                    final_clip = processar_corte("video_vidiom.mp4", tempo[0], tempo[1])
                    if final_clip:
                        st.success("Pronto!")
                        with open(final_clip, "rb") as f:
                            st.download_button("📥 BAIXAR AGORA", f, file_name="vidiom_pro.mp4")
    else:
        st.image("https://img.freepik.com/free-vector/upload-concept-illustration_114360-1205.jpg", width=200)
        st.info("Arraste um vídeo MP4 para começar a mágica.")

# Rodapé
st.markdown("<br><br><center><small>VIDIOM AI - O futuro da edição automática</small></center>", unsafe_allow_html=True)
