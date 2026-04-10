import streamlit as st
import urllib.parse
import random
import re
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

# --- 1. CONFIGURAÇÃO VISUAL PREMIUM ---
st.set_page_config(page_title="Vidiom AI | Premium Studio", layout="wide", page_icon="🎬")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #e0e0e0; }
    [data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 1px solid #1a1a1a; }
    h1, h2, h3 { font-family: 'Inter', sans-serif; background: -webkit-linear-gradient(#fff, #888); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .stButton>button { width: 100%; background: linear-gradient(135deg, #6366f1, #a855f7); color: white; border: none; padding: 12px; border-radius: 12px; font-weight: bold; }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea { background-color: #0f0f0f !important; border: 1px solid #222 !important; color: white !important; border-radius: 10px !important; }
    .card { background: #0a0a0a; border: 1px solid #1a1a1a; padding: 20px; border-radius: 15px; border-left: 5px solid #6366f1; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CONFIGURAÇÕES IA ---
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    else:
        st.error("Configure sua GEMINI_API_KEY nas Secrets do Streamlit.")
except Exception as e:
    st.error(f"Erro de configuração: {e}")

def get_video_id(url):
    pattern = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
    match = re.search(pattern, url)
    return match.group(1) if match else None

# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("🛰️ VIDIOM AI")
    email = st.text_input("Acesse sua conta", placeholder="seu@email.com")
    if email:
        st.success("⚡ 100 Créditos Disponíveis")

# --- 4. INTERFACE PRINCIPAL ---
st.title("Estúdio de Produção Viral")

if not email:
    st.warning("👋 Por favor, digite seu e-mail na barra lateral para liberar as ferramentas.")
else:
    tab1, tab2, tab3 = st.tabs(["✂️ Cortes por Link", "🎨 Imagem por Prompt", "🎥 Vídeo por Prompt"])

    # --- ABA 1: CORTES POR LINK ---
    with tab1:
        st.subheader("🧬 Viral Slicer (YouTube -> Redes Sociais)")
        st.write("Extraia os melhores momentos e ganhe um guia de legendas.")
        url_yt = st.text_input("Cole o link do vídeo do YouTube aqui:", key="yt_link")
        
        if st.button("🧬 Analisar e Criar Roteiro de Cortes"):
            vid_id = get_video_id(url_yt)
            with st.spinner("Analisando vídeo..."):
                transcript_text = ""
                if vid_id:
                    try:
                        t_list = YouTubeTranscriptApi.list_transcripts(vid_id)
                        t = t_list.find_transcript(['pt', 'en']).fetch()
                        transcript_text = " ".join([i['text'] for i in t])
                    except:
                        transcript_text = None
                
                try:
                    # Usando gemini-1.5-flash ou gemini-pro (ajustado para evitar o erro NotFound)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    contexto = transcript_text[:5000] if transcript_text else "Conteúdo baseado no tema do vídeo."
                    prompt = (
                        f"Aja como um especialista em retenção de TikTok e Kwai. Vídeo: {url_yt}. Transcrição: {contexto}. "
                        "Crie 2 roteiros de cortes. Para cada corte entregue: \n"
                        "1. Título Curioso.\n"
                        "2. Gancho de Legenda (Hook) para os primeiros 2 segundos.\n"
                        "3. Roteiro detalhado com indicações de [LEGENDA EM DESTAQUE] para palavras importantes."
                    )
                    
                    res = model.generate_content(prompt)
                    st.markdown("---")
                    st.markdown(f'<div class="card">{res.text}</div>', unsafe_allow_html=True)
                except:
                    st.error("Erro ao conectar com a IA. Tente outro link ou verifique sua API Key.")

    # --- ABA 2: IMAGEM POR PROMPT ---
    with tab2:
        st.subheader("🎨 Gerador de Arte Estática")
        st.write("Crie thumbnails ou artes para seus vídeos via comando de voz/texto.")
        prompt_img = st.text_input("O que você deseja ver? (Ex: Um leão cyberpunk no espaço)", key="img_prompt")
        
        if st.button("✨ Gerar Imagem Agora"):
            with st.spinner("Desenhando sua ideia..."):
                seed = random.randint(1, 999999)
                safe_prompt = urllib.parse.quote(f"{prompt_img}, ultra realistic, high resolution, 8k")
                img_url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1024&height=1024&nologo=true&seed={seed}&model=flux"
                st.image(img_url, caption=f"Resultado para: {prompt_img}", use_container_width=True)

    # --- ABA 3: VÍDEO POR PROMPT ---
    with tab3:
        st.subheader("🎥 Gerador de Clipes Animados")
        st.write("Crie pequenos clipes de vídeo para usar nos seus cortes.")
        prompt_vid = st.text_input("Descreva a cena animada: (Ex: Chuva de moedas de ouro)", key="vid_prompt")
        
        if st.button("🎬 Animar Cena"):
            with st.spinner("Renderizando vídeo..."):
                v_seed = random.randint(1, 9999)
                safe_vid_prompt = urllib.parse.quote(prompt_vid)
                v_url = f"https://pollinations.ai/p/{safe_vid_prompt}?width=1280&height=720&model=video&seed={v_seed}"
                
                st.components.v1.html(f"""
                    <iframe src="{v_url}" width="100%" height="450" style="border:2px solid #6366f1; border-radius:15px;" allowfullscreen></iframe>
                """, height=500)
                st.info("Aguarde alguns segundos para o carregamento do player.")

st.markdown("---")
st.caption("Vidiom AI v2.0 - O Estúdio definitivo para criadores de conteúdo.")
