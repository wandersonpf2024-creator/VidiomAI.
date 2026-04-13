import streamlit as st
from supabase import create_client
from groq import Groq
from datetime import datetime

# --- CONFIG ---
st.set_page_config(page_title="NutriScan AI | Premium", layout="wide")

# --- CSS PREMIUM ---
st.markdown("""
<style>

/* FUNDO PREMIUM */
.stApp {
    background: radial-gradient(circle at top, #0f172a, #000000 80%);
}

/* ANIMAÇÃO FUNDO */
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

/* CONTAINER */
.block-container {
    backdrop-filter: blur(20px);
    background: rgba(0,0,0,0.6);
    border-radius: 20px;
    padding: 30px;
    animation: fadeUp 1s ease;
}

/* ANIMAÇÃO */
@keyframes fadeUp {
    from {opacity:0; transform:translateY(40px);}
    to {opacity:1; transform:translateY(0);}
}

/* TITULO */
.main-title {
    text-align: center;
    font-size: 3.5rem;
    font-weight: 900;
    background: linear-gradient(90deg,#22c55e,#3b82f6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* INPUT */
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

/* BOTÃO */
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

/* CARDS */
.price-card {
    background: rgba(255,255,255,0.05);
    border-radius: 20px;
    padding: 25px;
    backdrop-filter: blur(15px);
    transition: 0.3s;
}

.price-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 0 30px #22c55e55;
}

.best-seller {
    border: 2px solid #22c55e;
}

.badge {
    background: linear-gradient(90deg,#22c55e,#3b82f6);
    color: black;
    padding: 5px 15px;
    border-radius: 50px;
    font-size: 0.8rem;
    font-weight: bold;
    position: relative;
    top: -10px;
}

/* BOTÃO COMPRA */
.buy-button {
    display: block;
    padding: 12px;
    border-radius: 50px;
    text-align: center;
    background: linear-gradient(90deg,#22c55e,#3b82f6);
    color: black !important;
    font-weight: bold;
    margin-top: 15px;
}

.old-price {
    text-decoration: line-through;
    color: #888;
}

#MainMenu, footer, header {visibility: hidden;}

</style>
""", unsafe_allow_html=True)

# --- API ---
try:
    groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
except:
    st.error("Configure suas API keys no secrets.toml")
    st.stop()

# --- USO ---
def check_usage():
    today = datetime.now().strftime('%Y-%m-%d')
    try:
        res = supabase.table("refeicoes").select("id").gte("created_at", today).execute()
        return len(res.data)
    except:
        return 0

# --- UI ---
st.markdown('<h1 class="main-title">NUTRISCAN IA</h1>', unsafe_allow_html=True)

usage = check_usage()
limit = 3

col1, col2, col3 = st.columns([1,4,1])

with col2:
    if usage >= limit:
        st.warning("Limite grátis atingido. Faça upgrade.")
    else:
        st.write(f"🔥 Créditos: {usage}/{limit}")
        query = st.text_area("Descreva seu objetivo:")

        if st.button("GERAR PLANO 🚀"):
            if query:
                with st.spinner("IA trabalhando..."):
                    try:
                        resp = groq_client.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            messages=[{"role": "user", "content": query}]
                        )
                        plan = resp.choices[0].message.content

                        st.markdown(f"""
                        <div style="background:#111; padding:20px; border-radius:15px; border:1px solid #22c55e;">
                        {plan}
                        </div>
                        """, unsafe_allow_html=True)

                        supabase.table("refeicoes").insert({
                            "nome_prato": query
                        }).execute()

                        st.rerun()
                    except:
                        st.error("Erro na IA.")
            else:
                st.info("Digite algo.")

# --- PLANOS ---
st.markdown("## 💎 Upgrade")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="price-card">
    <h3>Basic</h3>
    <h2>$3.99</h2>
    <p>10 créditos</p>
    <a href="#" class="buy-button">Comprar</a>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="price-card best-seller">
    <div class="badge">POPULAR</div>
    <h3>Pro</h3>
    <h2>$7.99</h2>
    <p>50 créditos</p>
    <a href="#" class="buy-button">Comprar</a>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="price-card">
    <h3>Elite</h3>
    <h2>$47</h2>
    <p>Ilimitado</p>
    <a href="#" class="buy-button">Comprar</a>
    </div>
    """, unsafe_allow_html=True)

# --- HISTÓRICO ---
with st.expander("📂 Histórico"):
    try:
        res = supabase.table("refeicoes").select("nome_prato").order("created_at", desc=True).limit(5).execute()
        for i in res.data:
            st.write(i["nome_prato"])
    except:
        st.write("Sem histórico")
