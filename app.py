import streamlit as st
from groq import Groq
import re
from youtube_transcript_api import YouTubeTranscriptApi

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="VIDIOM AI | S-TIER", layout="wide")
st.markdown("<style>.stApp { background: #050505; color: #fff; }</style>", unsafe_allow_html=True)

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

url_input = st.text_input("Cole o link do YouTube aqui:")

if st.button("🚀 GERAR ROTEIRO DE CORTE"):
    if url_input and client:
        with st.spinner("IA de Elite Processando..."):
            v_id = extrair_id(url_input)
            transcricao = ""
            
            if v_id:
                try:
                    data = YouTubeTranscriptApi.get_transcript(v_id, languages=['pt', 'en'])
                    transcricao = " ".join([t['text'] for t in data])
                except:
                    transcricao = "Sem legendas. Analise pelo título/contexto."

            prompt = f"""
            Aja como um editor de vídeos virais de alto nível.
            Crie um plano de corte estratégico para este vídeo: {url_input}
            Contexto/Falas: {transcricao[:5000]}
            
            Entregue:
            1. O GANCHO (Hook) ideal para os primeiros 3 segundos.
            2. TEMPO SUGERIDO (Início e Fim do corte).
            3. ROTEIRO DE LEGENDAS DINÂMICAS.
            4. POR QUE ISSO VAI VIRALIZAR?
            """
            
            try:
                # MUDANÇA AQUI: Usando o modelo mais atualizado da Groq
                chat_completion = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama-3.3-70b-versatile",
                )
                st.session_state.resultado = chat_completion.choices[0].message.content
            except Exception as e:
                st.error(f"Erro na Groq: {e}")
                st.info("Dica: Verifique se o modelo 'llama-3.3-70b-versatile' está disponível no seu console Groq.")

if "resultado" in st.session_state:
    st.markdown("---")
    st.subheader("🎬 Plano de Viralização Gerado:")
    st.info(st.session_state.resultado)
