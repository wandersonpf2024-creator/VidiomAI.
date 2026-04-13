# ------------------ IMPORTS ------------------
import streamlit as st
from supabase import create_client
from groq import Groq
import time

# ------------------ CONFIG ------------------
st.set_page_config(page_title="NutriScan AI", layout="wide")

# ------------------ CSS PREMIUM (FIX) ------------------
st.markdown("""
<style>
.stApp { background: #020617; color: white; }

/* HERO */
.hero {
    position: relative; height: 350px; border-radius: 25px;
    overflow: hidden; margin-bottom: 30px;
}
.hero img { width: 100%; height: 100%; object-fit: cover; filter: brightness(0.4); }
.hero-text { position: absolute; bottom: 30px; left: 30px; z-index: 2; }
.hero-text h1 { 
    font-size: 3.5rem; font-weight: 900; 
    background: linear-gradient(90deg, #22c55e, #3b82f6);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}

/* CARDS DE PREÇO */
.price-card {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 20px; padding: 25px; text-align: center;
    transition: 0.3s; height: 100%; position: relative;
}
.price-card:hover { border-color: #22c55e; transform: translateY(-5px); }
.best { border: 2px solid #22c55e !important; }
.badge {
    background: #22c55e; color: black; padding: 2px 12px;
    border-radius: 50px; font-size: 0.7rem; font-weight: bold;
    position: absolute; top: -12px; left: 50%; transform: translateX(-50%);
}
.buy-btn {
    display: block; padding: 12px; background: #22c55e;
    color: black !important; border-radius: 12px;
    font-weight: bold; text-decoration: none; margin-top: 15px;
}

#MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ------------------ API SETUP ------------------
try:
    groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
except:
    st.error("Check your API Keys in Streamlit Secrets.")

# ------------------ HERO ------------------
st.markdown("""
<div class="hero">
    <img src="https://images.unsplash.com/photo-1490645935967-10de6ba17061?q=80&w=2070">
    <div class="hero-text">
        <h1>NUTRISCAN AI</h1>
        <p>Premium Nutrition & Fitness Planner</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ------------------ GENERATOR ------------------
col_main = st.columns([1, 4, 1])[1]

with col_main:
    st.subheader("🚀 Generate Your AI Plan")
    query = st.text_area("What is your goal today?", placeholder="Ex: 7-day keto diet...", height=120)
    
    # Botão de Gerar
    if st.button("GENERATE PLAN 🚀", use_container_width=True):
        if query:
            with st.spinner("Processing with Llama 3.3..."):
                try:
                    resp = groq_client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": query}]
                    )
                    plan = resp.choices[0].message.content
                    st.markdown(f'<div style="background:#111; padding:20px; border-radius:15px; border:1px solid #22c55e; white-space:pre-wrap;">{plan}</div>', unsafe_allow_html=True)
                    
                    # Tenta salvar, mas não trava se a tabela não existir
                    try:
                        supabase.table("refeicoes").insert({"nome_prato": query[:50]}).execute()
                    except: pass
                except:
                    st.error("AI is busy, please try again.")

# ------------------ PRICING SECTION ------------------
st.markdown("<br><h2 style='text-align:center;'>💎 UPGRADE TO PRO</h2>", unsafe_allow_html=True)
p1, p2, p3 = st.columns(3)

with p1:
    st.markdown("""
    <div class="price-card">
        <h3>Starter</h3>
        <h2>$3.99</h2>
        <p style="color:#22c55e;">10 Credits</p>
        <a href="LINK_PAYPAL_1" class="buy-btn">BUY NOW</a>
    </div>
    """, unsafe_allow_html=True)

with p2:
    st.markdown("""
    <div class="price-card best">
        <div class="badge">POPULAR</div>
        <h3>Pro Fitness</h3>
        <h2 style="margin:0;">$7.99</h2>
        <p style="color:#22c55e;">50 Credits</p>
        <a href="LINK_PAYPAL_2" class="buy-btn">GET 50% OFF</a>
    </div>
    """, unsafe_allow_html=True)

with p3:
    st.markdown("""
    <div class="price-card">
        <h3>Elite Annual</h3>
        <h2>$47.90</h2>
        <p style="color:#22c55e;">Unlimited / Year</p>
        <a href="LINK_PAYPAL_3" class="buy-btn">GO ELITE</a>
    </div>
    """, unsafe_allow_html=True)
