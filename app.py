import streamlit as st
import os
from moviepy.video.io.VideoFileClip import VideoFileClip
import moviepy.video.fx.all as vfx 
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.VideoClip import ImageClip

# --- 1. CONFIGURAÇÃO DE TEMA DARK ---
st.set_page_config(page_title="VIDIOM AI", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0d0d0d; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #000000 !important; border-right: 1px solid #1e1e1e; }
    
    /* Container para centralizar a logo na sidebar */
    .logo-sidebar-container {
        display: flex;
        justify-content: center;
        padding: 20px 0;
        margin-bottom: 10px;
    }

    .menu-item {
        padding: 12px; border-radius: 8px; margin-bottom: 5px;
        display: flex; align-items: center; gap: 12px; color: #d1d1d1;
    }
    .active-menu { background-color: #262626; color: white; font-weight: bold; }

    .btn-upgrade {
        background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%);
        color: white; padding: 12px; border-radius: 8px; text-align: center;
        font-weight: bold; margin-top: 20px; display: block; text-decoration: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. MOTOR DE VÍDEO (MARCA D'ÁGUA PEQUENA) ---
def process_vidiom_final(video_path, start, end):
    output = "vidiom_output.mp4"
    logo_file = "logonova.png" # Usando a logo mais recente
    
    try:
        clip = VideoFileClip(video_path).subclip(start, end)
        h = clip.h
        w = int(h * (9/16))
        if w % 2 != 0: w -= 1
        
        final_clip = vfx.crop(clip, x_center=clip.w/2, width=w).copy()
        
        # Se a logo existir, coloca no vídeo
        if os.path.exists(logo_file):
            logo = ImageClip(logo_file).set_duration(final_clip.duration).set_opacity(0.6)
            # Logo bem pequena (15% da largura do vídeo)
            logo = vfx.resize(logo, width=int(final_clip.w * 0.15))
            logo = logo.set_position(("right", "bottom")).margin(right=15, bottom=15, opacity=0)
            result = CompositeVideoClip([final_clip, logo])
        else:
            result = final_clip

        result.write_videofile(output, codec="libx264", audio_codec="aac", fps=24, logger=None, ffmpeg_params=["-pix_fmt", "yuv420p"])
        clip.close()
        return output
    except Exception as e:
        st.error(f"Erro na renderização: {e}")
        return None

# --- 3. BARRA LATERAL (ESTILO ADICONE.PNG) ---
with st.sidebar:
    st.markdown('<div class="logo-sidebar-container">', unsafe_allow_html=True)
    # Tenta carregar a logonova.png
    if os.path.exists("logonova.png"):
        st.image("logonova.png", width=180)
    else:
        st.markdown("<h2 style='color:white;'>VIDIOM.AI</h2>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="menu-item active-menu">🏠 Estúdio Criativo</div>', unsafe_allow_html=True)
    st.markdown('<div class="menu-item">🌍 Explorar</div>', unsafe_allow_html=True)
    st.markdown('<div class="menu-item">📁 Minhas Criações</div>', unsafe_allow_html=True)
    st.write("---")
    
    nav = st.radio("Ferramentas", ["Editor de Cortes", "Planos de Upgrade"], label_visibility="collapsed")
    
    st.write("---")
    st.markdown('<a class="btn-upgrade">🚀 Faça Upgrade Agora</a>', unsafe_allow_html=True)
    st.markdown('<div class="menu-item">🎁 Indique um Amigo</div>', unsafe_allow_html=True)

# --- 4. ÁREA CENTRAL ---
if nav == "Editor de Cortes":
    st.title("🎬 Creative Studio")
    uploaded = st.file_uploader("Selecione o vídeo para transformar em Short", type=["mp4", "mov"])
    
    if uploaded:
        with open("temp_in.mp4", "wb") as f: f.write(uploaded.getbuffer())
        
        st.video("temp_in.mp4")
        
        with VideoFileClip("temp_in.mp4") as v: dur = int(v.duration)
        t_range = st.slider("Selecione o trecho", 0, dur, (0, min(10, dur)))
        
        if st.button("Gerar Short com Marca d'água", type="primary"):
            with st.status("Processando..."):
                res = process_vidiom_final("temp_in.mp4", t_range[0], t_range[1])
                if res:
                    st.success("Corte concluído!")
                    with open(res, "rb") as f:
                        st.download_button("📥 BAIXAR VÍDEO", f, file_name="vidiom_short.mp4")
else:
    st.write("### Área de Assinaturas")
    st.info("Aqui você pode configurar os planos que vimos nas imagens anteriores.")
