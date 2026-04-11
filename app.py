import os
import subprocess
import sys

# --- FORÇAR ATUALIZAÇÃO DA BIBLIOTECA (HARD OVERRIDE) ---
try:
    import google.generativeai as genai
    # Verifica se a versão é antiga (menor que 0.7)
    from importlib.metadata import version
    if float(version('google-generativeai')[:3]) < 0.8:
        raise ImportError
except (ImportError, Exception):
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "google-generativeai"])
    import google.generativeai as genai

import streamlit as st
import re
from youtube_transcript_api import YouTubeTranscriptApi

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="VIDIOM AI | ULTIMATE", layout="wide")

def extrair_id(url):
    pattern = r'(?:v=|\/)([a-zA-Z0-9_-]{11})'
    match = re.search(pattern, url)
    return match.group(1) if match else None

# --- MOTOR RESILIENTE ---
def executar_ia(prompt):
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        
        # O modelo Flash é o mais moderno. Se a biblioteca estiver atualizada, ele VAI funcionar.
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Erro: {str(e)}"

# --- INTERFACE ---
st.title("🛰️ VIDIOM AI - Sistema Blindado")
st.markdown("---")

url = st.text_input("Link do YouTube:")

if st.button("GERAR CORTES"):
    if url:
        with st.status("Forçando conexão segura...", expanded=True) as status:
            v_id = extrair_id(url)
            transcricao = ""
            
            if v_id:
                try:
                    t = YouTubeTranscriptApi.get_transcript(v_id, languages=['pt', 'en'])
                    transcricao = " ".join([i['text'] for i in t])
                except: transcricao = "Sem legendas."

            res = executar_ia(f"Crie um roteiro de corte para: {url}. Texto: {transcricao[:2500]}")
            st.session_state.output = res
            status.update(label="Concluído!", state="complete")

if "output" in st.session_state:
    st.subheader("🎬 Roteiro")
    st.info(st.session_state.output)
