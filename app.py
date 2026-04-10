import streamlit as st
import urllib.parse
import random
import re
from supabase import create_client, Client
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

# --- 1. CONFIGURAÇÃO DE ESTILO "DARK PREMIUM" ---
st.set_page_config(page_title="Vidiom AI | Pro Studio", layout="wide", page_icon="🎬")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #e0e0e0; }
    [data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 1px solid #1a1a1a; }
    h1, h2, h3 { font-family: 'Inter', sans-serif; background: -webkit-linear-gradient(#fff, #bbb); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; }
    .stButton>button { width: 100%; background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%); color: white; border: none; padding: 15px; border-radius: 12px; font-weight: bold; transition: 0.3s; }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 8px 15px rgba(99, 102, 241, 0.4); }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea { background-color: #0f0f0f !important; border: 1px solid #222 !important; color: white !important; border-radius: 10px !important; }
    .stTabs [data-baseweb="tab"] { color: #777; font-size: 16px; }
    .stTabs [data-baseweb="tab--active"] { color: #fff; border-bottom: 2px solid #6366f1; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CONEXÕES ---
try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
    GEMINI_KEY = st.secrets["GEMINI_API_KEY"]
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    genai.configure(api_key=GEMINI_KEY)
except Exception as e:
    st.error("Erro nas Secrets. Verifique as chaves no painel do Streamlit.")

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
    st.title("🛰️ VIDIOM AI")
    email = st.text_input("Seu E-mail", placeholder="exemplo@email.com")
    if email:
        u = sync_user(email)
        st.success(f"⚡ {u['credits']} Créditos")
    st.markdown("---")
    st.write("Versão 2.0 - Premium")

st.title("Estúdio de Criação Viral")

if not email:
    st.info("👋 Digite seu e-mail para acessar o painel.")
else:
    tab1, tab2, tab3, tab4 = st.tabs(["✍️ Roteiros", "🖼️ Imagens", "🎥 Vídeos", "📺 YouTube para Shorts"])

    # TAB 1: ROTEIROS
    with tab1:
        st.subheader("Gerador de Scripts Virais")
        prompt_video = st.text_area("Sobre o que é o vídeo?")
        if st.button("🚀 Criar Roteiro"):
            model = genai.GenerativeModel('gemini-1.5-flash')
            res = model.generate_content(f"Crie um roteiro de 60s para Reels/TikTok sobre {prompt_video}. Inclua sugestões de legenda de tela.")
            st.markdown(res.text)

    # TAB 2: IMAGENS (FLUX MOTOR)
    with tab2:
        st.subheader("IA de Imagem Ultra-Realista")
        desc_img = st.text_input("O que a IA deve desenhar? (Em Inglês funciona melhor)")
        if st.button("🎨 Gerar Imagem"):
            with st.spinner("Desenhando..."):
                seed = random.randint(1, 100000)
                # Otimização automática de prompt
                full_p = urllib.parse.quote(f"{desc_img}, cinematic lighting, 8k, hyper-realistic, masterpiece")
                url = f"https://image.pollinations.ai/prompt/{full_p}?width=1024&height=1024&nologo=true&seed={seed}&model=flux"
                st.image(url)
                st.markdown(f"[📥 Baixar Imagem]({url})")

    # TAB 3: VÍDEOS
    with tab3:
        st.subheader("Gerador de Vídeo IA")
        desc_vid = st.text_input("Descreva o movimento do vídeo:")
        if st.button("🎬 Gerar Clipe"):
            with st.spinner("Animando..."):
                v_url = f"https://pollinations.ai/p/{urllib.parse.quote(desc_vid)}?width=1280&height=720&model=video&seed={random.randint(1,999)}"
                st.components.v1.html(f'<iframe src="{v_url}" width="100%" height="450" style="border:2px solid #6366f1; border-radius:15px;"></iframe>', height=500)

    # TAB 4: YOUTUBE PARA VIRAL (O SEU DIFERENCIAL)
    with tab4:
        st.subheader("Cortes Automáticos de YouTube")
        url_yt = st.text_input("Link do Vídeo do YouTube:")
        if st.button("🧬 Analisar Vídeo"):
            vid_id = get_video_id(url_yt)
            if vid_id:
                try:
                    with st.spinner("Capturando áudio e criando legendas..."):
                        # Tenta capturar qualquer legenda disponível
                        transcripts = YouTubeTranscriptApi.list_transcripts(vid_id)
                        try:
                            # Tenta português ou então a primeira disponível
                            t = transcripts.find_transcript(['pt', 'en']).fetch()
                        except:
                            t = transcripts.find_generated_transcripts().fetch()
                        
                        full_text = " ".join([i['text'] for i in t])
                        
                        # IA criando o corte e as legendas
                        model = genai.GenerativeModel('gemini-1.5-flash')
                        prompt_final = f"Baseado no texto: {full_text[:5000]}. Crie 2 roteiros de cortes de 30 segundos. Para cada um, defina: 1. Título impactante. 2. Legenda de abertura (Hook). 3. O texto exato que deve aparecer como legenda em destaque no centro da tela."
                        res = model.generate_content(prompt_final)
                        st.markdown("---")
                        st.markdown(res.text)
                except Exception:
                    st.error("Este vídeo não permite extração de áudio direta. Tente outro vídeo ou um link com legendas ativadas.")
            else:
                st.error("URL inválida.")
