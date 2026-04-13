# ------------------ IMPORTS ------------------
import streamlit as st
from supabase import create_client
from groq import Groq
from datetime import datetime
import time

# PDF
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter

# ------------------ CONFIG ------------------
st.set_page_config(page_title="NutriScan AI", layout="wide")

# ------------------ LOGIN ------------------
if "user" not in st.session_state:
    st.session_state.user = None

if not st.session_state.user:
    st.title("Welcome to NutriScan AI")
    email = st.text_input("Enter your email")

    if st.button("Continue"):
        if email:
            st.session_state.user = email
            st.rerun()

    st.stop()

# ------------------ CSS PREMIUM ------------------
st.markdown("""
<style>

/* ANIMAÇÃO GLOBAL */
.block-container {
    animation: fadeIn 1s ease-in-out;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

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
}
.hero::after {
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(to top, rgba(0,0,0,0.8), transparent);
}

/* TEXTO HERO */
.hero-text {
    position: absolute;
    bottom: 40px;
    left: 40px;
    color: white;
}
.hero-text h1 {
    font-size: 3.5rem;
    font-weight: 900;
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

/* INPUT */
textarea {
    background: #020617 !important;
    border-radius: 15px !important;
    color: white !important;
}

/* BOTÃO */
.stButton button {
    background: linear-gradient(90deg,#22c55e,#3b82f6);
    color: black;
    border-radius: 12px;
    padding: 14px;
    font-weight: bold;
    transition: 0.3s;
}
.stButton button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 20px #22c55e;
}

/* CARDS */
.price-card {
    background: rgba(255,255,255,0.05);
    padding: 25px;
    border-radius: 20px;
    transition: 0.3s;
}
.price-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 0 25px #22c55e55;
}
.best {
    border: 2px solid #22c55e;
}

/* BOTÃO LINK */
.buy {
    display:block;
    padding:10px;
    background:#22c55e;
    text-align:center;
    border-radius:50px;
    margin-top:10px;
    color:black;
    font-weight:bold;
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

# ------------------ FUNÇÃO USO ------------------
def check_usage():
    try:
        res = supabase.table("refeicoes").select("*").execute()
        return len(res.data)
    except:
        return 0

# ------------------ PDF ------------------
def gerar_pdf(texto):
    file = "/mnt/data/plano.pdf"
    doc = SimpleDocTemplate(file, pagesize=letter)
    styles = getSampleStyleSheet()
    story = [Paragraph(l, styles["Normal"]) for l in texto.split("\n")]
    doc.build(story)
    return file

# ------------------ MAIN ------------------
usage = check_usage()
limit = 3

st.subheader("Generate your plan")

query = st.text_area("Describe your goal:")

if usage >= limit:
    st.warning("Free limit reached.")
else:
    st.write(f"Credits: {usage}/{limit}")

    if st.button("GENERATE PLAN 🚀"):
        if query:
            placeholder = st.empty()

            with placeholder.container():
                st.write("🤖 AI is thinking...")
                bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.01)
                    bar.progress(i+1)

            try:
                resp = groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role":"user","content":query}]
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
                    time.sleep(0.002)

                # salvar
                supabase.table("refeicoes").insert({
                    "nome_prato": query
                }).execute()

                # PDF
                pdf = gerar_pdf(plan)
                with open(pdf, "rb") as f:
                    st.download_button("📄 Download PDF", f, "plan.pdf")

            except Exception as e:
                st.error(e)

# ------------------ STRIPE ------------------
STRIPE_BASIC = "https://buy.stripe.com/SEU_LINK_BASIC"
STRIPE_PRO = "https://buy.stripe.com/SEU_LINK_PRO"
STRIPE_ELITE = "https://buy.stripe.com/SEU_LINK_ELITE"

st.markdown("## 💎 Upgrade")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(f"""
    <div class="price-card">
    <h3>Basic</h3>
    <h2>$3.99</h2>
    <a href="{STRIPE_BASIC}" class="buy">Buy</a>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="price-card best">
    <h3>Pro</h3>
    <h2>$7.99</h2>
    <a href="{STRIPE_PRO}" class="buy">Best</a>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="price-card">
    <h3>Elite</h3>
    <h2>$47</h2>
    <a href="{STRIPE_ELITE}" class="buy">Go</a>
    </div>
    """, unsafe_allow_html=True)

# ------------------ HISTÓRICO ------------------
with st.expander("📂 History"):
    try:
        res = supabase.table("refeicoes")\
            .select("nome_prato, created_at")\
            .order("created_at", desc=True)\
            .limit(5)\
            .execute()

        for i in res.data:
            st.write(f"✅ {i['nome_prato']}")
    except:
        st.write("No history yet.")
