import streamlit as st
import os
from moviepy.video.io.VideoFileClip import VideoFileClip
import moviepy.video.fx.all as vfx 
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.VideoClip import TextClip

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="VIDIOM AI", layout="wide")

st.markdown("""
    <style>
    /* DEFINIÇÃO DAS ANIMAÇÕES */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes scaleIn {
        from {
            opacity: 0;
            transform: scale(0.95);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }

    /* APLICAÇÃO DAS ANIMAÇÕES NOS ELEMENTOS */
    
    .vidiom-logo-top {
        animation: fadeInUp 0.8s ease-out forwards;
        text-align: center;
        font-family: 'Inter', sans-serif;
        font-size: 32px;
        letter-spacing: 8px;
        font-weight: 300;
        text-transform: uppercase;
        padding: 20px 0;
    }

    .header-box {
        animation: fadeInUp 1s ease-out forwards;
        display: flex;
        align-items: center;
        margin-bottom: 20px;
    }

    /* O container do vídeo vem com um leve "pulo" de escala */
    .video-frame-vidiom {
        animation: scaleIn 0.8s ease-out 0.2s backwards;
        background-color: #1a1a1b;
        border-radius: 20px;
        padding: 30px;
        border: 1px solid #262627;
        margin-bottom: 25px;
    }

    .stVideo {
        overflow: hidden !important;
        border-radius: 20px !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }

    /* Botões e Inputs aparecem por último */
    .stSlider, .stTextArea, .stFileUploader, .stButton {
        animation: fadeInUp 0.8s ease-out 0.4s backwards;
    }

    /* ESTILOS GERAIS MANTIDOS */
    .stApp { background-color: #0d0d0d; color: #ffffff; }
    .main .block-container { max-width: 1100px !important; margin: 0 auto; }
    .header-text { font-size: 22px; font-weight: bold; margin-left: 12px; }

    div.stButton > button:first-child {
        background: white !important;
        color: black !important;
        border-radius: 30px !important;
        padding: 12px 50px !important;
        font-weight: bold !important;
        border: none !important;
        float: right;
        box-shadow: 0 0 20px rgba(255, 255, 255, 0.2);
    }

    .stButton > button {
        background-color: #1c1c1e;
        color: #8e8e93;
        border: 1px solid #3a3a3c;
        border-radius: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LÓGICA DE VÍDEO (MARCA D'ÁGUA + CORTE 9:16) ---
def processar_vidiom_animated(video_in, start, end):
    output_path = "vidiom_render.mp4"
    try:
        with VideoFileClip(video_in, audio=True).subclip(start, end) as clip:
            h = clip.h
            w_v = h * (9/16)
            clip_v = vfx.crop(clip, x_center=clip.w/2, width=w_v)
            
            try:
                marca = (TextClip("VIDIOM.AI", fontsize=25, color='white', font='Arial-Bold')
                         .set_opacity(0.5)
                         .set_duration(clip.duration)
                         .set_position(('right', 'bottom'))
                         .margin(right=20, bottom=40, opacity=0))
                final = CompositeVideoClip([clip_v, marca])
            except:
                final = clip_v

            final.write_videofile(output_path, codec="libx264", audio_codec="aac", threads=1, logger=None)
        return output_path
    except Exception as e:
        st.error(f"Erro: {e}")
        return None

# --- 3. INTERFACE COM MOTION DESIGN ---

st.markdown('<div class="vidiom-logo-top">VIDIOM.AI</div>', unsafe_allow_html=True)
st.markdown('<div class="header-box">🎬 <span class="header-text">Converta vídeos longos em vídeos curtos</span></div>', unsafe_allow_html=True)

arquivo = st.file_uploader("", type=["mp4", "mov"])

if arquivo:
    with open("temp.mp4", "wb") as f: f.write(arquivo.getbuffer())
    
    with VideoFileClip("temp.mp4") as v:
        dur = int(v.duration)

    st.markdown('<div class="video-frame-vidiom">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.video("temp.mp4")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.write("### Selecione o corte")
    tempo = st.slider("", 0, dur, (0, min(60, dur)))

    st.write("### Estilo de Legenda")
    cols = st.columns(10)
    for i in range(10):
        with cols[i]: st.button(f"Mod {i+1}", key=f"e{i}")

    st.write("---")
    c1, c2 = st.columns([3, 1])
    with c1:
        st.text_area("Contexto", placeholder="O que acontece no vídeo?")
    with c2:
        st.write("##")
        if st.button("Converter"):
            with st.status("🎬 Processando...", expanded=False):
                res = processar_vidiom_animated("temp.mp4", tempo[0], tempo[1])
                if res:
                    st.success("Pronto!")
                    with open(res, "rb") as f:
                        st.download_button("📥 BAIXAR", f, file_name="vidiom.mp4")
else:
    st.info("Upload de vídeo pendente.")

st.markdown("<br><center><small>© 2026 VIDIOM.AI</small></center>", unsafe_allow_html=True)
