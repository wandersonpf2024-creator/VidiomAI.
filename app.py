st.markdown("""
<style>

/* 🎬 FUNDO CINEMÁTICO PREMIUM */
.stApp {
    background: radial-gradient(circle at top, #0f172a, #000000 80%);
    overflow-x: hidden;
}

/* efeito animado */
.stApp::before {
    content: "";
    position: fixed;
    width: 200%;
    height: 200%;
    background: linear-gradient(45deg, #22c55e22, #3b82f622, #22c55e22);
    animation: bgMove 12s linear infinite;
    z-index: 0;
}

@keyframes bgMove {
    0% { transform: translate(-30%, -30%); }
    50% { transform: translate(-10%, -10%); }
    100% { transform: translate(-30%, -30%); }
}

/* 🧠 CONTAINER PRINCIPAL */
.block-container {
    backdrop-filter: blur(20px);
    background: rgba(0,0,0,0.6);
    border-radius: 20px;
    padding: 30px;
    animation: fadeUp 1s ease;
}

/* animação entrada */
@keyframes fadeUp {
    from {opacity:0; transform:translateY(40px);}
    to {opacity:1; transform:translateY(0);}
}

/* 🔥 TÍTULO */
.main-title {
    text-align: center;
    font-size: 3.5rem;
    font-weight: 900;
    background: linear-gradient(90deg,#22c55e,#3b82f6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* ✨ INPUT PREMIUM */
textarea {
    background: #0f172a !important;
    border-radius: 15px !important;
    border: 2px solid transparent !important;
    transition: 0.3s !important;
}

textarea:focus {
    border: 2px solid #22c55e !important;
    box-shadow: 0 0 20px #22c55e !important;
}

/* 🚀 BOTÃO NETFLIX */
.stButton button {
    width: 100%;
    border-radius: 12px;
    padding: 14px;
    font-weight: bold;
    background: linear-gradient(90deg,#22c55e,#3b82f6);
    color: black;
    position: relative;
    overflow: hidden;
    transition: 0.3s;
}

/* efeito brilho passando */
.stButton button::before {
    content: "";
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(120deg, transparent, rgba(255,255,255,0.6), transparent);
    transition: 0.5s;
}

.stButton button:hover::before {
    left: 100%;
}

.stButton button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 25px #22c55e;
}

/* 💎 CARDS PREMIUM */
.price-card {
    background: rgba(255,255,255,0.05);
    border-radius: 20px;
    padding: 25px;
    backdrop-filter: blur(15px);
    transition: 0.3s;
    position: relative;
    overflow: hidden;
}

/* glow animado */
.price-card::after {
    content: "";
    position: absolute;
    width: 200%;
    height: 200%;
    background: linear-gradient(45deg, transparent, #22c55e33, transparent);
    animation: glowMove 6s linear infinite;
}

@keyframes glowMove {
    0% { transform: translate(-50%, -50%); }
    100% { transform: translate(50%, 50%); }
}

.price-card:hover {
    transform: translateY(-10px) scale(1.02);
    box-shadow: 0 0 30px #22c55e55;
}

/* ⭐ destaque */
.best-seller {
    border: 2px solid #22c55e;
}

/* badge */
.badge {
    background: linear-gradient(90deg,#22c55e,#3b82f6);
    color: black;
    padding: 5px 15px;
    border-radius: 50px;
    font-size: 0.8rem;
    font-weight: bold;
    position: absolute;
    top: -12px;
    left: 50%;
    transform: translateX(-50%);
}

/* botão compra */
.buy-button {
    display: block;
    padding: 12px;
    border-radius: 50px;
    text-align: center;
    background: linear-gradient(90deg,#22c55e,#3b82f6);
    color: black !important;
    font-weight: bold;
    margin-top: 15px;
    transition: 0.3s;
}

.buy-button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 15px #22c55e;
}

.old-price {
    text-decoration: line-through;
    color: #888;
}

#MainMenu, footer, header {visibility: hidden;}

</style>
""", unsafe_allow_html=True)
