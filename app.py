import streamlit as st
import os
from moviepy.video.io.VideoFileClip import VideoFileClip
import moviepy.video.fx.all as vfx 
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.VideoClip import TextClip

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="VIDIOM AI", layout="wide")

st.markdown("""
    <style>
    @keyframes fadeInUp { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }
    @keyframes scaleIn { from { opacity: 0; transform: scale(0.95); } to { opacity: 1; transform: scale(1); } }

    .stApp { background-color: #0d0d0d; color: #ffffff; }
    .main .block-container { max-width: 1100px !important; margin: 0 auto; }

    .vidiom-logo-top {
        animation: fadeInUp 0.8s ease-out forwards;
        text-align: center; font-family: 'Inter', sans-serif; font-size: 32px;
        letter-spacing: 8px; font-weight: 300; text-transform: uppercase; padding: 20px 0;
    }

    .video-frame-vidiom {
        animation: scaleIn 0.8s ease-out 0.2s backwards;
        background-color: #1a1a1b; border-radius: 20px; padding: 30px;
        border: 1px solid #262627; margin-bottom: 25px;
    }

    .stVideo { overflow: hidden !important; border-radius: 20px !important; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }

    div.stButton > button:first-child {
        background: white !important; color: black !important; border-radius: 30px !important;
        padding: 12px 50px !important; font-weight: bold !important; border: none !important;
        float: right; box-shadow: 0 0 20px rgba(255, 255, 255, 0.2);
    }

    .stButton > button { background-color: #1c1c1e; color: #8e8e93; border: 1px solid #3a3a3c; border-radius: 12px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. FIXED VIDEO LOGIC (ENSURING IMAGE VISIBILITY) ---
def process_vidiom_fixed(video_in, start, end):
    output_path = "vidiom_final_render.mp4"
    try:
        # Load clip and ensure it's RGB
        clip = VideoFileClip(video_in, audio=True).subclip(start, end)
        
        # 1. Calculate Vertical Crop (9:16)
        h = clip.h
        target_w = h * (9/16)
        
        # Use vfx.crop and immediately call .copy() to preserve image data
        clip_v = vfx.crop(clip, x_center=clip.w/2, width=target_w).copy()
        
        # 2. Add Watermark [VIDIOM.AI]
        try:
            wm = (TextClip("VIDIOM.AI", fontsize=25, color='white', font='Arial-Bold')
                     .set_opacity(0.5)
                     .set_duration(clip_v.duration)
                     .set_position(('right', 'bottom'))
                     .margin(right=20, bottom=40, opacity=0))
            final = CompositeVideoClip([clip_v, wm])
        except:
            final = clip_v

        # 3. CRITICAL: Force libx264 and set pixel format for compatibility
        final.write_videofile(
            output_path, 
            codec="libx264", 
            audio_codec="aac", 
            temp_audiofile='temp-audio.m4a', 
            remove_temp=True, 
            fps=24, 
            logger=None,
            ffmpeg_params=["-pix_fmt", "yuv420p"] # This line ensures the image shows on all devices
        )
        
        clip.close()
        final.close()
        return output_path
    except Exception as e:
        st.error(f"Render Error: {e}")
        return None

# --- 3. INTERFACE ---
st.markdown('<div class="vidiom-logo-top">VIDIOM.AI</div>', unsafe_allow_html=True)
st.markdown('<h4 style="color:#8e8e93; font-weight:normal;">‹ Convert long videos into shorts</h4>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("", type=["mp4", "mov"])

if uploaded_file:
    with open("input_cache.mp4", "wb") as f: f.write(uploaded_file.getbuffer())
    
    with VideoFileClip("input_cache.mp4") as v:
        dur = int(v.duration)

    st.markdown('<div class="video-frame-vidiom">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.video("input_cache.mp4")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.write("### Select duration")
    time_range = st.slider("", 0, dur, (0, min(60, dur)))

    st.write("### Style")
    cols = st.columns(10)
    for i in range(10):
        with cols[i]: st.button(f"S{i+1}", key=f"s_{i}")

    st.write("---")
    c1, c2 = st.columns([3, 1])
    with c1:
        st.text_area("Context", placeholder="What is this video about?")
    with c2:
        st.write("##")
        if st.button("Convert"):
            with st.status("🎬 Encoding viral video...", expanded=False):
                res = process_vidiom_fixed("input_cache.mp4", time_range[0], time_range[1])
                if res:
                    st.success("Render complete!")
                    with open(res, "rb") as f:
                        st.download_button("📥 DOWNLOAD", f, file_name="vidiom_short.mp4")
else:
    st.info("Upload a video to start.")

st.markdown("<br><center><small>© 2026 VIDIOM.AI</small></center>", unsafe_allow_html=True)
