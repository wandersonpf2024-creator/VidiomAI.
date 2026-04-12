import streamlit as st
import os

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="VIDIOM AI | Subtitles", layout="wide")

# Inicializa o contador se não existir
if 'contador' not in st.session_state:
    st.session_state.contador = 0

# CSS para manter o estilo que você gosta
st.markdown("""
    <style>
    .stApp { background-color: #080808; color: #ffffff; }
    header { display: none !important; }
    .top-bar {
        background-color: #000000; border-bottom: 1px solid #1f1f1f;
        padding: 10px 40px; display: flex; justify-content: space-between;
        align-items: center; height: 65px; position: fixed; width: 100%; top: 0; z-index: 999;
    }
    .panel { background-color: #0f0f10; border: 1px solid #1f1f1f; border-radius: 12px; padding: 20px; }
    </style>
""", unsafe_allow_html=True)

# --- CABEÇALHO ---
st.markdown(f"""
    <div class="top-bar">
        <div style="font-weight: 900; font-size: 22px;">🎞️ VIDIOM.AI</div>
        <div style="display: flex; gap: 20px; align-items: center;">
            <div style="color: #888;">Uso: {st.session_state.contador}/3 hoje</div>
            <div style="background-color: white; color: black; padding: 6px 15px; border-radius: 5px; font-weight: bold; font-size: 12px;">UPGRADE</div>
        </div>
    </div>
""", unsafe_allow_html=True)

st.write("##")
st.write("##")

# --- LÓGICA PRINCIPAL ---
col1, col2 = st.columns([1, 1.5])

with col1:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("Subir Vídeo")
    video_file = st.file_uploader("Escolha o vídeo", type=["mp4", "mov"], label_visibility="collapsed")
    
    if video_file:
        estilo = st.selectbox("Estilo da Legenda", ["Amarelo Viral", "Branco Clean", "Impacto"])
        
        # SÓ MOSTRA O BOTÃO SE ESTIVER DENTRO DO LIMITE
        if st.session_state.contador < 3:
            if st.button("GERAR LEGENDA", type="primary", use_container_width=True):
                with st.status("Analizando áudio com Groq..."):
                    # SIMULAÇÃO DA IA (Aqui entra o código do Whisper/Groq)
                    import time
                    time.sleep(4) 
                    
                    # Se chegou aqui, deu certo:
                    st.session_state.contador += 1
                    st.success("Legenda gerada com sucesso!")
                    st.rerun() # Atualiza a tela para mostrar o vídeo legendado
        else:
            st.error("🚀 Limite diário atingido! Faça o Upgrade.")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("Resultado")
    if video_file:
        if st.session_state.contador > 0:
            st.video(video_file)
            st.caption(f"Exibindo vídeo com estilo: {estilo}")
        else:
            st.info("Clique em 'Gerar Legenda' para processar.")
    else:
        st.image("https://via.placeholder.com/600x350/000/666?text=Aguardando+Midia")
    st.markdown('</div>', unsafe_allow_html=True)
