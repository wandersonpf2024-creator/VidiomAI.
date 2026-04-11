import streamlit as st
import os
from moviepy.video.io.VideoFileClip import VideoFileClip
import moviepy.video.fx.all as vfx 
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.VideoClip import TextClip

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="VIDIOM AI | Global", layout="wide")

st.markdown("""
    <style>
    /* ANIMATIONS DEFINITIONS */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes scaleIn {
        from { opacity: 0; transform: scale(0.95); }
        to { opacity: 1; transform: scale(1); }
    }

    /* GENERAL STYLING */
    .stApp { background-color: #0d0d0d; color: #ffffff; }
    .main .block-container { max-width: 1100px !important; margin: 0 auto; }

    /* LOGO TOP */
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

    /* HEADER BOX */
    .header-box {
        animation: fadeInUp 1s ease-out forwards;
        display: flex;
        align-items: center;
        margin-bottom: 20px;
    }
    .header-text { font-size: 22px; font-weight: bold; margin-left: 12px; }

    /* VIDEO PREVIEW CONTAINER (ROUNDED) */
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
        border-radius: 20px !important; /* Your 4 rounded corners */
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }

    /* INPUTS & BUTTONS ANIMATION */
    .stSlider, .stTextArea, .stFileUploader, .stButton {
        animation: fadeInUp 0.8s ease-out 0.4s backwards;
    }

    /* CONVERT BUTTON (WHITE PILL STYLE) */
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

    /* CAPTION STYLE BUTTONS */
    .stButton > button {
        background-color: #1c1c1e;
        color: #8e8e93;
        border: 1px solid #3a3a3c;
        border-radius: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. VIDEO LOGIC (WATERMARK + 9:16 CROP) ---
def process_vidiom_global(video_in, start, end):
    output_path = "vidiom_export.mp4"
    try:
        with VideoFileClip(video_in, audio=True).subclip(start, end) as clip:
            # 9:16 Vertical Transformation
            h = clip.h
            w_v = h * (9/16)
            clip_v = vfx.crop(clip, x_center=clip.w/2, width=w_v)
            
            # Internal Watermark [VIDIOM.AI]
            try:
                wm = (TextClip("VIDIOM.AI", fontsize=25, color='white', font='Arial-Bold')
                         .set_opacity(0.5)
                         .set_duration(clip.duration)
                         .set_position(('right', 'bottom'))
                         .margin(right=20, bottom=40, opacity=0))
                final = CompositeVideoClip([clip_v, wm])
            except:
                final = clip_v

            final.write_videofile(output_path, codec="libx264", audio_codec="aac", threads=1, logger=None)
        return output_path
    except Exception as e:
        st.error(f"Processing error: {e}")
        return None

# --- 3. GLOBAL INTERFACE ---

# Top Branding
st.markdown('<div class="vidiom-logo-top">VIDIOM.AI</div>', unsafe_allow_html=True)

# Header
st.markdown('<div class="header-box">🎬 <span class="header-text">Convert long videos into shorts</span></div>', unsafe_allow_html=True)

# File Uploader
uploaded_file = st.file_uploader("", type=["mp4", "mov"])

if uploaded_file:
    with open("temp_vid.mp4", "wb") as f: f.write(uploaded_file.getbuffer())
    
    with VideoFileClip("temp_vid.mp4") as v:
        total_dur = int(v.duration)

    # Video Frame with Rounded Corners
    st.markdown('<div class="video-frame-vidiom">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.video("temp_vid.mp4")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.write("### Select the clip duration")
    time_range = st.slider("", 0, total_dur, (0, min(60, total_dur)))

    st.write("### Select caption style")
    cols = st.columns(10)
    for i in range(10):
        with cols[i]: st.button(f"Style {i+1}", key=f"style_{i}")

    st.write("---")
    
    c_input, c_action = st.columns([3, 1])
    with c_input:
        st.text_area("Video Context", placeholder="Describe the climax or main scene...")
    with c_action:
        st.write("##")
        if st.button("Convert"):
            with st.status("🎬 Rendering 9:16 viral video...", expanded=False):
                result = process_vidiom_global("temp_vid.mp4", time_range[0], time_range[1])
                if result:
                    st.success("Ready to go!")
                    with open(result, "rb") as f:
                        st.download_button("📥 DOWNLOAD NOW", f, file_name="vidiom_viral.mp4")
else:
    st.info("Drag and drop your video to start the magic.")

# Footer
st.markdown("<br><center><small>© 2026 VIDIOM.AI - Smart Video Edition</small></center>", unsafe_allow_html=True)
