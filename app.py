# ------------------ IMPORTS ------------------
import streamlit as st
from supabase import create_client
from groq import Groq
from datetime import datetime

# ------------------ CONFIG ------------------
st.set_page_config(page_title="NutriScan AI | Premium", layout="wide")

# ------------------ PREMIUM CSS ------------------
st.markdown("""
<style>

/* 🥗 BACKGROUND IMAGE */
.stApp {
    background-image: 
        linear-gradient(rgba(0,0,0,0.75), rgba(0,0,0,0.9)),
        url('https://images.unsplash.com/photo-1498837167922-ddd27525d352?q=80&w=2070');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* subtle animation */
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

/* container */
.block-container {
    backdrop-filter: blur(18px);
    background: rgba(0,0,0,0.6);
    border-radius: 25px;
    padding: 40px;
}

/* title */
.main-title {
    font-size: 3.8rem;
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

/* input */
textarea {
    background: #020617 !important;
    border-radius: 15px !important;
    border: 1px solid #1e293b !important;
    color: white !important;
}

textarea:focus {
    border: 1px solid #22c55e !important;
    box-shadow: 0 0 20px #22c55e;
}

/* button */
.stButton button {
    width: 100%;
    padding: 16px;
    border-radius: 12px;
    font-weight: bold;
    background: linear-gradient(90deg,#22c55e,#3b82f6);
    color: black;
    transition: 0.3s;
}

.stButton button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 20px #22c55e;
}

/* pricing cards */
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

/* buy button */
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

/* hide streamlit UI */
#MainMenu, footer, header {visibility: hidden;}

</style>
""", unsafe_allow_html=True)

# ------------------ CONNECTIONS ------------------
try:
    groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    supabase = create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"]
    )
except:
    st.error("API keys not configured properly.")
    st.stop()

# ------------------ USAGE ------------------
def check_usage():
    today = datetime.now().strftime('%Y-%m-%d')
    try:
        res = supabase.table("refeicoes").select("id").gte("created_at", today).execute()
        return len(res.data)
    except:
        return 0

# ------------------ UI ------------------
st.markdown('<h1 class="main-title">NUTRISCAN AI</h1>', unsafe_allow_html=True)

usage = check_usage()
limit = 3

col1, col2, col3 = st.columns([1,4,1])

with col2:
    if usage >= limit:
        st.warning("⚠️ Free daily limit reached. Upgrade to continue.")
    else:
        st.write(f"🔥 Credits: {usage}/{limit}")
        query = st.text_area("Describe your goal (e.g. 7-day weight loss plan):")

        if st.button("GENERATE PLAN 🚀"):
            if query:
                with st.spinner("AI is generating your plan..."):
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
                        st.error("Error generating plan.")
            else:
                st.info("Please enter your goal.")

# ------------------ PRICING ------------------
st.markdown("## 💎 Upgrade")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="price-card">
    <h3>Basic</h3>
    <h2>$3.99</h2>
    <p>10 credits</p>
    <a href="#" class="buy-button">Buy Now</a>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="price-card best-seller">
    <h3>Pro</h3>
    <h2>$7.99</h2>
    <p>50 credits</p>
    <a href="#" class="buy-button">Best Value</a>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="price-card">
    <h3>Elite</h3>
    <h2>$47</h2>
    <p>Unlimited</p>
    <a href="#" class="buy-button">Go Unlimited</a>
    </div>
    """, unsafe_allow_html=True)

# ------------------ HISTORY ------------------
with st.expander("📂 Recent Activity"):
    try:
        res = supabase.table("refeicoes").select("nome_prato").order("created_at", desc=True).limit(5).execute()
        for i in res.data:
            st.write(f"✅ {i['nome_prato']}")
    except:
        st.write("No history yet.")
