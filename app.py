import streamlit as st

# --- 1. CONFIGURAÇÃO DA PÁGINA (ESTILO EDITOR PRO) ---
st.set_page_config(page_title="VIDIOM AI | Editor", layout="wide")

# CSS Avançado para criar o layout de 3 colunas e cores Pro Dark
st.markdown("""
    <style>
    /* Reset de cores e fundo preto absoluto do monitor */
    .stApp { background-color: #000000; color: #ffffff; }
    
    /* Configuração da Sidebar (Barra de Navegação) */
    [data-testid="stSidebar"] {
        background-color: #121213 !important;
        border-right: 1px solid #262627;
        width: 80px !important; # Barra de ícones fina
    }
    
    /* Estilo dos painéis (Library e Preview) */
    .editor-panel {
        background-color: #1a1a1b;
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #262627;
        height: 100%;
    }
    
    /* Área da Timeline (Simulação) */
    .timeline-panel {
        background-color: #1a1a1b;
        border-radius: 12px;
        padding: 15px;
        border: 1px solid #262627;
        margin-top: 15px;
    }
    
    /* Cabeçalho da Library */
    .library-header {
        font-size: 18px;
        font-weight: bold;
        color: #d1d1d1;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BARRA DE NAVEGAÇÃO LATERAL (SIDEBAR) ---
# Aqui simulamos os ícones que aparecem na imagem de referência
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>V</h2>", unsafe_allow_html=True) # Ícone V do VIDIOM
    st.write("---")
    st.markdown("<center>📂 <br> <small>Media</small></center>", unsafe_allow_html=True)
    st.write("---")
    st.markdown("<center>✂️ <br> <small>Cut</small></center>", unsafe_allow_html=True)
    st.write("---")
    st.markdown("<center>🤖 <br> <small>AI Tools</small></center>", unsafe_allow_html=True)
    st.write("##") # Espaço
    st.write("⚙️ Settings")

# --- 3. ÁREA DO EDITOR (LAYOUT DE COLUNAS) ---

st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Divisão Principal: 1 Coluna para Library | 2 Colunas para Preview+Timeline
col_lib, col_edit = st.columns([1, 2.5])

# PAINEL DA BIBLIOTECA (LIBRARY) - Esquerda
with col_lib:
    st.markdown('<div class="editor-panel">', unsafe_allow_html=True)
    st.markdown('<div class="library-header">Media Library</div>', unsafe_allow_html=True)
    
    # Campo de Upload igual à imagem
    uploaded_file = st.file_uploader("Upload or Drag Video", type=["mp4"])
    
    st.markdown("---")
    
    # Simulação dos 'All projects' e vídeos recentes
    st.write("**All projects**")
    c1, c2 = st.columns(2)
    with c1: st.image("https://via.placeholder.com/150x100?text=Video+1", caption="Scene 1")
    with c2: st.image("https://via.placeholder.com/150x100?text=Video+2", caption="Scene 2")
    
    st.markdown('</div>', unsafe_allow_html=True)

# PAINEL DE EDIÇÃO (PREVIEW E TIMELINE) - Direita
with col_edit:
    # 1. Player de Preview
    st.markdown('<div class="editor-panel">', unsafe_allow_html=True)
    st.markdown('<div class="library-header">Preview</div>', unsafe_allow_html=True)
    
    if uploaded_file:
        st.video(uploaded_file)
    else:
        st.image("https://via.placeholder.com/800x450?text=Waiting+for+Video", caption="Import video to start")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 2. Linha do Tempo (TIMELINE) - Simulação
    st.markdown('<div class="timeline-panel">', unsafe_allow_html=True)
    st.markdown('<div class="library-header" style="font-size:14px;">Timeline (Segment Selection)</div>', unsafe_allow_html=True)
    
    # Nosso slider de seleção do tempo vira a timeline aqui
    st.slider("00:00", 0, 100, (0, 30), label_visibility="collapsed")
    
    st.write("---")
    st.button("✂️ Generate 9:16 Short", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
