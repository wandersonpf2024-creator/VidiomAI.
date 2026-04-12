import streamlit as st

# --- 1. CONFIGURAÇÃO E DESIGN CUSTOMIZADO ---
st.set_page_config(page_title="VIDIOM.AI | Legendas Mágicas", layout="wide")

st.markdown("""
    <style>
    /* Fundo em degradê escuro Profissional */
    .stApp {
        background: radial-gradient(circle at top, #1a1a2e 0%, #080808 100%);
        color: white;
        font-family: 'Inter', sans-serif;
    }
    
    /* REMOVE CABEÇALHO PADRÃO */
    header, [data-testid="stHeader"] { display: none !important; }
    .stMainBlockContainer { padding-top: 20px !important; }

    /* NAVBAR SUPERIOR */
    .nav-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 20px 10%;
    }
    .nav-links { display: flex; gap: 30px; font-size: 14px; color: #bbb; }
    .btn-entrar {
        background: #ffffff; color: black; padding: 8px 25px;
        border-radius: 50px; font-weight: bold; font-size: 14px;
    }

    /* TEXTO CENTRAL (HERO SECTION) */
    .hero-container {
        text-align: center;
        margin-top: 80px;
        padding: 0 15%;
    }
    .hero-title {
        font-size: 72px;
        font-weight: 800;
        line-height: 1.1;
        margin-bottom: 20px;
        background: linear-gradient(to right, #fff 30%, #6366f1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-subtitle {
        font-size: 20px;
        color: #999;
        max-width: 700px;
        margin: 0 auto 50px auto;
    }

    /* CAIXA DE INPUT (O CORAÇÃO DA PÁGINA) */
    .input-box {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 40px;
        max-width: 800px;
        margin: 0 auto;
        backdrop-filter: blur(10px);
    }
    
    /* Estilização do botão de upload do Streamlit para combinar */
    [data-testid="stFileUploadDropzone"] {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 2px dashed rgba(255, 255, 255, 0.2) !important;
        border-radius: 15px !important;
    }
    
    .footer-tech {
        margin-top: 40px;
        font-size: 12px;
        color: #555;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. BARRA DE NAVEGAÇÃO ---
st.markdown(f"""
    <div class="nav-bar">
        <div style="display: flex; align-items: center; gap: 10px;">
            <img src="https://via.placeholder.com/150x40?text=VIDIOM.AI" style="height: 25px;"> 
        </div>
        <div class="nav-links">
            <div>Valores</div>
            <div>Blog</div>
            <div>Ajuda</div>
        </div>
        <div class="btn-entrar">Entrar</div>
    </div>
""", unsafe_allow_html=True)

# --- 3. CONTEÚDO PRINCIPAL (HERO) ---
st.markdown("""
    <div class="hero-container">
        <h1 class="hero-title">Gerador de Legendas <br> Inteligente</h1>
        <p class="hero-subtitle">
            Poupe horas de edição. Crie legendas dinâmicas e virais para seus vídeos 
            em poucos cliques com nossa tecnologia de IA avançada.
        </p>
    </div>
""", unsafe_allow_html=True)

# --- 4. CAIXA DE AÇÃO (INPUTS) ---
with st.container():
    st.markdown('<div class="input-box">', unsafe_allow_html=True)
    
    # Input de Link
    col_link, col_btn = st.columns([3, 1])
    with col_link:
        url = st.text_input("YouTube / Instagram Link", placeholder="Cole o link aqui...", label_visibility="collapsed")
    with col_btn:
        st.button("Criar agora", type="primary", use_container_width=True)
    
    st.markdown("<div style='text-align:center; margin: 20px 0; color: #444; font-weight: bold;'>OU</div>", unsafe_allow_html=True)
    
    # Upload de Arquivo
    uploaded_file = st.file_uploader("Escolha seu Arquivo ou Arraste até aqui", type=["mp4", "mov"], label_visibility="collapsed")
    
    if uploaded_file:
        st.success("Vídeo carregado! Clique abaixo para processar.")
        if st.button("🚀 GERAR LEGENDAS (0/3 Grátis)", use_container_width=True):
            st.write("Processando seu vídeo...")
            
    st.markdown('</div>', unsafe_allow_html=True)

# --- 5. RODAPÉ ---
st.markdown("""
    <div class="footer-tech">
        🔴 Com tecnologia da <b>Groq & OpenAI</b>
    </div>
""", unsafe_allow_html=True)
