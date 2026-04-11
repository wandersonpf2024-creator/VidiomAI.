import streamlit as st
import os
from moviepy.video.io.VideoFileClip import VideoFileClip
import moviepy.video.fx.all as vfx 
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.VideoClip import ImageClip

# --- 1. CONFIGURAÇÃO DE ESTILO ORIGINAL (DARK & CLEAN) ---
st.set_page_config(page_title="VIDIOM AI | Video Editor", layout="wide")

st.markdown("""
    <style>
    /* Fundo escuro e fontes limpas */
    .stApp { background-color: #0d0d0d; color: #ffffff; }
    
    /* Logo centralizada com o brilho original */
    .vidiom-logo {
        text-align: center; font-family: 'Inter', sans-serif; font-size: 42px;
        letter-spacing: 10px; font-weight: 300; text-transform: uppercase; padding: 40px 0;
        background: linear-gradient(to right, #d9d9d9 0%, #d9d9d9 40%, #ffffff 50%, #d9d9d9 60%, #d9d9d9 100%);
        background-size: 200% auto; -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        animation: shimmer_smooth 4s infinite linear;
    }
    @keyframes shimmer_smooth { 0% { background-position: -200% 0; } 100% { background-position: 200% 0; } }
    
    /* Moldura do vídeo */
    .video-container {
        background-color: #1a1a1b; border-radius: 20px; padding: 20px;
        border: 1px solid #333; margin-bottom: 20px;
    }
    
    /* Botão de download de destaque */
    .stDownloadButton > button {
        background-color: #ffffff !important; color: #000000 !important;
        border-radius: 25px !important; font-weight: bold !important; width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. MOTOR DE VÍDEO COM MARCA D'ÁGUA (IMAGEM) ---
def render_video_clean(video_path, start, end):
    output = "vidiom_final.mp4"
    logo_file = "logonova.png" # Sua logo enviada
    
    try:
        clip = VideoFileClip(video_path).subclip(start, end)
        h = clip.h
        w = int(h * (9/16))
        if w % 2 != 0: w -= 1 # Garante dimensões pares
        
        # Crop para 9:16
        final_clip = vfx.crop(clip, x_center=clip.w/2, width=w).copy()
        
        # Aplica a logo como marca d'água se o arquivo existir
        if os.path.exists(logo_file):
            logo = (ImageClip(logo_file)
                    .set_duration(final_clip.duration)
                    .set_opacity(0.6))
            # Redimensiona para 15% da largura e coloca no canto
            logo = vfx.resize(logo, width=int(final_clip.w * 0.15))
            logo = logo.set_position(("right", "bottom")).margin(right=15, bottom=20, opacity=0)
            result = CompositeVideoClip([final_clip, logo])
        else:
            result = final_clip

        result.write_videofile(output, codec="libx264", audio_codec="aac", fps=24, logger=None, ffmpeg_params=["-pix_fmt", "yuv420p"])
        clip.close()
        return output
    except Exception as e:
        st.error(f"Erro: {e}")
        return None

# --- 3. INTERFACE PRINCIPAL ---

st.markdown('<div class="vidiom-logo">VIDIOM.AI</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload your video here", type=["mp4", "mov"])

if uploaded_file:
    with open("input_temp.mp4", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    col_pre, col_settings = st.columns([1.5, 1])
    
    with col_pre:
        st.markdown('<div class="video-container">', unsafe_allow_html=True)
        st.video("input_temp.mp4")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_settings:
        st.write("### ⚙️ Video Settings")
        with VideoFileClip("input_temp.mp4") as v:
            duration = int(v.duration)
        
        time_range = st.slider("Select Segment", 0, duration, (0, min(15, duration)))
        
        st.write("---")
        if st.button("CREATE VIRAL SHORT", type="primary", use_container_width=True):
            with st.status("🎬 Processing..."):
                final_path = render_video_clean("input_temp.mp4", time_range[0], time_range[1])
                if final_path:
                    st.success("Your video is ready!")
                    with open(final_path, "rb") as f:
                        st.download_button("📥 DOWNLOAD NOW", f, file_name="vidiom_short.mp4")

# Footer simples
st.write("##")
st.markdown("<center style='color:#555;'>Powered by VIDIOM.AI Engine</center>", unsafe_allow_html=True)
