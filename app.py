import streamlit as st
import google.generativeai as genai
import re
from youtube_transcript_api import YouTubeTranscriptApi

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="VIDIOM AI", layout="wide")

# --- CSS PROFISSIONAL ---
st.markdown("""
<style>
    .stApp { background: #080808; color: #fff; }
    .stButton>button { background: #6366f1; color: white; border-radius: 8px; width: 100%; }
    .result-box { background: #111; border: 1px solid #333; padding: 20px; border-radius: 10px; color: #00ff88; }
</style>
""", unsafe_allow_html=True)

# --- ENGINE COM NOME DE MODELO "HARD-CODED" ---
def setup_engine():
    try:
        if "GEMINI_API_KEY" in st.secrets:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            # Tentando o nome de sistema mais básico para evitar o erro 404
            return genai.GenerativeModel("gemini-1.5-flash")
    except Exception as e:
        st.error(f"Erro ao configurar IA: {e}")
        return None
    return None

model = setup_engine()

# --- FUNÇÃO DE EXTRAÇÃO ---
def extrair_id(url):
    pattern = r'(?:v=|\/)([a-zA-Z0-9_-]{11})'
    match = re.search(pattern, url)
    return match.group(1) if match else None

# --- UI ---
st.title("🚀 VIDIOM AI - Viral Engine")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Configuração")
    url_input = st.text_input("Link do YouTube:")
    estilo = st.selectbox("Estilo do Corte:", ["Hormozi", "Minimalista", "Podcast"])
    
    if st.button("Gerar Estratégia Viral"):
        if not url_input:
            st.warning("Insira um link.")
        elif not model:
            st.error("API Key não configurada corretamente.")
        else:
            with st.status("Processando...", expanded=True) as status:
                v_id = extrair_id(url_input)
                transcricao = ""
                
                if v_id:
                    try:
                        st.write("Extraindo legendas...")
                        data = YouTubeTranscriptApi.get_transcript(v_id, languages=['pt', 'en'])
                        transcricao = " ".join([t['text'] for t in data])
                    except:
                        st.write("⚠️ Legenda não disponível. Analisando via metadados.")

                # PROMPT REALMENTE ENVIADO
                prompt = f"""
                Analise o vídeo: {url_input}
                Transcrição: {transcricao[:3000]}
                Crie um roteiro de corte viral estilo {estilo}.
                Inclua: Gancho, Melhores momentos (timestamps) e sugestão de legenda.
                """
                
                try:
                    st.write("Solicitando análise à IA...")
                    # Chamada simplificada para evitar erros de versão
                    response = model.generate_content(prompt)
                    st.session_state.vidiom_res = response.text
                    status.update(label="Concluído!", state="complete")
                except Exception as e:
                    st.error(f"Erro na Geração: {e}")
                    st.info("Dica: Se o erro for 404, verifique se a biblioteca 'google-generativeai' no seu requirements.txt está na última versão.")

with col2:
    st.subheader("Resultado")
    if "vidiom_res" in st.session_state:
        st.markdown(f'<div class="result-box">{st.session_state.vidiom_res}</div>', unsafe_allow_html=True)
