import streamlit as st
import os
from moviepy.video.io.VideoFileClip import VideoFileClip
import moviepy.video.fx.all as vfx 
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.VideoClip import TextClip

# --- 1. CONFIGURAÇÃO E CSS (ESTILO PREMIUM UNIFICADO) ---
st.set_page_config(page_title="VIDIOM AI | Professional", layout="wide")

st.markdown("""
    <style>
    @keyframes fadeInUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
    @keyframes shimmer { 0% { background-position: -200% 0; } 100% { background-position: 200% 0; } }

    .stApp { background-color: #0d0d0d; color: #ffffff; }
    
    .vidiom-logo-top {
        text-align: center; font-family: 'Inter', sans-serif; font-size: 30px;
        letter-spacing: 7px; text-transform: uppercase; padding: 20px 0;
        background: linear-gradient(to right, #d9d9d9 0%, #ffffff 50%, #d9d9d9 100%);
        background-size: 200% auto; -webkit-background-clip: text;
        -webkit-text-fill-color: transparent; animation: shimmer 4s infinite linear;
    }

    /* ESTILO DOS CARDS DE PLANOS */
    .plan-card { background: #252526; border-radius: 12px; padding: 20px; margin-bottom: 15px; border: 2px solid transparent; }
    .plan-card.active { border-color: #3b82f6; background: #2d2d2e; }
    .price-large { font-size: 28px; font-weight: bold; float: right; }
    .benefits-box { background: #1a1a1b; border-radius: 15px; padding: 30px; height: 100%; }
    
    /* ESTILO DO EDITOR */
    .video-frame-vidiom { background-color: #1a1a1b; border-radius: 20px; padding: 30px; border: 1px solid #262627; }
    .stVideo { border-radius: 20px !important; overflow: hidden !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. MOTOR DE PROCESSAMENTO (CORREÇÃO DE ERRO 32) ---
def process_video_vidiom(video_in, start, end):
    output_path = "vidiom_final.mp4"
    try:
        clip = VideoFileClip(video_in).subclip(start, end)
        h = clip.h
        target_w = int(h * (9/16))
        if target_w % 2 != 0: target_w -= 1 # Garante dimensões pares
        
        clip_v = vfx.crop(clip, x_center=clip.w/2, width=target_w).copy()
        
        # Tenta add marca d'água interna
        try:
            wm = (TextClip("VIDIOM.AI", fontsize=25, color='white', font='Arial-Bold')
                  .set_opacity(0.5).set_duration(clip_v.duration).set_position(('right', 'bottom')).margin(right=20, bottom=40, opacity=0))
            final = CompositeVideoClip([clip_v, wm])
        except:
            final = clip_v

        final.write_videofile(output_path, codec="libx264", audio_codec="aac", fps=24, logger=None, ffmpeg_params=["-pix_fmt", "yuv420p"])
        clip.close()
        return output_path
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# --- 3. MENU LATERAL (SIDEBAR) ---
with st.sidebar:
    st.markdown('<div class="vidiom-logo-top" style="font-size:20px;">VIDIOM.AI</div>', unsafe_allow_html=True)
    st.write("---")
    # Menu de navegação igual ao MindVideo
    choice = st.radio("Menu", ["🎬 Video Editor", "💎 Upgrade Plan", "🤖 AI Settings"])
    st.write("---")
    st.info("Credits: 05 left")

# --- 4. TELAS DO APLICATIVO ---

if choice == "🎬 Video Editor":
    st.markdown('<div class="vidiom-logo-top">VIDIOM.AI</div>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Upload long video", type=["mp4", "mov"])
    
    if uploaded_file:
        with open("temp.mp4", "wb") as f: f.write(uploaded_file.getbuffer())
        with VideoFileClip("temp.mp4") as v:
            dur = int(v.duration)

        st.markdown('<div class="video-frame-vidiom">', unsafe_allow_html=True)
        st.video("temp.mp4")
        st.markdown('</div>', unsafe_allow_html=True)
        
        time_range = st.slider("Select Cut Range", 0, dur, (0, min(60, dur)))
        
        if st.button("Generate Short Video", type="primary"):
            with st.status("Processing..."):
                res = process_video_vidiom("temp.mp4", time_range[0], time_range[1])
                if res:
                    st.success("Done!")
                    with open(res, "rb") as f:
                        st.download_button("📥 DOWNLOAD", f, file_name="short.mp4")

elif choice == "💎 Upgrade Plan":
    st.markdown('<div class="vidiom-logo-top">VIDIOM.AI</div>', unsafe_allow_html=True)
    
    billing = st.radio("Billing", ["Monthly", "Annual (-57%)"], horizontal=True)
    
    c_left, c_right = st.columns([1, 1.2])
    with c_left:
        # Layout de planos
        st.markdown(f'<div class="plan-card active"><span class="price-large">{"$29.9" if billing=="Monthly" else "$15.9"}</span><div style="font-size: 20px; font-weight: bold;">Pro Plan</div><div style="color:#3b82f6;">✦ 1000 Credits</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="plan-card"><span class="price-large">{"$69.9" if billing=="Monthly" else "$39.9"}</span><div style="font-size: 20px; font-weight: bold;">Max Plan</div><div style="color:#3b82f6;">✦ 2500 Credits</div></div>', unsafe_allow_html=True)
    
    with c_right:
        st.markdown('<div class="benefits-box"><h3>Pro Benefits</h3><li>No Watermark</li><li>HD 1080p</li><li>All AI Models Access</li><li>Priority Support</li></div>', unsafe_allow_html=True)
        st.button("Upgrade Now", use_container_width=True, type="primary")

else:
    st.write("### AI Engine Settings")
    st.selectbox("Default Model", ["Luma Ray 2.0", "Vidu Q2", "Jimeng Pro"])
