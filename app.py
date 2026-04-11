import streamlit as st
import google.generativeai as genai
import re
from youtube_transcript_api import YouTubeTranscriptApi

# --- SETUP ---
st.set_page_config(page_title="VIDIOM AI", layout="wide")

# Inicializa a IA de forma simples
def iniciar_ia():
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("ERRO: Configure a GEMINI_API_KEY nas Secrets do Streamlit!")
        return None
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    return genai.GenerativeModel('gemini-1.5-flash')

ia = iniciar_ia()

# Função para pegar o ID do vídeo
def pegar_id(url):
    regex = r"(?:v=|\/)([0-9A-Za-z_-]{11})"
    busca = re.search(regex, url)
    return busca.group(1) if busca else None

# --- INTERFACE ---
st.title("✂️ VIDIOM AI - GERADOR DE CORTES")

link = st.text_input("Cole o link do YouTube aqui:")

if st.button("CRIAR ROTEIRO DE CORTE"):
    if link and ia:
        with st.spinner("Analisando vídeo..."):
            video_id = pegar_id(link)
            texto_video = ""
            
            # Tenta pegar a legenda
            if video_id:
                try:
                    legenda = YouTubeTranscriptApi.get_transcript(video_id, languages=['pt', 'en'])
                    texto_video = " ".join([t['text'] for t in legenda])
                except:
                    texto_video = "Legenda não encontrada. Analise pelo contexto do título."

            # O Prompt que faz o trabalho duro
            prompt = f"""
            Aja como um editor de vídeos virais. 
            Analise este conteúdo: {texto_video[:3500]}
            
            1. Escolha o melhor momento para um corte de 60 segundos.
            2. Escreva um TÍTULO chamativo.
            3. Escreva o ROTEIRO das legendas dinâmicas.
            """
            
            try:
                resposta = ia.generate_content(prompt)
                st.session_state.resultado = resposta.text
                st.success("Roteiro gerado!")
            except Exception as e:
                st.error(f"Erro na IA: {e}")

# Exibe o resultado
if "resultado" in st.session_state:
    st.markdown("### 🎬 Seu Roteiro de Corte:")
    st.text_area("", st.session_state.resultado, height=400)
