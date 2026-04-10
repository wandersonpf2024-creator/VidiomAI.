import streamlit as st
import urllib.parse
import random
import re
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

# --- 1. CONFIGURAÇÃO VISUAL ---
st.set_page_config(page_title="Vidiom AI | Pro Studio", layout="wide", page_icon="🎬")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #e0e0e0; }
    h1, h2, h3 { font-family: 'Inter', sans-serif; background: -webkit-linear-gradient(#fff, #888); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; }
    .stButton>button { width: 100%; background: linear-gradient(135deg, #6366f1, #a855f7); color: white; border: none; padding: 12px; border-radius: 12px; font-weight: bold; }
    .stTextInput>div>div>input { background-color: #0f0f0f !important; border: 1px solid #333 !important; color: white !important; border-radius: 10px !important; }
    .card { background: #0a0a0a; border: 1px solid #1a1a1a; padding: 20px; border-radius: 15px; border-left: 5px solid #6366f1; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CONEXÃO COM A IA ---
def carregar_modelo():
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        # Usamos o 1.5-flash que é o mais rápido e estável para apps web
        return genai.GenerativeModel('gemini-1.5-flash')
    except:
        st.error("⚠️ Erro: Verifique se 'GEMINI_API_KEY' está correta nas Secrets do Streamlit.")
        return None

model = carregar_modelo()

def get_video_id(url):
    pattern = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
    match = re.search(pattern, url)
    return match.group(1) if match else None

# --- 3. INTERFACE ---
st.title("🛰️ VIDIOM AI - Estúdio Viral")

with st.sidebar:
    st.markdown("### 🔑 Acesso")
    email = st.text_input("Seu e-mail")
    if email:
        st.success("Conectado: 100 Créditos")

if not email:
    st.info("Digite seu e-mail para liberar as ferramentas.")
else:
    tab1, tab2, tab3 = st.tabs(["✂️ Cortes por Link", "🎨 Imagens por Prompt", "🎥 Vídeos por Prompt"])

    # --- ABA 1: CORTES ---
    with tab1:
        st.subheader("Extrair Cortes de Links")
        link_input = st.text_input("Cole o link (YouTube, TikTok, Instagram, etc):")
        
        if st.button("🧬 Analisar e Criar Roteiro"):
            if not model:
                st.error("IA não configurada.")
            else:
                with st.spinner("Analisando..."):
                    vid_id = get_video_id(link_input)
                    transcricao = ""
                    
                    # Se for YouTube, tenta pegar a fala
                    if vid_id:
                        try:
                            t = YouTubeTranscriptApi.get_transcript(vid_id, languages=['pt', 'en'])
                            transcricao = " ".join([i['text'] for i in t])
                        except: transcricao = ""

                    # IA faz o trabalho de roteiro e legendas
                    prompt = (
                        f"Analise o vídeo do link: {link_input}. "
                        f"Texto extraído: {transcricao[:3000] if transcricao else 'Use o tema do link'}. "
                        "Crie 2 roteiros de cortes virais (TikTok/Reels). "
                        "Diga o Título, o Gancho (Hook) e quais partes da LEGENDA devem ser coloridas."
                    )
                    
                    try:
                        res = model.generate_content(prompt)
                        st.markdown("---")
                        st.markdown(f'<div class="card">{res.text}</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Erro na conexão com a IA: {e}")

    # --- ABA 2: IMAGENS ---
    with tab2:
        st.subheader("Gerar Imagem com IA (Flux)")
        prompt_img = st.text_input("O que você quer criar?")
        if st.button("🎨 Gerar Arte"):
            with st.spinner("Desenhando..."):
                seed = random.randint(1, 100000)
                url_final = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt_img)}?width=1024&height=1024&nologo=true&seed={seed}&model=flux"
                st.image(url_final)

    # --- ABA 3: VÍDEO POR PROMPT (VERSÃO FIXA) ---
    with tab3:
        st.subheader("🎥 Gerador de Clipes Animados")
        prompt_vid = st.text_input("Descreva a cena animada:", key="vid_prompt_novo")
        
        if st.button("🎬 Animar Cena"):
            with st.spinner("Renderizando vídeo..."):
                v_seed = random.randint(1, 9999)
                safe_vid_prompt = urllib.parse.quote(prompt_vid)
                # Link direto para o player
                v_url = f"https://pollinations.ai/p/{safe_vid_prompt}?width=1280&height=720&model=video&seed={v_seed}"
                
                # O segredo está no 'sandbox' e no estilo para não redirecionar
                st.components.v1.html(f"""
                    <div style="width:100%; height:450px; overflow:hidden; border-radius:15px; border:2px solid #6366f1;">
                        <iframe 
                            src="{v_url}" 
                            width="100%" 
                            height="100%" 
                            style="border:none;" 
                            sandbox="allow-scripts allow-same-origin"
                            allowfullscreen>
                        </iframe>
                    </div>
                """, height=500)
                st.info("Aguarde cerca de 20 segundos. Se o site tentar 'fugir', o navegador vai bloqueá-lo e manter o vídeo aqui.")
