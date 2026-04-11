import streamlit as st
import google.generativeai as genai
import re
from youtube_transcript_api import YouTubeTranscriptApi

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="VIDIOM AI | Estúdio de Cortes", layout="wide")

st.markdown("""
<style>
    .stApp { background: #050505; color: #fff; }
    .stButton>button { background: linear-gradient(90deg, #6366f1, #a855f7); color: white; border-radius: 10px; font-weight: bold; height: 50px; }
    .result-box { background: #0f0f0f; border: 1px solid #333; padding: 25px; border-radius: 15px; color: #00ff88; font-family: 'Courier New', monospace; }
</style>
""", unsafe_allow_html=True)

# --- ENGINE ULTRA COMPATÍVEL ---
def setup_engine():
    try:
        if "GEMINI_API_KEY" in st.secrets:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            # TROCA CRUCIAL: 'gemini-pro' é o modelo com maior compatibilidade mundial
            return genai.GenerativeModel("gemini-pro")
    except Exception as e:
        st.error(f"Erro de Setup: {e}")
        return None
    return None

model = setup_engine()

def extrair_id(url):
    pattern = r'(?:v=|\/)([a-zA-Z0-9_-]{11})'
    match = re.search(pattern, url)
    return match.group(1) if match else None

# --- UI ---
st.title("🛰️ VIDIOM AI - Viral Engine")
st.markdown("### Acelerador de Cortes e Legendas")

col1, col2 = st.columns(2, gap="large")

with col1:
    st.subheader("⚙️ Configuração")
    url_input = st.text_input("Link do YouTube:", placeholder="Cole aqui o seu link...")
    estilo = st.selectbox("Estilo do Roteiro:", ["Hormozi (Dinâmico)", "Minimalista", "Podcast (Falas longas)"])
    
    if st.button("🚀 GERAR ESTRATÉGIA DE CORTE"):
        if not url_input:
            st.warning("Por favor, insira um link.")
        elif not model:
            st.error("API Key não detectada. Verifique as 'Secrets' no Streamlit.")
        else:
            with st.status("Processando inteligência...", expanded=True) as status:
                v_id = extrair_id(url_input)
                transcricao = ""
                
                if v_id:
                    try:
                        st.write("🔍 Extraindo áudio do vídeo...")
                        data = YouTubeTranscriptApi.get_transcript(v_id, languages=['pt', 'en'])
                        transcricao = " ".join([t['text'] for t in data])
                    except:
                        st.write("⚠️ Legenda oficial não encontrada. Analisando contexto...")

                # PROMPT DE ALTO NÍVEL
                prompt = f"""
                Você é um estrategista viral. Analise este vídeo: {url_input}
                Transcrição: {transcricao[:3500]}
                
                Crie um roteiro de corte para TikTok/Reels no estilo {estilo}.
                Entregue:
                1. O GANCHO (Frase de abertura impactante).
                2. TIMESTAMPS (Início e fim sugeridos).
                3. ROTEIRO DE LEGENDAS (Frases curtas com marcação de ênfase).
                """
                
                try:
                    st.write("🧠 IA gerando roteiro final...")
                    # Chamada direta
                    response = model.generate_content(prompt)
                    st.session_state.vidiom_final = response.text
                    status.update(label="Análise Finalizada!", state="complete")
                except Exception as e:
                    st.error(f"Erro Crítico: {e}")
                    st.info("O servidor da IA recusou a conexão. Tente mudar o modelo para 'gemini-1.0-pro' no código.")

with col2:
    st.subheader("🎬 Roteiro de Edição")
    if "vidiom_final" in st.session_state:
        st.markdown(f'<div class="result-box">{st.session_state.vidiom_final}</div>', unsafe_allow_html=True)
        st.download_button("📥 Baixar Script", st.session_state.vidiom_final, "roteiro_vidiom.txt")
    else:
        st.info("Aguardando o link e o processamento...")

st.markdown("---")
st.caption("Foco: Viralização e Retenção Estratégica.")
