import streamlit as st
import google.generativeai as genai
import re
from youtube_transcript_api import YouTubeTranscriptApi

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="VIDIOM AI | S-TIER", layout="wide")

# --- ENGINE COM FORÇA BRUTA ---
def call_gemini(prompt):
    try:
        # Pega a chave das secrets
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        
        # Tentamos o modelo mais estável hoje. 
        # Se este falhar, o problema é a sua API KEY ou o faturamento no Google AI Studio.
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Erro de Conexão: {str(e)}"

def extrair_id(url):
    pattern = r'(?:v=|\/)([a-zA-Z0-9_-]{11})'
    match = re.search(pattern, url)
    return match.group(1) if match else None

# --- UI MODERNA ---
st.title("🛰️ VIDIOM AI - Sistema Anti-Falhas")
st.markdown("---")

col1, col2 = st.columns(2, gap="large")

with col1:
    st.subheader("⚙️ Configuração do Corte")
    url_input = st.text_input("Link do YouTube:")
    estilo = st.selectbox("Estilo Visual:", ["Hormozi (Dinâmico)", "Minimalista", "Impacto"])
    
    if st.button("🚀 GERAR ESTRATÉGIA"):
        if not url_input:
            st.warning("Insira um link.")
        else:
            with st.status("Executando Protocolo de Análise...", expanded=True) as status:
                v_id = extrair_id(url_input)
                transcricao = ""
                
                if v_id:
                    try:
                        st.write("📥 Extraindo legendas...")
                        data = YouTubeTranscriptApi.get_transcript(v_id, languages=['pt', 'en'])
                        transcricao = " ".join([t['text'] for t in data])
                    except:
                        st.write("⚠️ Legenda não disponível. Analisando metadados...")

                # PROMPT TÉCNICO
                prompt = f"""
                Analise este vídeo: {url_input}
                Transcrição: {transcricao[:3000]}
                Crie um roteiro de corte viral estilo {estilo}.
                Indique: HOOK, TIMESTAMPS e LEGENDAS.
                """
                
                st.write("🧠 Consultando Cérebro da IA...")
                resultado = call_gemini(prompt)
                st.session_state.vidiom_final = resultado
                status.update(label="Processo Concluído!", state="complete")

with col2:
    st.subheader("🎬 Roteiro Final")
    if "vidiom_final" in st.session_state:
        st.markdown(f"```text\n{st.session_state.vidiom_final}\n```")
    else:
        st.info("O roteiro aparecerá aqui após o processamento.")
