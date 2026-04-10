import streamlit as st
import urllib.parse
import random
import re
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

# --- 1. ESTILO PREMIUM ---
st.set_page_config(page_title="Vidiom AI | All-in-One", layout="wide", page_icon="🎬")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #e0e0e0; }
    [data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 1px solid #1a1a1a; }
    h1, h2, h3 { font-family: 'Inter', sans-serif; background: -webkit-linear-gradient(#fff, #888); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .stButton>button { width: 100%; background: linear-gradient(135deg, #6366f1, #a855f7); color: white; border: none; padding: 12px; border-radius: 12px; font-weight: bold; }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea { background-color: #0f0f0f !important; border: 1px solid #222 !important; color: white !important; border-radius: 10px !important; }
    .stTabs [data-baseweb="tab"] { color: #888; font-weight: bold; }
    .stTabs [data-baseweb="tab--active"] { color: #fff; border-bottom-color: #6366f1; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CONFIGURAÇÕES ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except:
    st.error("Erro: Configure sua GEMINI_API_KEY.")

def get_video_id(url):
    pattern = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
    match = re.search(pattern, url)
    return match.group(1) if match else None

# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("🛰️ VIDIOM AI")
    email = st.text_input("E-mail de acesso", placeholder="seu@email.com")
    if email:
        st.success("⚡ 100 Créditos Disponíveis")

# --- 4. INTERFACE ---
st.title("Estúdio de Criação Viral")

if not email:
    st.warning("👋 Digite seu e-mail para começar.")
else:
    tab1, tab2, tab3 = st.tabs(["✂️ Cortes & Legendas", "🎨 Imagem Ultra", "🎥 Vídeo IA"])

    # ABA 1: CORTES (O CORAÇÃO DO SAAS)
    with tab1:
        st.subheader("🧬 Viral Slice (YouTube -> Shorts/Kwai/TikTok)")
        url_yt = st.text_input("Cole o link do vídeo:")
        if st.button("Analisar e Criar Cortes"):
            vid_id = get_video_id(url_yt)
            with st.spinner("IA extraindo o melhor do conteúdo..."):
                transcript = ""
                if vid_id:
                    try:
                        t_list = YouTubeTranscriptApi.list_transcripts(vid_id)
                        t = t_list.find_transcript(['pt', 'en']).fetch()
                        transcript = " ".join([i['text'] for i in t])
                    except: transcript = None
                
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt = (
                    f"Analise o vídeo: {url_yt}. Transcrição: {transcript[:5000] if transcript else 'Indisponível'}. "
                    "Crie 2 roteiros de cortes virais. Para cada um: \n"
                    "1. Título Impactante. \n"
                    "2. GANCHO (Texto para os primeiros 3s). \n"
                    "3. Roteiro com [GUIA DE LEGENDAS COLORIDAS] para retenção estilo Hormozi."
                )
                res = model.generate_content(prompt)
                st.markdown("---")
                st.markdown(res.text)

    # ABA 2: IMAGENS (MOTOR FLUX)
    with tab2:
        st.subheader("🎨 Gerador de Imagem Premium")
        img_desc = st.text_input("Descreva a imagem (Inglês ajuda):")
        if st.button("Gerar Imagem"):
            with st.spinner("Desenhando..."):
                seed = random.randint(1, 999999)
                full_p = urllib.parse.quote(f"{img_desc}, cinematic lighting, 8k, realistic")
                url = f"https://image.pollinations.ai/prompt/{full_p}?width=1024&height=1024&nologo=true&seed={seed}&model=flux"
                st.image(url, use_container_width=True)

    # ABA 3: VÍDEOS
    with tab3:
        st.subheader("🎥 Animação com IA")
        vid_desc = st.text_input("O que acontece no vídeo?")
        if st.button("Criar Clipe"):
            with st.spinner("Renderizando..."):
                v_url = f"https://pollinations.ai/p/{urllib.parse.quote(vid_desc)}?width=1280&height=720&model=video&seed={random.randint(1,999)}"
                st.components.v1.html(f'<iframe src="{v_url}" width="100%" height="450" style="border:2px solid #6366f1; border-radius:15px;" allowfullscreen></iframe>', height=500)
