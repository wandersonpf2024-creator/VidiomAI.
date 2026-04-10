import streamlit as st
from supabase import create_client, Client
import google.generativeai as genai
import urllib.parse

# --- 1. CONFIGURAÇÕES (PEGANDO DAS SECRETS) ---
try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
    GEMINI_KEY = st.secrets["GEMINI_API_KEY"]
    
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    genai.configure(api_key=GEMINI_KEY)
except Exception as e:
    st.error("Erro nas chaves (Secrets). Verifique o Advanced Settings do Streamlit.")

# --- 2. FUNÇÃO BLINDADA ---
def sync_user(email_user):
    try:
        # Tenta buscar
        res = supabase.table("profiles").select("*").eq("email", email_user).execute()
        if len(res.data) > 0:
            return res.data[0]
        else:
            # Tenta criar se não existir
            new_user = {"email": email_user, "credits": 100}
            data = supabase.table("profiles").insert(new_user).execute()
            return data.data[0]
    except Exception as e:
        # SE DER ERRO NO BANCO, ELE DEIXA USAR MESMO ASSIM (Modo Offline/Demo)
        return {"email": email_user, "credits": "Demo (DB Error)"}

# --- 3. INTERFACE ---
st.set_page_config(page_title="Vidiom AI", layout="wide")

with st.sidebar:
    st.title("🛰️ Vidiom AI")
    email = st.text_input("Seu E-mail")
    
    if email:
        user_data = sync_user(email)
        st.subheader(f"Créditos: ⚡ {user_data['credits']}")

st.title("Estúdio de Conteúdo Viral")

if not email:
    st.info("Digite seu e-mail na esquerda para começar.")
else:
    tab1, tab2 = st.tabs(["✍️ Criar Script", "🎨 Criar Imagem"])
    
    with tab1:
        tema = st.text_input("Sobre o que é o seu vídeo?")
        if st.button("Gerar Roteiro"):
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(f"Crie um roteiro viral para TikTok sobre: {tema}")
            st.write(response.text)

    with tab2:
        img_desc = st.text_input("Descreva a imagem")
        if st.button("Gerar Imagem"):
            url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(img_desc)}?width=1080&height=1080&nologo=true"
            st.image(url)
