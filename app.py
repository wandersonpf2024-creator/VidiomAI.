import streamlit as st
import urllib.parse
import random
from supabase import create_client, Client
import google.generativeai as genai

# --- 1. CONFIGURAÇÃO DE ESTILO "MINDVIDEO" (UI/UX) ---
st.set_page_config(page_title="Vidiom AI | Premium Studio", layout="wide", page_icon="🎬")

st.markdown("""
    <style>
    /* Estilo Global - Dark Mode Profundo */
    .stApp { background-color: #050505; color: #e0e0e0; }
    
    /* Sidebar Minimalista */
    [data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 1px solid #1a1a1a; }
    
    /* Títulos Estilo Tech */
    h1, h2, h3 { 
        font-family: 'Inter', sans-serif; 
        background: -webkit-linear-gradient(#fff, #888);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -1px;
    }

    /* Botões Premium (Gradiente MindVideo) */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        color: white; border: none; padding: 12px;
        border-radius: 12px; font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(99, 102, 241, 0.3);
    }

    /* Inputs e Cards */
    .stTextInput>div>div>input {
        background-color: #0f0f0f !important;
        border: 1px solid #1a1a1a !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 15px !important;
    }
    
    .stTabs [data-baseweb="tab"] { color: #888; }
    .stTabs [data-baseweb="tab--active"] { color: #fff; border-bottom-color: #6366f1; }
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
    st.error("Erro de conexão. Verifique suas Secrets no Streamlit.")

# --- 3. LÓGICA DE CRÉDITOS ---
def sync_user(email_user):
    try:
        res = supabase.table("profiles").select("*").eq("email", email_user).execute()
        if len(res.data) > 0: return res.data[0]
        else:
            new_user = {"email": email_user, "credits": 100}
            data = supabase.table("profiles").insert(new_user).execute()
            return data.data[0]
    except: return {"email": email_user, "credits": "100 (Free)"}

# --- 4. INTERFACE PRINCIPAL ---
with st.sidebar:
    st.markdown("### 🛰️ VIDIOM AI")
    st.write("Studio de Criação Inteligente")
    st.markdown("---")
    email = st.text_input("Acesse sua conta", placeholder="seu@email.com")
    
    if email:
        user_data = sync_user(email)
        st.success(f"⚡ {user_data['credits']} Créditos")
        st.markdown("---")
        st.markdown("**Plano:** Professional")
        if st.button("💎 Upgrade para Unlimited"):
            st.info("Em breve: Integração com Stripe")

# --- ÁREA DE TRABALHO ---
st.title("Estúdio de Produção")
st.write("Selecione a ferramenta para iniciar sua criação viral.")

if not email:
    st.warning("⚠️ Digite seu e-mail na barra lateral para começar.")
else:
    tab1, tab2 = st.tabs(["🎥 Gerador de Script", "🖼️ Gerador de Imagem Ultra"])

    with tab1:
        st.markdown("### 📝 Criar Roteiro Viral")
        tema = st.text_area("Sobre o que será o seu conteúdo?", placeholder="Ex: Um vídeo curto sobre como a IA está mudando o mercado de trabalho em 2026...")
        if st.button("🚀 Gerar Roteiro"):
            with st.spinner("O Gemini está arquitetando seu roteiro..."):
                model = genai.GenerativeModel('gemini-pro')
                prompt = f"Crie um roteiro para TikTok/Reels ultra engajador sobre: {tema}. Use ganchos fortes nos primeiros 3 segundos."
                response = model.generate_content(prompt)
                st.markdown("---")
                st.markdown(response.text)

    with tab2:
        st.markdown("### 🎨 Criação de Visual Premium")
        img_desc = st.text_input("Descreva a cena (melhor em Inglês):", placeholder="Ex: Futuristic cinematic car, neon city background, 8k, hyper-realistic")
        
        if st.button("✨ Criar Obra de Arte"):
            if img_desc:
                with st.spinner("Gerando imagem com motor Flux..."):
                    # Adicionando palavras-chave de qualidade
                    premium_prompt = f"{img_desc}, 8k, cinematic, highly detailed, professional lighting, masterpiece"
                    encoded_prompt = urllib.parse.quote(premium_prompt)
                    seed = random.randint(1, 999999)
                    
                    # URL do motor FLUX (Mais potente que o anterior)
                    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true&seed={seed}&model=flux"
                    
                    # Layout de exibição
                    st.markdown("---")
                    st.image(url, use_container_width=True)
                    st.markdown(f"📥 [Clique aqui para baixar a imagem em alta resolução]({url})")
            else:
                st.error("Por favor, descreva o que você quer criar.")
