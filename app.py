import streamlit as st
import os
from moviepy.video.io.VideoFileClip import VideoFileClip
import moviepy.video.fx.all as vfx 
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.VideoClip import TextClip

# --- 1. CONFIGURAÇÃO DE TEMA DARK (ESTILO MINDVIDEO) ---
st.set_page_config(page_title="VIDIOM AI", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0d0d0d; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #000000 !important; border-right: 1px solid #1e1e1e; }
    
    .logo-container-sidebar { text-align: center; padding: 10px 0; margin-bottom: 20px; }
    
    .menu-item {
        padding: 10px; border-radius: 8px; margin-bottom: 5px;
        display: flex; align-items: center; gap: 12px; color: #d1d1d1; cursor: pointer;
    }
    .active-menu { background-color: #262626; color: white; font-weight: bold; }

    .btn-upgrade {
        background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%);
        color: white; padding: 12px; border-radius: 8px; text-align: center;
        font-weight: bold; margin-top: 20px; display: block; text-decoration: none;
    }

    .video-card { background-color: #141414; border-radius: 15px; padding: 20px; border: 1px solid #262627; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. MOTOR DE VÍDEO COM MARCA D'ÁGUA REFORÇADA ---
def process_vidiom_with_watermark(video_path, start, end):
    output = "vidiom_branded.mp4"
    try:
        clip = VideoFileClip(video_path).subclip(start, end)
        
        # Ajuste de dimensões para 9:16 (Sempre Par)
        h = clip.h
        w = int(h * (9/16))
        if w % 2 != 0: w -= 1
        
        # Corte centralizado
        final_clip = vfx.crop(clip, x_center=clip.w/2, width=w).copy()
        
        # TENTATIVA DE MARCA D'ÁGUA
        try:
            # Se o ImageMagick não estiver no servidor, o TextClip dará erro.
            # Criamos o texto da marca d'água
            txt_clip = (TextClip("VIDIOM.AI", fontsize=35, color='white', font='Arial-Bold')
                        .set_duration(final_clip.duration)
                        .set_opacity(0.6)
                        .set_position(("center", h - 100))) # 100px acima do fundo
            
            # Sobreposição
            result = CompositeVideoClip([final_clip, txt_clip])
        except Exception as e:
            st.warning("Nota: Renderização de texto (marca d'água) requer ImageMagick. Gerando vídeo limpo.")
            result = final_clip

        result.write_videofile(
            output, 
            codec="libx264", 
            audio_codec="aac", 
            fps=24, 
            logger=None, 
            ffmpeg_params=["-pix_fmt", "yuv420p"]
        )
        
        clip.close()
        result.close()
        return output
    except Exception as e:
        st.error(f"Render Error: {e}")
        return None

# --- 3. SIDEBAR COM A SUA NOVA LOGO ---
with st.sidebar:
    st.markdown('<div class="logo-container-sidebar">', unsafe_allow_html=True)
    # Tenta usar a sua imagem enviada (lonova.png)
    try:
        st.image("lonova.png", width=200)
    except:
        st.markdown("<h2 style='text-align:center;'>VIDIOM.AI</h2>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="menu-item active-menu">🏠 Estúdio Criativo</div>', unsafe_allow_html=True)
    st.markdown('<div class="menu-item">📁 Minhas Criações</div>', unsafe_allow_html=True)
    st.write("---")
    
    nav = st.radio("Ferramentas", ["Cortar Vídeo", "Planos de Upgrade"], label_visibility="collapsed")
    
    st.write("---")
    st.markdown('<a class="btn-upgrade">🚀 Faça Upgrade Agora</a>', unsafe_allow_html=True)

# --- 4. DASHBOARD ---
if nav == "Cortar Vídeo":
    st.title("🎬 Estúdio de Cortes")
    uploaded = st.file_uploader("Arraste seu vídeo aqui", type=["mp4", "mov"])
    
    if uploaded:
        with open("input.mp4", "wb") as f: f.write(uploaded.getbuffer())
        
        c1, c2 = st.columns([1.5, 1])
        with c1:
            st.markdown('<div class="video-card">', unsafe_allow_html=True)
            st.video("input.mp4")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with c2:
            with VideoFileClip("input.mp4") as v: dur = int(v.duration)
            t_range = st.slider("Selecione o tempo", 0, dur, (0, min(15, dur)))
            
            if st.button("Gerar Vídeo com Marca d'água", type="primary", use_container_width=True):
                with st.status("Renderizando..."):
                    res = process_vidiom_with_watermark("input.mp4", t_range[0], t_range[1])
                    if res:
                        st.success("Vídeo pronto!")
                        with open(res, "rb") as f:
                            st.download_button("📥 BAIXAR AGORA", f, file_name="vidiom_short.mp4")
else:
    st.write("### Página de Planos em Manutenção")
