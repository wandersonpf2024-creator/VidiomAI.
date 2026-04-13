# ------------------ IMPORTS ------------------
import streamlit as st
from supabase import create_client
from groq import Groq
from datetime import datetime
import time

# ------------------ CONFIG ------------------
st.set_page_config(page_title="NutriScan AI | Global", layout="wide")

# ------------------ LOGIN ------------------
if "user" not in st.session_state:
    st.session_state.user = None

if not st.session_state.user:
    st.markdown("""
        <style>
        .stApp { background: #020617; }
        .login-box {
            background: rgba(255,255,255,0.05);
            padding: 40px;
            border-radius: 20px;
            border: 1px solid #22c55e;
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)
    
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.title("🔐 Welcome")
        email = st.text_input("Enter your email to start:")
        if st.button("Access Platform", use_container_width=True):
            if email:
                st.session_state.user = email
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ------------------ CSS PREMIUM UNIFICADO ------------------
st.markdown("""
<style>
.stApp { background: #020617; color: white !important; }
.hero {
    position: relative; height: 400px; border-radius: 25px;
    overflow: hidden; margin-bottom: 40px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);
}
.hero img { width: 100%; height: 100%; object-fit: cover; filter: brightness(0.5); }
.hero-text { position: absolute; bottom: 40px; left: 40px; color: white; z-index: 2; }
.hero-text h1 {
    font-size: 4rem; font-weight: 900;
    background: linear-gradient(90deg, #22c55e, #3b82f6);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.price-card {
    background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 25px; padding: 30px; text-align: center; transition: 0.4s;
    height: 100%; position: relative;
}
.price-card:hover { transform: translateY(-10px); border-color: #22c55e; background: rgba(34, 197, 94, 0.05); }
.best-seller { border: 2px solid #22c55e !important; }
.badge {
    background: #22c55e; color: black; padding: 4px 15px; border-radius: 50px;
    font-size: 0.7rem; font-weight: 900; position: absolute; top: -12px; left: 50%; transform: translateX(-50%);
}
.buy-btn {
    display: block; padding: 12px; background: #22c55e; color: black !important;
    border-radius: 12px; font-weight: bold; text-decoration: none; margin-top: 20px; transition: 0.3s;
}
#MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ------------------ HERO SECTION ------------------
st.markdown("""
<div class="hero">
    <img src="https://images.unsplash.com/photo-1490645935967-10de6ba17061?q=80&w=2070">
    <div class="hero-text">
        <h1>NUTRISCAN AI</h1>
        <p>Your World-Class AI Nutrition & Fitness Coach</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ------------------ API SETUP ------------------
try:
    groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
except:
    st.error("Check your API keys in Secrets.")

def check_usage(email):
    try:
        res = supabase.table("refeicoes").select("id").eq("user_email", email).execute()
        return len(res.data)
    except: return 0

# ------------------ MAIN GENERATOR ------------------
usage = check_usage(st.session_state.user)
limit = 3

col_m1, col_m2, col_m3 = st.columns([1, 4, 1])
with col_m2:
    st.subheader(f"Welcome, {st.session_state.user}")
    query = st.text_area("What's your goal?", placeholder="Ex: 7-day keto plan...", height=120)

    if usage >= limit:
        st.warning("⚠️ Daily limit reached. Please upgrade to Pro below.")
    else:
        st.write(f"Credits used: **{usage}/{limit}**")
        if st.button("GENERATE PLAN 🚀", use_container_width=True):
            if query:
                placeholder = st.empty()
                with placeholder.container():
                    st.write("🤖 AI is thinking...")
                    bar = st.progress(0)
                    for i in range(100):
                        time.sleep(0.005)
                        bar.progress(i+1)
                
                try:
                    resp = groq_client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role":"system","content":"You are a pro nutritionist."},
                                  {"role":"user","content":query}]
                    )
                    plan = resp.choices[0].message.content
                    placeholder.empty()
                    st.markdown(f'<div style="background:rgba(255,255,255,0.05);padding:25px;border-radius:15px;border:1px solid #22c55e;white-space:pre-wrap;">{plan}</div>', unsafe_allow_html=True)
                    
                    supabase.table("refeicoes").insert({
                        "nome_prato": query[:50], 
                        "user_email": st.session_state.user
                    }).execute()
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

# ------------------ PRICING ------------------
st.markdown("<br><h2 style='text-align:center;'>💎 UPGRADE TO PRO</h2>", unsafe_allow_html=True)
p1, p2, p3 = st.columns(3)
with p1:
    st.markdown('<div class="price-card"><h3>Basic</h3><h2>$3.99</h2><p>10 Credits</p><a href="LINK1" class="buy-btn">BUY</a></div>', unsafe_allow_html=True)
with p2:
    st.markdown('<div class="price-card best-seller"><div class="badge">POPULAR</div><h3>Pro</h3><h2>$7.99</h2><p>50 Credits</p><a href="LINK2" class="buy-btn">BUY</a></div>', unsafe_allow_html=True)
with p3:
    st.markdown('<div class="price-card"><h3>Elite</h3><h2>$47.90</h2><p>Unlimited</p><a href="LINK3" class="buy-btn">BUY</a></div>', unsafe_allow_html=True)
