import streamlit as st
from supabase import create_client
from groq import Groq

# --- 1. PAGE CONFIG (GLOBAL FOCUS) ---
st.set_page_config(page_title="NutriScan AI", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background-image: linear-gradient(rgba(0, 0, 0, 0.85), rgba(0, 0, 0, 0.95)), 
                          url('https://images.unsplash.com/photo-1490645935467-49f76bb62c27?q=80&w=2070');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    .main-title {
        text-align: center;
        background: linear-gradient(135deg, #22c55e 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem; font-weight: 900;
    }
    .result-card {
        background: #111111;
        border: 2px solid #22c55e;
        border-radius: 20px;
        padding: 30px;
        color: white;
    }
    .paypal-button {
        display: block;
        width: 100%;
        background: #0070ba;
        color: white !important;
        text-align: center;
        padding: 15px;
        border-radius: 50px;
        font-weight: bold;
        text-decoration: none;
        box-shadow: 0 4px 15px rgba(0, 112, 186, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. CONNECTIONS ---
try:
    groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
except:
    st.error("API Keys missing.")
    st.stop()

# --- 3. DATABASE LOGIC (AUTOMATED CREDITS) ---
def get_user_credits(email):
    # Aqui simulamos a busca por e-mail no Supabase
    # Na automação, o Make.com vai dar 'Update' nesta coluna credits
    try:
        res = supabase.table("users").select("credits").eq("email", email).single().execute()
        return res.data['credits']
    except:
        return 0

def use_credit(email, current_credits):
    supabase.table("users").update({"credits": current_credits - 1}).eq("email", email).execute()

# --- 4. INTERFACE ---
st.markdown('<h1 class="main-title">NUTRISCAN AI</h1>', unsafe_allow_html=True)

# Simulação de Login (Para o mercado internacional, o e-mail é essencial para os créditos)
user_email = st.text_input("Enter your email to access your credits:", placeholder="email@example.com")

if user_email:
    credits = get_user_credits(user_email)
    st.write(f"💎 **Available Credits:** {credits}")

    if credits <= 0:
        st.markdown(f"""
            <div style="background: rgba(255,255,255,0.05); padding: 30px; border-radius: 20px; text-align: center;">
                <h2 style="color: #ff4b4b;">OUT OF CREDITS</h2>
                <p>Get 10 extra AI generations for <b>$4.99</b></p>
                <a href="SEU_LINK_DO_PAYPAL_AQUI" class="paypal-button">💳 BUY 10 CREDITS VIA PAYPAL</a>
                <p style="font-size: 0.8rem; margin-top: 10px;">Credits are added automatically after payment.</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        query = st.text_area("What is your fitness goal today?", height=150)
        
        if st.button("GENERATE PLAN 🚀", use_container_width=True):
            if query:
                with st.spinner("AI is thinking..."):
                    # Chamada da IA
                    response = groq_client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": query}]
                    )
                    plan = response.choices[0].message.content
                    
                    st.markdown(f'<div class="result-card">{plan}</div>', unsafe_allow_html=True)
                    
                    # Deduz o crédito automaticamente
                    use_credit(user_email, credits)
                    st.rerun()
