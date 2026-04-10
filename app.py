import streamlit as st
from supabase import create_client, Client
import google.generativeai as genai
import urllib.parse

# --- 1. CONFIGURAÇÕES DE CONEXÃO (COLE SUAS CHAVES AQUI) ---
SUPABASE_URL = "https://rnqgodykpbtgyvkxfnjz.supabase.co"
SUPABASE_KEY = "SUA_CHAVE_ANON_AQUI"
GEMINI_KEY = "SUA_CHAVE_GEMINI_AQUI"

# Inicializando APIs
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
genai.configure(api_key=GEMINI_KEY)

# --- 2. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Vidiom AI | Global Content", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: white; }
    .stButton>button { background: linear-gradient(90deg, #1f6feb, #09b3af); color: white; border-radius: 8px; border: none; }
    .sidebar .sidebar-content { background-color: #161b22; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LÓGICA DE CRÉDITOS ---
def sync_user(email):
    # Tenta buscar o usuário, se não existir, cria
    res = supabase.table("profiles").select("*").eq("email", email).execute()
    if not res.data:
        data = supabase.table("profiles").insert({"email": email, "credits": 100}).execute()
        return data.data[0]
    return res.data[0]

def deduct_credits(email, amount):
    res = supabase.table("profiles").select("credits").eq("email", email).execute()
    current = res.data[0]['credits']
    if current >= amount:
        supabase.table("profiles").update({"credits": current - amount}).eq("email", email).execute()
        return True
    return False

# --- 4. INTERFACE ---
with st.sidebar:
    st.title("🛰️ Vidiom AI")
    email = st.text_input("Login with Email", placeholder="user@example.com")
    
    if email:
        user = sync_user(email)
        st.subheader(f"Credits: ⚡ {user['credits']}")
        
        st.write("---")
        st.write("💎 **Upgrade Plans**")
        st.link_button("PRO Plan ($49)", "SEU_LINK_STRIPE_49")
        st.link_button("ELITE Plan ($97)", "SEU_LINK_STRIPE_97")

st.title("International Content Studio")

if not email:
    st.warning("Please enter your email on the sidebar to start.")
else:
    tab1, tab2, tab3 = st.tabs(["✍️ Copywriter", "🎨 AI Image", "🎬 Video Captions"])

    with tab1:
        topic = st.text_input("What is the topic of the viral post?")
        if st.button("Generate Script (2 Credits)"):
            if deduct_credits(email, 2):
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content(f"Write a viral Instagram caption about: {topic}")
                st.write(response.text)
                st.rerun()
            else: st.error("Insufficient credits.")

    with tab2:
        img_topic = st.text_input("Describe the image you want")
        if st.button("Generate Image (5 Credits)"):
            if deduct_credits(email, 5):
                encoded = urllib.parse.quote(img_topic)
                url = f"https://image.pollinations.ai/prompt/{encoded}?width=1080&height=1080&nologo=true"
                st.image(url)
                st.rerun()
            else: st.error("Insufficient credits.")

    with tab3:
        st.info("Video translation & captions module ready for upload.")
        # Lógica de vídeo ficaria aqui