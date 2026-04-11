import streamlit as st
import google.generativeai as genai
import re
from youtube_transcript_api import YouTubeTranscriptApi

# --- 1. SETUP IA (NOME CORRIGIDO) ---
def setup_engine():
    try:
        if "GEMINI_API_KEY" in st.secrets:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            # NOME OFICIAL ESTÁVEL: gemini-1.5-flash
            return genai.GenerativeModel("gemini-1.5-flash")
    except Exception as e:
        st.error(f"Erro de Configuração: {e}")
        return None
    return None

model = setup_engine()

# --- 2. EXTRAÇÃO DE ID ---
def extrair_id(url):
    # Aceita links normais, shorts e youtu.be
    pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(pattern, url)
    return match.group(1) if match else None

# --- INTERFACE ---
st.set_page_config(page_title="VIDIOM AI", layout="wide")
st.title("🚀 VIDIOM AI – Viral Video Engine")

col1, col2 = st.columns(2)

with col1:
    url_input = st.text_input("Cole o link do YouTube:")
    estilo = st.selectbox("Estilo:", ["Hormozi", "Minimalista", "Podcast"])
    
    if st.button("🚀 Gerar Roteiro Viral"):
        if model and url_input:
            with st.status("Processando...", expanded=True) as status:
                v_id = extrair_id(url_input)
                texto_base = ""
                
                if v_id:
                    try:
                        st.write("Buscando legendas...")
                        # Tenta pegar em PT ou EN
                        transcript_list = YouTubeTranscriptApi.get_transcript(v_id, languages=['pt', 'en'])
                        texto_base = " ".join([t['text'] for t in transcript_list])
                    except:
                        st.write("⚠️ Legendas oficiais não encontradas. Usando análise por contexto.")
                
                # O PROMPT REAL (Aqui estava o erro do 'Hello')
                prompt_real = f"""
                Analise este conteúdo: {url_input}
                Transcrição: {texto_base[:3000]}
                Crie um roteiro de corte viral estilo {estilo}. 
                Indique o Gancho (Hook) e as frases da legenda.
                """
                
                try:
                    # CHAMADA CORRETA
                    st.write("IA Gerando Roteiro...")
                    response = model.generate_content(prompt_real)
                    st.session_state.resultado = response.text
                    status.update(label="Concluído!", state="complete")
                except Exception as e:
                    st.error(f"Erro na IA: {e}")
        else:
            st.error("Verifique a URL ou sua API Key nas Secrets.")

with col2:
    if "resultado" in st.session_state:
        st.subheader("🎬 Resultado do Corte")
        st.markdown(f"```\n{st.session_state.resultado}\n```")
