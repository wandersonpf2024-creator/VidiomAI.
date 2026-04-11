import streamlit as st
import os
from moviepy.video.io.VideoFileClip import VideoFileClip
import moviepy.video.fx.all as vfx 
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.VideoClip import TextClip

# --- 1. CONFIGURAÇÃO DA PÁGINA (WIDE + TEMA ESCURO) ---
st.set_page_config(page_title="VIDIOM AI", layout="wide")

st.markdown("""
    <style>
    /* Fundo e Container */
    .stApp { background-color: #0d0d0d; color: #ffffff; }
    .main .block-container { max-width: 1100px !important; margin: 0 auto; }

    /* Nome do App no Topo (Sua marca) */
    .vidiom-logo-top {
        text-align: center;
        font-family: 'Inter', sans-serif;
        font-size: 32px;
        letter-spacing: 8px;
        font-weight: 300;
        text-transform: uppercase;
        padding: 20px 0;
    }

    /* Container do Vídeo Estilo Dashboard */
    .video-frame-vidiom {
        background-color: #1a1a1b;
        border-radius: 20px;
        padding: 30px;
        border: 1px solid #262627;
        margin-bottom: 25px;
    }

    /* BORDAS ARREDONDADAS NO VÍDEO (O que você pediu por último) */
    .stVideo {
        overflow: hidden !important;
        border-radius: 20px !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }

    /* Título com Claquete */
    .header-box {
        display: flex;
        align-items: center;
        margin-bottom: 20px;
    }
    .header-text { font-size: 22px; font-weight: bold; margin-left: 12px; }

    /* Botão CONVERTER (Branco, Arredondado, com Brilho) */
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

    /* Estilo dos Cards de Legenda */
    .stButton > button {
        background-color: #1c1c1e;
        color: #8e8e93;
        border: 1px solid #3a3a3c;
        border-radius: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LÓGICA DE VÍDEO (MARCA D'ÁGUA + CORTE VERTICAL) ---
def processar_vidiom_completo(video_in, start, end):
    output_path = "vidiom_final.mp4"
    try:
        with VideoFileClip(video_in, audio=True).subclip(start, end) as clip:
            # Transforma em Vertical 9:16 (Resolve o problema do tamanho)
            h = clip.h
            w_v = h * (9/16)
            clip_v = vfx.crop(clip, x_center=clip.w/2, width=w_v)
            
            # Desenha a Marca d'água [VIDIOM.AI] (Garante sua marca)
            try:
                marca = (TextClip("VIDIOM.AI", fontsize=25, color='white', font='Arial-Bold')
                         .set_opacity(0.5)
                         .set_duration(clip.duration)
                         .set_position(('right', 'bottom'))
                         .margin(right=20, bottom=40, opacity=0))
                final = CompositeVideoClip([clip_v, marca])
            except:
                final = clip_v # Fallback caso falte biblioteca de fontes

            final.write_videofile(output_path, codec="libx264", audio_codec="aac", threads=1, logger=None)
        return output_path
    except Exception as e:
        st.error(f"Erro: {e}")
        return None

# --- 3. INTERFACE (O QUE O USUÁRIO VÊ) ---

# Nome no topo
st.markdown('<div class="vidiom-logo-top">VIDIOM.AI</div>', unsafe_allow_html=True)

# Título com claquete
st.markdown('<div class="header-box">🎬 <span class="header-text">Converta vídeos longos em vídeos curtos</span></div>', unsafe_allow_html=True)

arquivo = st.file_uploader("", type=["mp4", "mov"])

if arquivo:
    with open("temp.mp4", "wb") as f: f.write(arquivo.getbuffer())
    
    with VideoFileClip("temp.mp4") as v:
        dur = int(v.duration)

    # Preview Arredondado dentro da Moldura
    st.markdown('<div class="video-frame-vidiom">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.video("temp.mp4")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.write("### Selecione a parte que deseja converter vídeos curtos")
    tempo = st.slider("", 0, dur, (0, min(60, dur)))

    st.write("### Selecionar modelo de legenda")
    cols = st.columns(10) # 10 colunas como pedido
    for i in range(10):
        with cols[i]: st.button(f"Estilo {i+1}", key=f"e{i}")

    st.write("---")
    
    c1, c2 = st.columns([3, 1])
    with c1:
        st.text_area("Duração dos vídeos curtos", placeholder="A IA vai focar no centro...")
    with c2:
        st.write("##")
        if st.button("Converter"):
            with st.status("🎬 Ajustando escala 9:16 e aplicando marca d'água...", expanded=False):
                res = processar_vidiom_completo("temp.mp4", tempo[0], tempo[1])
                if res:
                    st.success("Corte Realizado!")
                    with open(res, "rb") as f:
                        st.download_button("📥 BAIXAR AGORA", f, file_name="vidiom_viral.mp4")
else:
    st.info("Arraste e solte seu vídeo para começar.")

st.markdown("<br><center><small>© 2026 VIDIOM.AI - Inteligência em Vídeo</small></center>", unsafe_allow_html=True)
