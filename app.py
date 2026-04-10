import streamlit as st
import urllib.parse
import random
from supabase import create_client, Client
import google.generativeai as genai

# --- 1. CONFIGURAÇÃO DE ESTILO "MINDVIDEO" ---
st.set_page_config(page_title="Vidiom AI | Premium Studio", layout="wide", page_icon="🎬")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #e0e0e0; }
    [data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 1px solid #1a1a1a; }
    h1, h2, h3 { font-family: 'Inter', sans-serif; background: -webkit-linear-gradient(#fff, #888); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: -1px; }
    .stButton>button { width: 100%; background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%); color: white; border: none; padding: 12px; border-radius: 12px; font-weight: 600; transition: all 0.3s ease; }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 10px 20px rgba(99, 102, 241, 0.3); }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea { background-color: #0f0f0f !important; border: 1px solid #1a1a1a !important; color: white !important; border-radius: 12px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CONEXÕES ---
try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
    GEMINI_KEY = st.secrets["GEMINI_API_KEY"]
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    genai.configure(api_key=GEMINI_KEY)
except:
    st.error("Erro de conexão. Verifique as chaves.")

def sync_user(email_user):
    try:
        res = supabase.table("profiles").select("*").eq("email", email_user).execute()
        if len(res.data) > 0: return res.data[0]
        else:
            new_user = {"email": email_user, "credits": 100}
            data = supabase.table("profiles").insert(new_user).execute()
            return data.data[0]
    except: return {"email": email_user, "credits": "100 (Free)"}

# --- 3. SIDEBAR ---
with st.sidebar:
    st.markdown("### 🛰️ VIDIOM AI")
    email = st.text_input("Acesse sua conta", placeholder="seu@email.com")
    if email:
        user_data = sync_user(email)
        st.success(f"⚡ {user_data['credits']} Créditos")

# --- 4. ÁREA DE TRABALHO ---
st.title("Estúdio de Produção Premium")

if not email:
    st.warning("⚠️ Digite seu e-mail na barra lateral para começar.")
else:
    tab1, tab2, tab3 = st.tabs(["✍️ Roteiro Viral", "🖼️ Imagem Ultra", "🎥 Vídeo Mágico"])

    with tab1:
        st.markdown("### 📝 Criar Roteiro")
        tema = st.text_area("Sobre o que será o vídeo?")
        if st.button("🚀 Gerar Roteiro"):
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(f"Roteiro viral sobre: {tema}")
            st.write(response.text)

    with tab2:
        st.markdown("### 🎨 Visual Premium")
        img_desc = st.text_input("Descreva a imagem (Inglês):")
        if st.button("✨ Criar Imagem"):
            seed = random.randint(1, 999999)
            url_img = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(img_desc)}?width=1024&height=1024&nologo=true&seed={seed}&model=flux"
            st.image(url_img, use_container_width=True)

    with tab3:
        st.markdown("### 🎥 Gerador de Vídeo IA")
        video_desc = st.text_input("Descreva o movimento do vídeo (ex: 'A futuristic car driving through a neon city at night'):")
        
        if st.button("🎬 Gerar Vídeo"):
            if video_desc:
                with st.spinner("A gerar o seu vídeo... Isso pode demorar até 30 segundos."):
                    # O motor de vídeo funciona via Pollinations
                    seed_v = random.randint(1, 999999)
                    # Criamos a URL para o vídeo (utilizando o modelo de vídeo)
                    video_url = f"https://pollinations.ai/p/{urllib.parse.quote(video_desc)}?width=1280&height=720&model=video&seed={seed_v}"
                    
                    st.markdown("---")
                    # Exibe o vídeo usando um player de HTML5
                    st.video(video_url)
                    st.markdown(f"📥 [Descarregar Vídeo]({video_url})")
            else:
                st.error("Descreva o vídeo antes de gerar.")
