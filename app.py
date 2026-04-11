import streamlit as st
import google.generativeai as genai
import re
from youtube_transcript_api import YouTubeTranscriptApi

# --- CONFIG PAGE ---
st.set_page_config(page_title="VIDIOM AI - Viral Video Engine", layout="wide", page_icon="🚀")

# --- STYLE ---
st.markdown("""
<style>
    .stApp { background: #050505; color: #fff; }
    h1, h2, h3 { color: white; font-family: 'Inter', sans-serif; }
    .stButton>button {
        background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%);
        color: white;
        border-radius: 10px;
        font-weight: bold;
        border: none;
        padding: 12px;
        width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 20px rgba(99, 102, 241, 0.4);
    }
    .script-box {
        background: #0a0a0a;
        border: 1px solid #222;
        padding: 25px;
        border-radius: 12px;
        font-family: 'Courier New', monospace;
        color: #00ff88;
        line-height: 1.6;
        white-space: pre-wrap;
    }
</style>
""", unsafe_allow_html=True)

# --- SETUP AI ---
def setup_engine():
    try:
        if "GEMINI_API_KEY" in st.secrets:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            # Usando o flash-latest para velocidade máxima
            return genai.GenerativeModel("gemini-1.5-flash-latest")
    except Exception as e:
        st.error(f"AI Configuration Error: {e}")
        return None
    return None

model = setup_engine()

# --- EXTRACT YOUTUBE ID (MELHORADO) ---
def extrair_id(url):
    pattern = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
    match = re.search(pattern, url)
    return match.group(1) if match else None

# --- HEADER ---
st.title("🚀 VIDIOM AI – Viral Video Engine")
st.markdown("### Turn Any Video Into Viral Shorts in Seconds")
st.markdown("---")

col1, col2 = st.columns(2, gap="large")

# --- LEFT SIDE: INPUT ---
with col1:
    st.subheader("📥 Video Input")
    url_input = st.text_input("Paste YouTube link:", placeholder="https://www.youtube.com/watch?v=...")

    estilo = st.selectbox(
        "Choose Style:",
        ["Hormozi Style (High Retention)", "Minimalist (Clean)", "High Impact (Aggressive)", "Podcast Style"]
    )

    if st.button("🚀 Generate Viral Script"):
        if not url_input:
            st.warning("Please insert a valid video link.")
        elif not model:
            st.error("AI Model not initialized. Check your API Key in Secrets.")
        else:
            with st.status("Engine at work...", expanded=True) as status:
                video_id = extrair_id(url_input)
                transcricao = ""

                # --- GET TRANSCRIPT ---
                if video_id:
                    try:
                        st.write("🔍 Searching for transcript...")
                        # Tenta português e inglês
                        t = YouTubeTranscriptApi.get_transcript(video_id, languages=['pt', 'en'])
                        transcricao = " ".join([i['text'] for i in t])
                        st.write("✅ Transcript extracted.")
                    except:
                        st.write("⚠️ No transcript found. AI will analyze based on link metadata.")

                # --- PROMPT DE ELITE ---
                prompt = f"""
                You are a world-class viral content strategist. 
                Goal: Extract the most addictive 30-60s segment from this video.

                Video URL: {url_input}
                Transcript: {transcricao[:4000]}

                Format your response with these exact sections:
                
                🔥 HOOK: (A scroll-stopping line)
                ⏱️ TIMESTAMPS: (Start - End)
                🎬 CAPTION SCRIPT: (Max 5 words per line, use emojis)
                ✨ POWER WORDS: (Words to highlight in YELLOW)
                🧠 WHY IT WORKS: (Psychological trigger)
                ⚡ VIRAL SCORE: (1-10)
                
                Style: {estilo}
                """

                try:
                    st.write("🧠 AI is analyzing viral triggers...")
                    # AQUI ESTAVA O ERRO: Chamando o prompt real
                    res = model.generate_content(prompt)
                    
                    if res.text:
                        st.session_state.resultado = res.text
                        status.update(label="Analysis Complete!", state="complete")
                    else:
                        st.error("AI returned an empty response.")
                except Exception as e:
                    st.error(f"AI Generation Error: {e}")

# --- RIGHT SIDE: OUTPUT ---
with col2:
    st.subheader("🎬 Viral Output")

    if "resultado" in st.session_state:
        st.markdown(
            f'<div class="script-box">{st.session_state.resultado}</div>',
            unsafe_allow_html=True
        )

        st.download_button(
            label="📥 Download Viral Script",
            data=st.session_state.resultado,
            file_name="vidiom_viral_script.txt",
            mime="text/plain"
        )
    else:
        st.info("Paste a link and click 'Generate' to see the magic happen.")

# --- FOOTER ---
st.markdown("---")
st.caption("VIDIOM AI © 2026 – Powered by Gemini 1.5 Pro Engine")
