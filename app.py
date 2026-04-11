import streamlit as st
import os
from moviepy.video.io.VideoFileClip import VideoFileClip
import moviepy.video.fx.all as vfx 
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.VideoClip import TextClip

# --- 1. CONFIGURAÇÃO DE TEMA DARK ---
st.set_page_config(page_title="VIDIOM AI", layout="wide")

st.markdown("""
    <style>
    /* RESET DE CORES PARA PRETO ABSOLUTO */
    .stApp {
        background-color: #0d0d0d;
        color: #ffffff;
    }

    /* BARRA LATERAL (SIDEBAR) PRETA */
    [data-testid="stSidebar"] {
        background-color: #000000 !important;
        border-right: 1px solid #1e1e1e;
    }

    /* LOGO VIDIOM.AI NO TOPO DA BARRA LATERAL */
    .vidiom-logo-sidebar {
        text-align: center;
        font-family: 'Inter', sans-serif;
        font-size: 22px;
        letter-spacing: 5px;
        font-weight: 300;
        text-transform: uppercase;
        padding: 20px 0;
        background: linear-gradient(to right, #d9d9d9 0%, #ffffff 50%, #d9d9d9 100%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shimmer 4s infinite linear;
    }
    @keyframes shimmer { 0% { background-position: -200% 0; } 100% { background-position: 200% 0; } }

    /* MENU ITEMS ESTILO MINDVIDEO */
    .menu-item {
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 5px;
        display: flex;
        align-items: center;
        gap: 12px;
        color: #d1d1d1;
        cursor: pointer;
    }
    .menu-item:hover {
        background-color: #1a1a1a;
    }
    .active-menu {
        background-color: #262626;
        color: white;
        font-weight: bold;
    }

    /* BOTÃO UPGRADE (ROXO/AZUL IGUAL À IMAGEM) */
    .btn-upgrade {
        background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%);
        color: white;
        padding: 12px;
        border-radius: 8px;
        text-align: center;
        font-weight: bold;
        margin-top: 20px;
        cursor: pointer;
        text-decoration: none;
        display: block;
    }

    /* ESTILO DO EDITOR (ÁREA CENTRAL) */
    .main-container {
        padding: 20px;
    }
    .video-card {
        background-color: #141414;
        border-radius: 15px;
        padding: 20px;
        border: 1px solid #262627;
    }

    /* INPUTS E SLIDERS DARK */
    .stSlider > div > div > div > div { background-color: #6366f1; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. MOTOR DE VÍDEO (FIXED) ---
def process_vidiom_core(video_path, start, end):
    output = "vidiom_render.mp4"
    try:
        clip = VideoFileClip(video_path).subclip(start, end)
        h = clip.h
        w = int(h * (9/16))
        if w % 2 != 0: w -= 1
        final = vfx.crop(clip, x_center=clip.w/2, width=w).copy()
        final.write_videofile(output, codec="libx264", audio_codec="aac", fps=24, logger=None, ffmpeg_params=["-pix_fmt", "yuv420p"])
        clip.close()
        return output
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# --- 3. BARRA LATERAL (SIDEBAR) ---
with st.sidebar:
    # Nome VIDIOM.AI no lugar do MindVideo
    st.markdown('<div class="vidiom-logo-sidebar">VIDIOM.AI</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="menu-item active-menu">🏠 Creative Studio</div>', unsafe_allow_html=True)
    st.markdown('<div class="menu-item">🌍 Explore</div>', unsafe_allow_html=True)
    st.markdown('<div class="menu-item">📁 My Creations</div>', unsafe_allow_html=True)
    st.write("---")
    
    # Navegação de funcionalidades
    nav = st.radio("Tools", ["Video to Short", "Text to Video", "AI Avatar", "Pricing Plan"], label_visibility="collapsed")
    
    st.write("---")
    st.markdown('<a class="btn-upgrade">🚀 Upgrade Now</a>', unsafe_allow_html=True)
    st.markdown('<div class="menu-item" style="margin-top:10px;">🎁 Refer a Friend</div>', unsafe_allow_html=True)

# --- 4. ÁREA PRINCIPAL (DASHBOARD) ---

if nav == "Video to Short":
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.title("🎬 Video to Short")
    st.write("Convert your landscape videos into viral 9:16 content.")
    
    uploaded = st.file_uploader("", type=["mp4", "mov"])
    
    if uploaded:
        with open("input_vidiom.mp4", "wb") as f: f.write(uploaded.getbuffer())
        
        col_v, col_edit = st.columns([1.5, 1])
        
        with col_v:
            st.markdown('<div class="video-card">', unsafe_allow_html=True)
            st.video("input_vidiom.mp4")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_edit:
            with VideoFileClip("input_vidiom.mp4") as v_temp:
                dur = int(v_temp.duration)
            
            st.write("### Settings")
            cut_range = st.slider("Select Segment (Seconds)", 0, dur, (0, min(30, dur)))
            
            if st.button("Generate Viral Short", use_container_width=True, type="primary"):
                with st.status("Creating your short..."):
                    res_path = process_vidiom_core("input_vidiom.mp4", cut_range[0], cut_range[1])
                    if res_path:
                        st.success("Ready to download!")
                        with open(res_path, "rb") as file_res:
                            st.download_button("📥 DOWNLOAD VIDEO", file_res, file_name="vidiom_short.mp4", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif nav == "Pricing Plan":
    # Aqui entra aquela tabela de planos que fizemos antes
    st.markdown('<h2 style="text-align:center;">Choose your plan</h2>', unsafe_allow_html=True)
    # ... (o código dos planos entra aqui)
    st.info("Plans page is active. Click on Editor to go back.")

# Footer Estilo API
with st.sidebar:
    st.write("##")
    cols_foot = st.columns(3)
    cols_foot[0].write("🌐")
    cols_foot[1].write("🎧")
    cols_foot[2].write("API")
