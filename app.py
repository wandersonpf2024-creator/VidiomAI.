# ------------------ IMPORTS ------------------
import streamlit as st
from supabase import create_client
from groq import Groq
from datetime import datetime
import time

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

# ------------------ HERO ------------------
st.markdown("""
<div style="
    background-image: url('https://images.unsplash.com/photo-1490645935967-10de6ba17061?q=80&w=2070');
    background-size: cover;
    padding: 60px;
    border-radius: 20px;
    color: white;
    margin-bottom: 30px;">
    <h1>NUTRISCAN AI</h1>
    <p>Your AI Nutrition & Fitness Planner</p>
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
    try:
        res = supabase.table("refeicoes").select("*").execute()
        return len(res.data)
    except:
        return 0

usage = check_usage()
limit = 3

# ------------------ MAIN ------------------
st.subheader("Generate your plan")

query = st.text_area("Describe your goal (e.g. weight loss diet):")

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
                    bar.progress(i + 1)

            try:
                resp = groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": query}]
                )

                plan = resp.choices[0].message.content

                placeholder.empty()
                output = st.empty()
                text = ""

                # efeito digitando
                for c in plan:
                    text += c
                    output.markdown(f"""
                    <div style="
                        background:#111;
                        padding:20px;
                        border-radius:15px;
                        border:1px solid #22c55e;">
                        {text}
                    </div>
                    """, unsafe_allow_html=True)
                    time.sleep(0.002)

                # salvar no banco (CORRETO)
                supabase.table("refeicoes").insert({
                    "nome_prato": query
                }).execute()

            except Exception as e:
                st.error(f"Error: {e}")

# ------------------ STRIPE ------------------
STRIPE_BASIC = "https://buy.stripe.com/SEU_LINK_BASIC"
STRIPE_PRO = "https://buy.stripe.com/SEU_LINK_PRO"
STRIPE_ELITE = "https://buy.stripe.com/SEU_LINK_ELITE"

st.markdown("## 💎 Upgrade")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(f"""
    <div style="background:#111;padding:20px;border-radius:15px;">
    <h3>Basic</h3>
    <h2>$3.99</h2>
    <p>10 credits</p>
    <a href="{STRIPE_BASIC}" target="_blank">Buy</a>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div style="background:#111;padding:20px;border-radius:15px;border:2px solid #22c55e;">
    <h3>Pro</h3>
    <h2>$7.99</h2>
    <p>50 credits</p>
    <a href="{STRIPE_PRO}" target="_blank">Best Value</a>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div style="background:#111;padding:20px;border-radius:15px;">
    <h3>Elite</h3>
    <h2>$47</h2>
    <p>Unlimited</p>
    <a href="{STRIPE_ELITE}" target="_blank">Go Unlimited</a>
    </div>
    """, unsafe_allow_html=True)

# ------------------ HISTORY ------------------
with st.expander("📂 History"):
    try:
        res = supabase.table("refeicoes")\
            .select("nome_prato, created_at")\
            .order("created_at", desc=True)\
            .limit(5)\
            .execute()

        for i in res.data:
            st.write(f"✅ {i['nome_prato']} - {i['created_at']}")
    except:
        st.write("No history yet.")
