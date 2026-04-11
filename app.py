import streamlit as st
import os
from moviepy.video.io.VideoFileClip import VideoFileClip
import moviepy.video.fx.all as vfx  # Importação correta para o crop
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.VideoClip import TextClip

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="VIDIOM AI", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0d0d0d; color: #ffffff; }
    .main .block-container { max-width: 1100px !important; margin: 0 auto; }

    /* Nome VIDIOM.AI no topo centralizado */
    .vidiom-logo-top {
        text-align: center;
        font-family: 'Inter', sans-serif;
        font-size: 32px;
        letter-spacing: 8px;
        font-weight: 300;
        text-transform: uppercase;
        padding: 20px 0;
    }

    /* Área de Preview do Vídeo (Igual ao seu print) */
    .video-frame-vidiom {
        background-color: #1a1a1b;
        border-radius: 12px;
        padding: 30px;
        border: 1px solid #262627;
        margin-bottom: 20px;
    }

    /* Botão CONVERTER com brilho (Canto inferior direito) */
    div.stButton > button:first-child {
        background: white !important;
        color: black !important;
        border-radius: 25px !important;
        padding: 10px 40px !important;
        font-weight: bold !important;
        border: none !important;
        float: right;
        box-shadow: 0 0 20px rgba(255, 255, 255, 0.2);
    }

    /* Cards de Legenda */
    .stButton > button {
        background-color: #1c1c1e;
        color: #8e8e93;
        border: 1px solid #3a3a3c;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO DE PROCESSAMENTO COM CORREÇÃO ---
def processar_escala_correta(video_in, start, end):
    output_path = "vidiom_render.mp4"
    try:
        with VideoFileClip(video_in, audio=True).subclip(start, end) as clip:
            
            # AJUSTE DE ESCALA 9:16 (CORRIGIDO)
            h = clip.h
            w_vertical = h * (9/16)
            
            # Usando vfx.crop corretamente para evitar o erro 'no attribute crop'
            clip_vertical = vfx.crop(clip, x_center=clip.w/2, width=w_vertical)
            
            # MARCA D'ÁGUA VIDIOM.AI (TEXTO)
            try:
                marca = (TextClip("VIDIOM.AI", fontsize=25, color='white', font='Arial-Bold')
                         .set_opacity(0.5)
                         .set_duration(clip.duration)
                         .set_position(('right', 'bottom'))
                         .margin(right=20, bottom=40, opacity=0))
                video_final = CompositeVideoClip([clip_vertical, marca])
            except:
                video_final = clip_vertical

            video_final.write_videofile(output_path, codec="libx264", audio_codec="aac", threads=1, logger=None)
            
        return output_path
    except Exception as e:
        st.error(f"Erro no processamento: {e}")
        return None

# --- INTERFACE ---
st.markdown('<div class="vidiom-logo-top">VIDIOM.AI</div>', unsafe_allow_html=True)

st.markdown('<h4 style="color:#8e8e93;">‹ Converta vídeos longos em vídeos curtos</h4>', unsafe_allow_html=True)

arquivo = st.file_uploader("", type=["mp4", "mov"])

if arquivo:
    with open("temp_v.mp4", "wb") as f: f.write(arquivo.getbuffer())
    
    with VideoFileClip("temp_v.mp4") as v:
        dur_max = int(v.duration)

    # Área de Preview (Estilo o print que você mandou)
    with st.container():
        st.markdown('<div class="video-frame-vidiom">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.video("temp_v.mp4")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.write("### Selecione a parte que deseja converter vídeos curtos")
    tempo = st.slider("", 0, dur_max, (0, min(60, dur_max)))

    st.write("### Selecionar modelo de legenda")
    cols_leg = st.columns(10)
    for i in range(10):
        with cols_leg[i]: st.button(f"Mod {i+1}", key=f"m{i}")

    st.write("---")
    
    c_inf, c_btn = st.columns([3, 1])
    with c_inf:
        st.text_area("Defina a duração dos vídeos curtos", placeholder="Ex: Foco no clímax da cena...")
    with c_btn:
        st.write("##")
        if st.button("Converter"):
            with st.status("🎬 Ajustando escala e gerando viral...", expanded=False):
                resultado = processar_escala_correta("temp_v.mp4", tempo[0], tempo[1])
                if resultado:
                    st.success("Pronto!")
                    with open(resultado, "rb") as f:
                        st.download_button("📥 BAIXAR VÍDEO", f, file_name="vidiom_short.mp4")
else:
    st.info("Arraste e solte seu vídeo para começar.")
