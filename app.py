import streamlit as st
import os

# --- 1. CONFIGURAÇÃO DE INTERFACE CINEMATOGRÁFICA ---
st.set_page_config(page_title="VIDIOM AI | Professional Studio", layout="wide")

st.markdown("""
    <style>
    /* Fundo Preto Profundo e Scroll customizado */
    .stApp { background-color: #080808; color: #e0e0e0; font-family: 'Inter', sans-serif; }
    
    /* REMOVE ELEMENTOS PADRÃO */
    header, [data-testid="stHeader"] { display: none !important; }
    .stMainBlockContainer { padding: 0px !important; }

    /* CABEÇALHO SUPERIOR (FIXO) */
    .top-bar {
        background-color: #000000;
        border-bottom: 1px solid #1f1f1f;
        padding: 10px 30px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        height: 65px;
        position: fixed;
        width: 100%;
        top: 0;
        z-index: 999;
    }

    .nav-links { display: flex; gap: 30px; align-items: center; font-size: 13px; letter-spacing: 1px; }
    .nav-item { color: #888; cursor: pointer; font-weight: 500; }
    .nav-item:hover { color: white; }
    
    .btn-upgrade-top {
        background-color: white; color: black; padding: 6px 18px;
        border-radius: 6px; font-weight: bold; font-size: 12px;
    }

    /* LAYOUT PRINCIPAL (BARRA LATERAL + CONTEÚDO) */
    .editor-layout { display: flex; margin-top: 65px; height: calc(100vh - 65px); }

    /* BARRA LATERAL DE FERRAMENTAS (ÍCONES VERTICAIS) */
    .tool-sidebar {
        width: 60px; background-color: #000000;
        border-right: 1px solid #1f1f1f;
        display: flex; flex-direction: column; align-items: center; padding-top: 20px; gap: 25px;
    }
    .tool-icon { color: #555; font-size: 20px; cursor: pointer; }
    .tool-icon:hover { color: #6366f1; }

    /* PAINÉIS DE EDIÇÃO */
    .panel {
        background-color: #0f0f10; border: 1px solid #1f1f1f;
        border-radius: 10px; padding: 15px; overflow: hidden;
    }
    .panel-title { font-size: 12px; color: #666; margin-bottom: 10px; text-transform: uppercase; }

    /* SIMULAÇÃO DE TIMELINE */
    .timeline-bg {
        background-color: #0a0a0b; border-top: 1px solid #1f1f1f;
        height: 200px; padding: 20px; position: relative;
    }
    .timeline-track {
        background: #1a1a1c; height: 40px; border-radius: 4px; 
        margin-bottom: 8px; border: 1px solid #262628;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CABEÇALHO (LOGO E NAV) ---
st.markdown(f"""
    <div class="top-bar">
        <div style="display: flex; align-items: center; gap: 15px;">
            <span style="font-weight: 900; font-size: 20px; letter-spacing: -1px;">🎞️ VIDIOM.AI</span>
        </div>
        <div class="nav-links">
            <div class="nav-item">PROJECTS</div>
            <div class="nav-item">TOOLS</div>
            <div class="nav-item">DASHBOARD</div>
            <div class="nav-item">SETTINGS</div>
            <div class="btn-upgrade-top">UPGRADE</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- 3. CORPO DO EDITOR ---
# Usamos colunas para dividir a Barra Lateral de Ícones do resto do App
main_col1, main_col2 = st.columns([0.05, 0.95])

with main_col1:
    st.markdown("""
        <div class="tool-sidebar">
            <div class="tool-icon">🏠</div>
            <div class="tool-icon">✂️</div>
            <div class="tool-icon">📁</div>
            <div class="tool-icon">🪄</div>
            <div class="tool-icon">⚙️</div>
        </div>
    """, unsafe_allow_html=True)

with main_col2:
    st.write("##") # Espaço para o header fixo
    
    # Grid Superior: Library (Esquerda) e Preview (Direita)
    up_col1, up_col2 = st.columns([1, 2])
    
    with up_col1:
        st.markdown('<div class="panel" style="height: 450px;">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">Library</div>', unsafe_allow_html=True)
        st.file_uploader("Import Media", type=["mp4"], label_visibility="collapsed")
        st.write("---")
        # Miniaturas (Thumbnails)
        c1, c2 = st.columns(2)
        c1.image("https://via.placeholder.com/150x90/1a1a1c/ffffff?text=Scene+A")
        c2.image("https://via.placeholder.com/150x90/1a1a1c/ffffff?text=Scene+B")
        st.markdown('</div>', unsafe_allow_html=True)

    with up_col2:
        st.markdown('<div class="panel" style="height: 450px;">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">Video Preview</div>', unsafe_allow_html=True)
        # Espaço do Player
        st.image("https://via.placeholder.com/800x400/000000/666666?text=Ready+to+Edit", use_column_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Grid Inferior: Timeline (Ocupa a largura toda)
    st.markdown('<div class="panel" style="margin-top: 15px;">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">Timeline / Sequence</div>', unsafe_allow_html=True)
    
    # Simulação visual das tracks da imagem
    st.markdown("""
        <div style="padding: 10px;">
            <div class="timeline-track" style="width: 60%; background: linear-gradient(90deg, #6366f1 0%, #4f46e5 100%);"></div>
            <div class="timeline-track" style="width: 80%; background: #262628;"></div>
        </div>
    """, unsafe_allow_html=True)
    
    st.slider("Playhead", 0, 100, (10, 50), label_visibility="collapsed")
    st.button("EXPORT 9:16 SHORT", type="primary", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
