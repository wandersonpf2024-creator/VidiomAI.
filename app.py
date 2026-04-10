import streamlit as st
import urllib.parse
import random
import re
from supabase import create_client, Client
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

# --- 1. CONFIGURAÇÃO DE ESTILO ---
st.set_page_config(page_title="Vidiom AI | Premium Studio", layout="wide", page_icon="🎬")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #e0e0e0; }
    [data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 1px solid #1a1a1a; }
    h1, h2, h3 { font-family: 'Inter', sans-serif; background: -webkit-linear-gradient(#fff, #888); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .stButton>button { width: 100%; background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%); color: white; border: none; padding: 12px; border-radius: 12px; font-weight: 600; }
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
    st.error("Verifique as Secrets no Streamlit Cloud.")

# --- 3. FUNÇÕES ---
def get_video_id(url):
    pattern = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
    match = re.search(pattern, url)
    return match.group(1) if match else None

def sync_user(email_user):
    try:
        res = supabase.table("profiles").select("*").eq("email", email_user).execute()
        if len(res.data) > 0: return res.data[0]
        else:
            new_user = {"email": email_user, "credits": 100}
            data = supabase.table("profiles").insert(new_user).execute()
            return data.data[0]
    except: return {"email": email_user, "credits": 100}

# --- 4. INTERFACE ---
with st.sidebar:
    st.markdown("### 🛰️ VIDIOM AI")
    email = st.text_input("E-mail de acesso", placeholder="seu@email.com")
    if email:
        user_data = sync_user(email)
        st.success(f"⚡ {user_data['credits']} Créditos")

st.title("Estúdio de Criação Viral")

if not email:
    st.warning("⚠️ Digite seu e-mail para começar.")
else:
    tab1, tab2, tab3, tab4 = st.tabs(["✍️ Roteiro", "🖼️ Imagem", "🎥 Vídeo", "📺 YouTube Shorts"])

    with tab1:
        st.subheader("Script Creator")
        tema = st.text_area("Tema do vídeo:")
        if st.button("🚀 Criar"):
            model = genai.GenerativeModel('gemini-1.5-flash')
            res = model.generate_content(f"Roteiro viral: {tema}")
            st.write(res.text)

    with tab2:
        st.subheader("Imagem Flux Pro")
        img_p = st.text_input("Descrição da imagem:")
        if st.button("✨ Gerar"):
            url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(img_p)}?width=1024&height=1024&nologo=true&seed={random.randint(1,999)}&model=flux"
            st.image(url)

    with tab3:
        st.subheader("Vídeo IA")
        vid_p = st.text_input("O que acontece no vídeo?")
        if st.button("🎬 Animar"):
            v_url = f"https://pollinations.ai/p/{urllib.parse.quote(vid_p)}?width=1280&height=720&model=video&seed={random.randint(1,99)}"
            st.components.v1.html(f'<iframe src="{v_url}" width="100%" height="450" style="border:2px solid #6366f1; border-radius:15px;"></iframe>', height=500)

    with tab4:
        # --- BLOCO DA ABA 4 ATUALIZADO ---
        st.subheader("📺 YouTube para Shorts (Pro)")
        url_yt = st.text_input("Link do YouTube:", key="yt_tab4")
        if st.button("🧬 Analisar Vídeo"):
            v_id = get_video_id(url_yt)
            if v_id:
                with st.spinner("Analisando transcrição e criando cortes..."):
                    try:
                        transcript_text = ""
                        try:
                            t_list = YouTubeTranscriptApi.list_transcripts(v_id)
                            try:
                                t = t_list.find_transcript(['pt', 'en']).fetch()
                            except:
                                t = t_list.find_generated_transcripts().fetch()
                            transcript_text = " ".join([i['text'] for i in t])
                        except: transcript_text = ""

                        model = genai.GenerativeModel('gemini-1.5-flash')
                        if transcript_text:
                            prompt = f"Baseado no texto: {transcript_text[:5000]}. Crie 2 roteiros de cortes com títulos, hooks e legendas de destaque."
                        else:
                            prompt = f"O vídeo {url_yt} está sem legendas. Crie ideias de cortes baseadas no tema provável."
                        
                        res = model.generate_content(prompt)
                        st.markdown("---")
                        st.markdown(res.text)
                    except: st.error("Erro ao processar este vídeo.")
