import streamlit as st
import os
from datetime import date

# --- CONFIGURAÇÃO VISUAL (ESTILO MONITOR PRO) ---
st.set_page_config(page_title="VIDIOM AI | Subtitles", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #080808; color: #ffffff; }
    header, [data-testid="stHeader"] { display: none !important; }
    .stMainBlockContainer { padding: 0px !important; }

    /* CABEÇALHO SUPERIOR */
    .top-bar {
        background-color: #000000;
        border-bottom: 1px solid #1f1f1f;
        padding: 10px 40px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        height: 65px;
        position: fixed; width: 100%; top: 0; z-index: 999;
    }

    .limit-badge {
        background-color: #1a1a1b;
        padding: 5px 15px;
        border-radius: 20px;
        border: 1px solid #333;
        font-size: 12px;
    }

    /* PAINÉIS */
    .panel {
        background-color: #0f0f10; border: 1px solid #1f1f1f;
        border-radius: 12px; padding: 20px; height: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# --- CONTROLE DE LIMITE (SIMPLES) ---
if 'videos_hoje' not in st.session_state:
    st.session_state.videos_hoje = 0

def incrementar_uso():
    st.session_state.videos_hoje += 1

# --- CABEÇALHO ---
st.markdown(f"""
    <div class="top-bar">
        <div style="display: flex; align-items: center; gap: 15px;">
            <span style="font-weight: 900; font-size: 22px;">🎞️ VIDIOM.AI</span>
        </div>
        <div style="display: flex; gap: 20px; align-items: center;">
            <div class="limit-badge">Grátis: {st.session_state.videos_hoje}/3 vídeos hoje</div>
            <div style="background-color: white; color: black; padding: 6px 15px; border-radius: 5px; font-weight: bold; font-size: 12px;">UPGRADE</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- INTERFACE PRINCIPAL ---
st.write("##") # Espaço para o header
st.write("##")

if st.session_state.videos_hoje >= 3:
    st.error("🚀 Você atingiu o limite de 3 vídeos diários! Faça o Upgrade para legendas ilimitadas.")
else:
    col1, col2 = st.columns([1.2, 2])

    with col1:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.subheader("1. Subir Vídeo")
        video_file = st.file_uploader("Arraste seu vídeo aqui", type=["mp4", "mov"], label_visibility="collapsed")
        
        if video_file:
            st.write("---")
            st.subheader("2. Escolha o Estilo")
            estilo = st.radio("Estilos de Legenda:", 
                             ["Viral Yellow (Hormozi)", "Minimalist White", "Bold Impact", "Netflix Style"])
            
            idioma = st.selectbox("Idioma do Vídeo:", ["Português", "Inglês", "Espanhol"])
            
            if st.button("GERAR LEGENDAS AGORA", type="primary", use_container_width=True):
                with st.status("IA analisando áudio..."):
                    # Aqui entraria a integração com Whisper ou AssemblyAI
                    import time
                    time.sleep(3)
                    st.success("Legendas Geradas!")
                    incrementar_uso()
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.subheader("Preview Profissional")
        if video_file:
            st.video(video_file)
            st.info(f"Legenda selecionada: {estilo}")
        else:
            st.image("https://via.placeholder.com/800x450/000/666?text=Aguardando+Vídeo", use_column_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("<br><center style='color:#444;'>VIDIOM AI v1.0 - Legendas Inteligentes</center>", unsafe_allow_html=True)
