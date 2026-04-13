st.markdown("""
<style>

/* 🥗 FUNDO COM IMAGEM PREMIUM */
.stApp {
    background-image: 
        linear-gradient(rgba(0,0,0,0.75), rgba(0,0,0,0.9)),
        url('https://images.unsplash.com/photo-1498837167922-ddd27525d352?q=80&w=2070');
    
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* 🎬 CAMADA DE MOVIMENTO SUAVE */
.stApp::before {
    content: "";
    position: fixed;
    width: 120%;
    height: 120%;
    top: -10%;
    left: -10%;
    background: radial-gradient(circle, rgba(34,197,94,0.15), transparent 70%);
    animation: moveBg 12s ease-in-out infinite;
}

@keyframes moveBg {
    0% { transform: translate(0,0); }
    50% { transform: translate(20px, 20px); }
    100% { transform: translate(0,0); }
}

/* 📦 CONTAINER MAIS PREMIUM */
.block-container {
    backdrop-filter: blur(18px);
    background: rgba(0,0,0,0.6);
    border-radius: 25px;
    padding: 40px;
}

/* 🔥 TÍTULO COM MAIS VIDA */
.main-title {
    font-size: 4rem;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(90deg,#22c55e,#3b82f6,#22c55e);
    background-size: 200%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shine 6s linear infinite;
}

@keyframes shine {
    0% { background-position: 0% }
    100% { background-position: 200% }
}

</style>
""", unsafe_allow_html=True)
