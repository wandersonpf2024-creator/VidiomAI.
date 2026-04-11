import streamlit as st
import os
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.VideoClip import TextClip

# --- CONFIGURAÇÃO VISUAL ---
st.set_page_config(page_title="VIDIOM AI", layout="wide")

st.markdown("""
    <style>
    .top-header { text-align: center; padding: 15px 0; font-family: 'Inter', sans-serif; font-size: 32px; letter-spacing: 6px; color: #ffffff; text-transform: uppercase; }
    .stApp { background-color: #05070a; color: #ffffff; }
    .main .block-container { max-width: 90% !important; margin: 0 auto; }
    
    /* Estilo do Botão Converter do Print */
    div.stButton > button:first-child { 
        background-color: #ffffff !important; 
        color: #000000 !important; 
        border-radius: 25px !important; 
        padding: 10px 45px !important; 
        font-weight: bold !important; 
        float: right; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO DE AJUSTE DE ESCALA (RESOVE O TAMANHO DO VÍDEO) ---
def processar_escala_vidiom(video_in, start, end):
    output_path = "vidiom_renderizado.mp4"
    try:
        with VideoFileClip(video_in, audio=True).subclip(start, end) as clip:
            
            # LÓGICA DE PREENCHIMENTO (9:16)
            # Pegamos a altura total e calculamos a largura vertical proporcional
            h = clip.h
            w_vertical = h * (9/16)
            
            # Cortamos o centro do vídeo para preencher a tela vertical sem barras pretas
            clip_vertical = clip.crop(x_center=clip.w/2, width=w_vertical)
            
            # DESENHANDO A MARCA D'ÁGUA VIDIOM.AI
            marca = (TextClip("VIDIOM.AI", fontsize=26, color='white', font='Arial-Bold')
                     .set_opacity(0.5)
                     .set_duration(clip.duration)
                     .set_position(('right', 'bottom'))
                     .margin(right=25, bottom=50, opacity=0))

            final = CompositeVideoClip([clip_vertical, marca])
            final.write_videofile(output_path, codec="libx264", audio_codec="aac", threads=1, logger=None)
            
        return output_path
    except Exception as e:
        st.error(f"Erro ao ajustar escala: {e}")
        return None

# --- ESTRUTURA DO APP ---
st.markdown('<div class="top-header">VIDIOM.AI</div>', unsafe_allow_html=True)

video_up = st.file_uploader("", type=["mp4", "mov"])

if video_up:
    with open("video_input.mp4", "wb") as f: f.write(video_up.getbuffer())
    
    with VideoFileClip("video_input.mp4") as v:
        dur = int(v.duration)

    # Exibição do player
    st.video("video_input.mp4")
    
    st.write("### Selecione a parte que deseja converter")
    periodo = st.slider("", 0, dur, (0, min(60, dur)))

    # Grade de Legendas (Igual ao print)
    st.write("### Selecionar modelo de legenda")
    cols = st.columns(8)
    for i in range(8):
        with cols[i]: st.button(f"Estilo {i+1}", key=f"leg_{i}")

    st.write("---")
    
    c1, c2 = st.columns([3, 1])
    with c1:
        st.text_area("Defina a duração dos vídeos curtos", placeholder="A IA vai focar no centro da ação para o formato vertical...")
    with c2:
        st.write("##")
        if st.button("Converter"):
            with st.status("🎬 Ajustando escala para 9:16...", expanded=False):
                res = processar_escala_vidiom("video_input.mp4", periodo[0], periodo[1])
                if res:
                    st.success("Vídeo Vertical Gerado!")
                    with open(res, "rb") as f:
                        st.download_button("📥 BAIXAR VÍDEO", f, file_name="vidiom_short.mp4")
else:
    st.info("Arraste um vídeo para começar.")
