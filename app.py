import streamlit as st
import google.generativeai as genai
import re
from youtube_transcript_api import YouTubeTranscriptApi

# --- CONFIG PAGE ---
st.set_page_config(page_title="VIDIOM AI - Viral Video Engine", layout="wide")

# --- STYLE ---
st.markdown("""
<style>
.stApp { background: #050505; color: #fff; }
h1, h2, h3 { color: white; }
.stButton>button {
    background: #6366f1;
    color: white;
    border-radius: 10px;
    font-weight: bold;
    border: none;
    padding: 12px;
}
.script-box {
    background: #111;
    border: 1px solid #222;
    padding: 20px;
    border-radius: 12px;
    font-family: monospace;
    color: #00ff88;
}
</style>
""", unsafe_allow_html=True)

# --- SETUP AI (MODELO CORRIGIDO) ---
def setup_engine():
    try:
        if "GEMINI_API_KEY" in st.secrets:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            return genai.GenerativeModel('gemini-pro')  # ✅ modelo que funciona
    except Exception as e:
        st.error(f"AI Error: {e}")
        return None
    return None

model = setup_engine()

# --- EXTRACT YOUTUBE ID ---
def extrair_id(url):
    pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(pattern, url)
    return match.group(1) if match else None

# --- HEADER ---
st.title("🚀 VIDIOM AI – Viral Video Engine")
st.markdown("### Turn Any Video Into Viral Shorts in Seconds")

st.markdown("---")

col1, col2 = st.columns(2)

# --- LEFT SIDE ---
with col1:
    st.subheader("📥 Video Input")

    url_input = st.text_input("Paste YouTube link:")

    estilo = st.selectbox(
        "Choose Style:",
        ["Hormozi Style", "Minimal", "High Impact", "Podcast"]
    )

    if st.button("🚀 Generate Viral Clip"):

        if not url_input:
            st.warning("Insert a valid video link.")
        elif not model:
            st.error("API error. Check your key.")
        else:
            with st.status("Analyzing video...", expanded=True) as status:

                video_id = extrair_id(url_input)
                transcricao = ""

                # --- GET TRANSCRIPT ---
                if video_id:
                    try:
                        st.write("Extracting transcript...")
                        t = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'pt'])
                        transcricao = " ".join([i['text'] for i in t])
                    except:
                        st.write("No transcript found. Using AI inference.")

                # --- PROMPT SUPER OTIMIZADO ---
                prompt = f"""
You are a world-class viral content strategist specialized in TikTok, Instagram Reels, and YouTube Shorts.

Your job is to IDENTIFY the most addictive and high-retention moment from a video.

Video URL: {url_input}

Transcript:
{transcricao[:3000]}

If transcript is missing, infer based on context.

Analyze deeply using:
- Curiosity gaps
- Emotional spikes
- Controversy
- Storytelling tension
- Pattern interrupts

OUTPUT:

🔥 HOOK (first 1–3 seconds):
Write a SCROLL-STOPPING opening line.

⏱️ BEST CLIP:
Give the exact timestamp (start - end) of the most viral moment.

🎬 CAPTION SCRIPT:
Rewrite into short, punchy subtitles (3–6 words per line).

✨ POWER WORDS:
Highlight impactful words in UPPERCASE.

🧠 PSYCHOLOGY:
Explain WHY this clip will retain attention.

⚡ VIRAL SCORE:
Score from 1 to 10.

💡 EXTRA:
Suggest 2 alternative hooks for A/B testing.

Style: {estilo}
"""

                try:
                    st.write("Generating viral script...")
                    res = model.generate_content(prompt)

                    st.session_state.resultado = res.text
                    status.update(label="Done!", state="complete")

                except Exception as e:
                    st.error(f"AI Error: {e}")

# --- RIGHT SIDE ---
with col2:
    st.subheader("🎬 Viral Output")

    if "resultado" in st.session_state:
        st.markdown(
            f'<div class="script-box">{st.session_state.resultado}</div>',
            unsafe_allow_html=True
        )

        st.download_button(
            "📥 Download Script",
            st.session_state.resultado,
            file_name="viral_script.txt"
        )
    else:
        st.info("Your viral script will appear here.")

# --- FOOTER ---
st.markdown("---")
st.caption("VIDIOM AI © 2026 – AI Viral Content Engine")
