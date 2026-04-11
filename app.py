import streamlit as st
from groq import Groq
import re
from youtube_transcript_api import YouTubeTranscriptApi

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="VIDIOM AI | GROQ SPEED", layout="wide")

# Estética Dark
st.markdown("<style>.stApp { background: #050505; color: #fff; }</style>", unsafe_allow_html=True)

# --- INICIALIZAÇÃO DA GROQ ---
def setup_groq():
    if "GROQ_API_KEY" not in st.secrets:
        st.error("Configure GROQ_API_KEY nas Secrets do Streamlit!")
        return None
    return Groq(api_key=st.secrets["GROQ_API_KEY"])

client = setup_groq()

def extrair_id(url):
    pattern = r'(?:v=|\/)([a-zA-Z0-9_-]{11})'
    match = re.search(pattern, url)
    return match.group(1) if match else None

# --- UI ---
st.title("⚡ VIDIOM AI - Edição Ultra-Rápida")
st.markdown("### Powered by Groq (Llama 3)")

url_input = st.text_input("Cole o link do YouTube aqui:")

if st.button("🚀 GERAR ROTEIRO DE CORTE"):
    if url_input and client:
        with st.spinner("Processando em alta velocidade..."):
            v_id = extrair_id(url_input)
            transcricao = ""
            
            if v_id:
                try:
                    data = YouTubeTranscriptApi.get_transcript(v_id, languages=['pt', 'en'])
                    transcricao = " ".join([t['text'] for t in data])
                except:
                    transcricao = "Sem legendas. Analise o link diretamente."

            # PROMPT PARA LLAMA 3
            prompt = f"Aja como um editor viral. Crie um roteiro de corte (gancho, tempo e legendas) para este vídeo: {url_input}. Contexto: {transcricao[:4000]}"
            
            try:
                # Chamada da API Groq (Llama 3 é excelente para isso)
                chat_completion = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama3-8b-8192",
                )
                st.session_state.resultado = chat_completion.choices[0].message.content
            except Exception as e:
                st.error(f"Erro na Groq: {e}")

if "resultado" in st.session_state:
    st.markdown("---")
    st.subheader("🎬 Plano de Viralização:")
    st.info(st.session_state.resultado)
