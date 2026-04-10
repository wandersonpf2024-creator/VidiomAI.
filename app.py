import streamlit as st
import urllib.parse
import random
import re
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

# --- 1. CONFIGURAÇÃO VISUAL ---
st.set_page_config(page_title="Vidiom AI | Premium", layout="wide", page_icon="🎬")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #e0e0e0; }
    .stButton>button { width: 100%; background: linear-gradient(135deg, #6366f1, #a855f7); color: white; border: none; padding: 12px; border-radius: 12px; font-weight: bold; }
    .stTextInput>div>div>input { background-color: #0f0f0f !important; border: 1px solid #333 !important; color: white !important; }
    .video-container { position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; background: #000; border-radius: 15px; border: 2px solid #6366f1; }
    .video-container iframe { position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CONFIGURAÇÃO IA ---
def setup_ia():
    try:
        if "GEMINI_API_KEY" in st.secrets:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            return genai.GenerativeModel('gemini-1.5-flash')
    except: return None
    return None

model = setup_ia()

# --- 3. INTERFACE ---
st.title("🛰️ VIDIOM AI - Estúdio Digital")

with st.sidebar:
    st.header("Acesso")
    email = st.text_input("E-mail para créditos")

if not email:
    st.info("Insira o seu e-mail para ativar as ferramentas.")
else:
    t1, t2, t3 = st.tabs(["✂️ Cortes", "🎨 Imagens", "🎥 Vídeos"])

    with t1:
        st.subheader("Roteirista de Cortes")
        link = st.text_input("Link do vídeo (YouTube/TikTok/etc):")
        if st.button("Gerar Estratégia de Corte"):
            if model:
                with st.spinner("IA a analisar..."):
                    res = model.generate_content(f"Crie um roteiro de corte viral para: {link}")
                    st.write(res.text)

    with t2:
        st.subheader("Gerador de Imagem")
        prompt_i = st.text_input("O que deseja criar?")
        if st.button("Gerar Imagem"):
            seed = random.randint(0, 99999)
            img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt_i)}?seed={seed}&model=flux&width=1024&height=1024&nologo=true"
            st.image(img_url)

    with t3:
        st.subheader("Gerador de Vídeo IA")
        prompt_v = st.text_input("Descreva a animação (ex: Fire burning in slow motion)")
        
        if st.button("Gerar Vídeo"):
            with st.spinner("A processar vídeo..."):
                v_seed = random.randint(0, 9999)
                # Usamos um link que foca apenas no resultado do vídeo
                v_url = f"https://pollinations.ai/p/{urllib.parse.quote(prompt_v)}?width=1280&height=720&model=video&seed={v_seed}"
                
                # Exibimos o link direto e tentamos o carregamento via HTML seguro
                st.markdown(f"✅ **Vídeo Gerado!** [Clique aqui para ver em ecrã inteiro se não carregar abaixo]({v_url})")
                
                # Técnica de Embed melhorada
                html_code = f"""
                <div class="video-container">
                    <iframe 
                        src="{v_url}" 
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                        allowfullscreen>
                    </iframe>
                </div>
                """
                st.components.v1.html(html_code, height=500)

st.markdown("---")
st.caption("Vidiom AI v2.1")
