import streamlit as st
import google.generativeai as genai
import random
import urllib.parse
import re

# --- ESTÉTICA DE ELITE (CYBER-SaaS) ---
st.set_page_config(page_title="VIDIOM AI | FIRST TO MARKET", layout="wide", page_icon="💎")

st.markdown("""
    <style>
    .stApp { background: #020202; color: #ffffff; }
    .main-header { font-size: 3rem; font-weight: 800; letter-spacing: -2px; color: #fff; margin-bottom: 0; }
    .accent { color: #6366f1; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] { background: #111; border: 1px solid #222; border-radius: 8px 8px 0 0; padding: 10px 20px; }
    .stTabs [aria-selected="true"] { background: #6366f1 !important; border: 1px solid #6366f1 !important; }
    div[data-testid="stStatusWidget"] { background: #0a0a0a; border: 1px solid #222; }
    </style>
    """, unsafe_allow_html=True)

# --- BACKEND DE INTELIGÊNCIA ---
def setup_engine():
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        # Nível Máximo: Pro para lógica complexa
        return genai.GenerativeModel('gemini-1.5-pro')
    except:
        return None

engine = setup_engine()

# --- INTERFACE ---
st.markdown("<h1 class='main-header'>VIDIOM <span class='accent'>AI</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#666; margin-bottom:30px;'>ESTRATÉGIA DE RETENÇÃO E GERAÇÃO S-TIER</p>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🛠️ CONFIGURAÇÕES")
    token = st.text_input("CHAVE DE ACESSO", type="password")
    st.markdown("---")
    st.info("SISTEMA DE GERAÇÃO ULTRA-FAST ATIVO")

if not token:
    st.warning("🔐 Digite o Token para acessar o motor de elite.")
else:
    tab1, tab2, tab3 = st.tabs(["🧬 CORTES VIRAIS", "🖼️ IMAGENS PREMIUM", "🎬 VÍDEO CINEMÁTICO"])

    # ABA 1: O NOSSO DIFERENCIAL (A IDEIA QUE VAI VENCER)
    with tab1:
        st.markdown("### 🧪 ANÁLISE DE RETENÇÃO PSICOLÓGICA")
        target_link = st.text_input("LINK DO CONTEÚDO (Youtube/TikTok/Insta/Kwai)")
        
        if st.button("EXTRAIR ESTRATÉGIA"):
            if engine:
                with st.status("Executando Engenharia Reversa do Algoritmo...", expanded=True):
                    prompt = f"""
                    Aja como um Diretor de Viralização de alto nível. Analise: {target_link}.
                    Sua missão é criar 2 cortes que forcem o usuário a assistir até o fim.
                    Entrega:
                    1. GANCHO DE IMPACTO (O que falar nos primeiros 2 segundos).
                    2. ROTEIRO DE EDIÇÃO (Onde colocar B-roll, zoom e efeitos).
                    3. TEXTO DE LEGENDA DINÂMICA (Estilo Alex Hormozi).
                    Seja agressivo na persuasão.
                    """
                    response = engine.generate_content(prompt)
                    st.write(response.text)
            else:
                st.error("ERRO DE API: VERIFIQUE SUA CHAVE NO STREAMLIT.")

    # ABA 2: IMAGEM (FLUX ENGINE)
    with tab2:
        st.markdown("### 🎨 GERAÇÃO VISUAL")
        p_img = st.text_input("PROMPT PARA IMAGEM (ALTA FIDELIDADE)")
        if st.button("GERAR ARTE"):
            seed = random.randint(100, 99999)
            # Flux é o modelo que os profissionais usam agora
            img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(p_img)}?width=1024&height=1024&nologo=true&seed={seed}&model=flux"
            st.image(img_url, caption="RENDER FINALIZADO")

    # ABA 3: VÍDEO (REPLICATE-BASED)
    with tab3:
        st.markdown("### 🎥 GERAÇÃO DE MOVIMENTO")
        p_vid = st.text_input("PROMPT PARA VÍDEO (USE INGLÊS PARA MÁXIMA PERFORMANCE)")
        
        if st.button("RENDERIZAR VÍDEO"):
            with st.spinner("PROCESSANDO FRAMES..."):
                v_seed = random.randint(100, 9999)
                v_url = f"https://pollinations.ai/p/{urllib.parse.quote(p_vid)}?width=1280&height=720&model=video&seed={v_seed}"
                
                # PROTEÇÃO ANTI-REDIRECIONAMENTO: Player Nativo Streamlit
                st.markdown(f"**LINK DO RENDER:** [DOWNLOAD MP4]({v_url})")
                st.video(v_url) 

st.markdown("---")
st.markdown("<p style='text-align:center; color:#333;'>VIDIOM AI © 2026 - TECNOLOGIA EXCLUSIVA</p>", unsafe_allow_html=True)
