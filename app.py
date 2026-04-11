import streamlit as st
import os

# --- 1. CONFIGURAÇÃO DE LAYOUT CINEMATOGRÁFICO ---
st.set_page_config(page_title="VIDIOM.AI Pro", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    /* FUNDO PRETO ABSOLUTO E REMOÇÃO DE PADRÕES */
    .stApp { background-color: #080808; color: #ffffff; }
    header, [data-testid="stHeader"] { display: none !important; }
    .stMainBlockContainer { padding: 0px !important; max-width: 100% !important; }

    /* BARRA SUPERIOR (HEADER) - FIEL À IMAGEM */
    .top-header {
        height: 60px;
        background-color: #000000;
        border-bottom: 1px solid #1f1f1f;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0 30px;
        position: fixed;
        width: 100%;
        top: 0;
        z-index: 1000;
    }

    .nav-items { display: flex; gap: 25px; align-items: center; font-family: sans-serif; }
    .nav-link { font-size: 11px; letter-spacing: 1.5px; color: #888; font-weight: 600; cursor: pointer; }
    .nav-link:hover { color: white; }
    
    .btn-upgrade-white {
        background-color: white; color: black; padding: 6px 16px;
        border-radius: 4px; font-weight: 800; font-size: 11px; text-transform: uppercase;
    }

    /* BARRA LATERAL DE FERRAMENTAS (SIDEBAR FINA) */
    .sidebar-tools {
        width: 55px;
        background-color: #000000;
        border-right: 1px solid #1f1f1f;
        height: 100vh;
        position: fixed;
        left: 0;
        top: 60px;
        display: flex;
        flex-direction: column;
        align-items: center;
        padding-top: 20px;
        gap: 25px;
        z-index: 999;
    }
    .tool-btn { color: #444; font-size: 18px; cursor: pointer; transition: 0.3s; }
    .tool-btn:hover { color: #6366f1; }

    /* AREA DE TRABALHO (GRID DE PAINÉIS) */
    .workspace {
        margin-left: 55px;
        margin-top: 60px;
        padding: 15px;
        display: grid;
        grid-template-columns: 1fr 1.5fr;
        grid-template-rows: 1fr 0.5fr;
        gap: 15px;
        height: calc(100vh - 80px);
    }

    .panel-box {
        background-color: #111112;
        border: 1px solid #1f1f1f;
        border-radius: 8px;
        padding: 15px;
        position: relative;
    }

    .panel-label {
        font-size: 11px;
        color: #555;
        text-transform: uppercase;
        font-weight: bold;
        margin-bottom: 10px;
        display: flex;
        justify-content: space-between;
    }

    /* TIMELINE (LINHA DO TEMPO) */
    .timeline-area {
        grid-column: span 2;
        background-color: #0a0a0b;
        border-radius: 8px;
        border: 1px solid #1f1f1f;
        padding: 15px;
    }

    /* OCULTAR ELEMENTOS CHAVE DO STREAMLIT QUE ESTRAGAM O DESIGN */
    [data-testid="stFileUploadDropzone"] { background: #1a1a1b !important; border: 1px dashed #333 !important; }
    </style>
""", unsafe_allow_html=True)

# --- 2. RENDERIZAÇÃO DO CABEÇALHO ---
st.markdown(f"""
    <div class="top-header">
        <div style="display: flex; align-items: center;">
            <img src="https://via.placeholder.com/150x30?text=VIDIOM.AI" style="height: 22px;"> </div>
        <div class="nav-items">
            <div class="nav-link">PROJECTS</div>
            <div class="nav-link">TOOLS</div>
            <div class="nav-link">DASHBOARD</div>
            <div class="nav-link">SETTINGS</div>
            <div class="btn-upgrade-white">UPGRADE</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- 3. BARRA DE FERRAMENTAS LATERAL ---
st.markdown("""
    <div class="sidebar-tools">
        <div class="tool-btn">🗂️</div>
        <div class="tool-btn">✂️</div>
        <div class="tool-btn">💬</div>
        <div class="tool-btn">🎵</div>
        <div class="tool-btn">⚙️</div>
    </div>
""", unsafe_allow_html=True)

# --- 4. ÁREA DE EDIÇÃO (GRID) ---
# Usamos colunas nativas do Streamlit dentro da margem para controle funcional
main_area = st.container()

with main_area:
    # Espaçamento para o cabeçalho e sidebar
    st.markdown('<div style="margin-left: 65px; margin-top: 75px; padding-right: 20px;">', unsafe_allow_html=True)
    
    row1_col1, row1_col2 = st.columns([1, 1.8])
    
    # PAINEL DA BIBLIOTECA (Library)
    with row1_col1:
        st.markdown('<div class="panel-box" style="height: 400px;">', unsafe_allow_html=True)
        st.markdown('<div class="panel-label"><span>LIBRARY</span> <span>Filter ▽</span></div>', unsafe_allow_html=True)
        
        up = st.file_uploader("Upload", type=["mp4"], label_visibility="collapsed")
        
        # Grid de vídeos (thumbnails) igual à imagem
        st.write("---")
        t1, t2 = st.columns(2)
        t1.image("https://via.placeholder.com/160x90/1a1a1b/666?text=Scene+01", caption="Vidiom_01")
        t2.image("https://via.placeholder.com/160x90/1a1a1b/666?text=Scene+02", caption="Vidiom_02")
        st.markdown('</div>', unsafe_allow_html=True)

    # PAINEL DE PREVIEW (Video)
    with row1_col2:
        st.markdown('<div class="panel-box" style="height: 400px; background-color: #000;">', unsafe_allow_html=True)
        st.markdown('<div class="panel-label">VIDEO PREVIEW</div>', unsafe_allow_html=True)
        if up:
            st.video(up)
        else:
            st.markdown("<center><br><br><br><p style='color:#333;'>Aguardando mídia...</p></center>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # PAINEL DA LINHA DO TEMPO (Timeline)
    st.markdown('<div style="margin-top: 15px;">', unsafe_allow_html=True)
    st.markdown('<div class="timeline-area">', unsafe_allow_html=True)
    st.markdown('<div class="panel-label">TIMELINE / EDITOR</div>', unsafe_allow_html=True)
    
    # Simulação visual da trilha de vídeo
    st.markdown("""
        <div style="height: 40px; background: #1a1a1c; border-radius: 4px; border-left: 4px solid #6366f1; margin-bottom: 5px; width: 70%;"></div>
        <div style="height: 40px; background: #1a1a1c; border-radius: 4px; border-left: 4px solid #333; width: 90%;"></div>
    """, unsafe_allow_html=True)
    
    st.slider("Playhead", 0, 100, (20, 80), label_visibility="collapsed")
