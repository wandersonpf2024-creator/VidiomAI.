import streamlit as st
import urllib.parse
import random
import re
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

# --- 1. CONFIGURAÇÃO VISUAL (Vidiom AI Premium) ---
st.set_page_config(page_title="Vidiom AI | Pro Studio", layout="wide", page_icon="🎬")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #e0e0e0; }
    h1 { background: -webkit-linear-gradient(#fff, #888); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; }
    .stButton>button { width: 100%; background: linear-gradient(135deg, #6366f1, #a855f7); color: white; border: none; padding: 12px; border-radius: 12px; font-weight: bold; transition: 0.3s; }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(99, 102, 241, 0.4); }
    .stTextInput>div>div>input { background-color: #0f0f0f !important; border: 1px solid #333 !important; color: white !important; }
    .result-card { background: #0a0a0a; border: 1px solid #1a1a1a; padding: 20px; border-radius: 15px; border-left: 5px solid #6366f1; margin-top: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. MOTOR DE IA ---
def init_gemini():
    try:
        if "GEMINI_API_KEY" in st.secrets:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            return genai.GenerativeModel('gemini-1.5-flash')
    except: return None
    return None

ia_model = init_gemini()

def get_yt_id(url):
    pattern = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
    match = re.search(pattern, url)
    return match.group(1) if match else None

# --- 3. INTERFACE ---
st.title("🛰️ VIDIOM AI - Estúdio 2026")

with st.sidebar:
    st.subheader("Painel de Controle")
    user_email = st.text_input("Seu E-mail")
    if user_email: st.success("🚀 Plano Pro Ativo")

if not user_email:
    st.info("👋 Bem-vindo! Insira seu e-mail para desbloquear as ferramentas de IA.")
else:
    t1, t2, t3 = st.tabs(["✂️ Cortes por Link", "🎨 Gerador de Imagem", "🎥 Gerador de Vídeo"])

    # ABA 1: CORTES
    with t1:
        st.subheader("Roteirista de Cortes Virais")
        url_link = st.text_input("Cole o link (YouTube, TikTok, Instagram):", key="link_corte")
        if st.button("🧬 Analisar e Criar Corte"):
            with st.spinner("Analisando conteúdo..."):
                transcript = ""
                yid = get_yt_id(url_link)
                if yid:
                    try:
                        t_data = YouTubeTranscriptApi.get_transcript(yid, languages=['pt', 'en'])
                        transcript = " ".join([i['text'] for i in t_data])
                    except: transcript = "Link externo (Rede Social)."

                if ia_model:
                    prompt = f"Crie 2 roteiros de cortes para: {url_link}. Contexto: {transcript[:2000]}. Foque em: Título, Gancho e Legendas dinâmicas."
                    res = ia_model.generate_content(prompt)
                    st.markdown(f'<div class="result-card">{res.text}</div>', unsafe_allow_html=True)
                else: st.error("Erro na API do Google.")

    # ABA 2: IMAGENS
    with t2:
        st.subheader("IA de Imagem (Flux Model)")
        p_img = st.text_input("Descreva a imagem:")
        if st.button("🎨 Criar Imagem"):
            seed = random.randint(1, 99999)
            img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(p_img)}?width=1024&height=1024&nologo=true&seed={seed}&model=flux"
            st.image(img_url, use_container_width=True)

    # ABA 3: VÍDEOS (VERSÃO CADEADO)
    with t3:
        st.subheader("🎥 Gerador de Vídeo IA")
        p_vid = st.text_input("Descreva a cena (ex: Golden dragon flying, 4k):", key="v_input_final")
        
        if st.button("🎬 Gerar Vídeo"):
            with st.spinner("IA Processando... (Isso pode levar 30 segundos)"):
                v_seed = random.randint(1, 9999)
                v_url = f"https://pollinations.ai/p/{urllib.parse.quote(p_vid)}?width=1280&height=720&model=video&seed={v_seed}"
                
                # Criamos um botão de download por cima para o usuário não se perder
                st.markdown(f"""
                    <div style="background: #1a1a1a; padding: 20px; border-radius: 15px; border: 1px solid #333; text-align: center;">
                        <h4 style="color: #fff; margin-bottom: 15px;">Seu vídeo está sendo processado!</h4>
                        <p style="font-size: 0.9em; color: #888;">Se a visualização abaixo falhar ou redirecionar, use o botão abaixo:</p>
                        <a href="{v_url}" target="_blank" style="text-decoration: none;">
                            <button style="background: #6366f1; color: white; border: none; padding: 10px 20px; border-radius: 8px; cursor: pointer; font-weight: bold;">
                                📥 Baixar / Ver Vídeo em Nova Aba
                            </button>
                        </a>
                    </div>
                """, unsafe_allow_html=True)
                
                # Tentativa de embed com proteção máxima contra clique/redirecionamento
                st.components.v1.html(f"""
                    <div style="pointer-events: none; border-radius:15px; overflow:hidden; border:2px solid #6366f1; margin-top: 20px;">
                        <iframe src="{v_url}" width="100%" height="450" frameborder="0" style="pointer-events: auto;"></iframe>
                    </div>
                """, height=500)
