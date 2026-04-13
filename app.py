# ------------------ IMPORTS ------------------
import streamlit as st
from supabase import create_client
from groq import Groq
from datetime import datetime
import time

# ------------------ CONFIG ------------------
st.set_page_config(page_title="NutriScan AI", layout="wide")

# ------------------ LOGIN SIMPLES ------------------
if "user" not in st.session_state:
    st.session_state.user = None

if not st.session_state.user:
    st.title("Login")
    email = st.text_input("Enter your email")

    if st.button("Continue"):
        if email:
            st.session_state.user = email
            st.rerun()

    st.stop()

# ------------------ CSS PREMIUM ------------------
st.markdown("""
<style>

/* HERO */
.hero {
    position: relative;
    height: 420px;
    border-radius: 25px;
    overflow: hidden;
    margin-bottom: 40px;
}

.hero img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    filter: brightness(0.6);
    transition: transform 6s ease;
}

.hero:hover img {
    transform: scale(1.08);
}

.hero::after {
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(to top, rgba(0,0,0,0.8), transparent);
}

.hero-text {
    position: absolute;
    bottom: 40px;
    left: 40px;
    color: white;
}

.hero-text h1 {
    font-size: 3.5rem;
    font-weight: 900;
    margin: 0;
    background: linear-gradient(90deg,#22c55e,#3b82f6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-text p {
    font-size: 1.2rem;
    opacity: 0.9;
}

/* INPUT */
textarea {
    background: #020617 !important;
    border-radius: 15px !important;
    border: 1px solid #1e293b !important;
    color: white !important;
}

/* BUTTON */
.stButton button {
    width: 100%;
    padding: 16px;
    border-radius: 12px;
    font-weight: bold;
    background: linear-gradient(90deg,#22c55e,#3b82f6);
    color: black;
}

/* CARDS */
.price-card {
    background: rgba(255,255,255,0.05);
    border-radius: 20px;
    padding: 25px;
    transition: 0.3s;
}

.price-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 0 25px #22c55e55;
}

.best-seller {
    border: 2px solid #22c55e;
}

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

#MainMenu, footer, header {visibility: hidden;}

</style>
""", unsafe_allow_html=True)

# ------------------ HERO ------------------
st.markdown("""
<div class="hero">
    <img src="https://images.unsplash.com/photo-1490645935967-10de6ba17061?q=80&w=2070">
    <div class="hero-text">
        <h1>NUTRISCAN AI</h1>
        <p>Your AI Nutrition & Fitness Planner</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ------------------ API ------------------
groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

# ------------------ USAGE ------------------
def check_usage():
    today = datetime.now().strftime('%Y-%m-%d')
    res = supabase.table("refeicoes").select("id").gte("created_at", today).execute()
    return len(res.data)

usage = check_usage()
limit = 3

# ------------------ MAIN ------------------
st.subheader("Generate your plan")

query = st.text_area("Describe your goal (e.g. 7-day diet plan):")

if usage >= limit:
    st.warning("Free limit reached. Upgrade to continue.")
else:
    st.write(f"Credits: {usage}/{limit}")

    if st.button("GENERATE PLAN 🚀"):
        if query:
            placeholder = st.empty()

            # loading
            with placeholder.container():
                st.write("🤖 AI is thinking...")
                bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.01)
                    bar.progress(i+1)

            try:
                resp = groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": query}]
                )
                plan = resp.choices[0].message.content

                placeholder.empty()
                output = st.empty()
                text = ""

                for c in plan:
                    text += c
                    output.markdown(f"""
                    <div style="background:#111;padding:20px;border-radius:15px;border:1px solid #22c55e;">
                    {text}
                    </div>
                    """, unsafe_allow_html=True)
                    time.sleep(0.003)

                supabase.table("refeicoes").insert({"nome_prato": query}).execute()

            except:
                st.error("AI error.")

# ------------------ STRIPE LINKS ------------------
STRIPE_BASIC = "https://buy.stripe.com/SEU_LINK_BASIC"
STRIPE_PRO = "https://buy.stripe.com/SEU_LINK_PRO"
STRIPE_ELITE = "https://buy.stripe.com/SEU_LINK_ELITE"

# ------------------ PRICING ------------------
st.markdown("## 💎 Upgrade")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(f"""
    <div class="price-card">
    <h3>Basic</h3>
    <h2>$3.99</h2>
    <p>10 credits</p>
    <a href="{STRIPE_BASIC}" target="_blank" class="buy-button">Buy Now</a>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="price-card best-seller">
    <h3>Pro</h3>
    <h2>$7.99</h2>
    <p>50 credits</p>
    <a href="{STRIPE_PRO}" target="_blank" class="buy-button">Best Value</a>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="price-card">
    <h3>Elite</h3>
    <h2>$47</h2>
    <p>Unlimited</p>
    <a href="{STRIPE_ELITE}" target="_blank" class="buy-button">Go Unlimited</a>
    </div>
    """, unsafe_allow_html=True)

# ------------------ HISTORY ------------------
with st.expander("📂 History"):
    res = supabase.table("refeicoes").select("nome_prato").order("created_at", desc=True).limit(5).execute()
    for i in res.data:
        st.write(f"✅ {i['nome_prato']}")
