import streamlit as st
from supabase import create_client
from groq import Groq
from datetime import datetime

# --- 1. PAGE CONFIG & DARK PREMIUM DESIGN ---
st.set_page_config(page_title="NutriScan AI | Fitness Planner", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background-image: linear-gradient(rgba(0, 0, 0, 0.85), rgba(0, 0, 0, 0.95)), 
                          url('https://images.unsplash.com/photo-1543362906-acfc16c67564?q=80&w=2070');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: white !important;
    }
    .main-title {
        text-align: center;
        background: linear-gradient(135deg, #22c55e 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem; font-weight: 900;
        margin-bottom: 10px;
    }
    .result-card {
        background: #111111 !important; 
        border: 2px solid #22c55e;
        border-radius: 20px;
        padding: 30px;
        margin: 20px auto;
        max-width: 900px;
        line-height: 1.6;
        color: white !important;
        white-space: pre-wrap;
    }
    .credit-warning {
        background: rgba(255, 75, 75, 0.2);
        border: 1px solid #ff4b4b;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
    }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 2. CONNECTIONS ---
try:
    groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
except Exception as e:
    st.error("Missing API Keys in Secrets.")
    st.stop()

# --- 3. LOGIC: CREDIT CHECKER (Daily Limit: 3) ---
def check_credits():
    today = datetime.now().strftime('%Y-%m-%d')
    try:
        # Counts how many rows were created by this user today
        res = supabase.table("refeicoes").select("id").gte("created_at", today).execute()
        usage = len(res.data)
        return usage
    except:
        return 0

# --- 4. AI GENERATOR ---
def generate_fitness_plan(user_input):
    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are an expert nutritionist. Provide detailed weight loss plans, step-by-step recipes, and fitness tips in English."},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except:
        return None

# --- 5. UI INTERFACE ---
st.markdown('<h1 class="main-title">NUTRISCAN AI</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>World-class AI Nutritionist & Fitness Planner</p>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    usage_today = check_credits()
    st.write(f"📊 **Daily Credits:** {usage_today}/3 used")

    if usage_today >= 3:
        st.markdown("""
            <div class="credit-warning">
                <h3>🚫 Daily Limit Reached</h3>
                <p>You have used your 3 free daily recipes. <br> <b>Get more credits to continue!</b></p>
                <button style="border-radius:20px; padding:10px; border:none; background:#22c55e; color:white; font-weight:bold; cursor:pointer;">GET CREDITS NOW</button>
            </div>
        """, unsafe_allow_html=True)
    else:
        user_query = st.text_area("What is your fitness goal?", placeholder="Ex: 7-day keto meal plan for weight loss...", height=150)
        
        if st.button("GENERATE MY PLAN 🚀", use_container_width=True):
            if user_query:
                with st.spinner("AI is cooking your plan..."):
                    plan = generate_fitness_plan(user_query)
                    if plan:
                        st.markdown(f'<div class="result-card">{plan}</div>', unsafe_allow_html=True)
                        
                        # DOWNLOAD OPTION
                        st.download_button(
                            label="📥 Download My Plan (TXT)",
                            data=plan,
                            file_name="my_fitness_plan.txt",
                            mime="text/plain"
                        )
                        
                        # Save to Database
                        supabase.table("refeicoes").insert({
                            "nome_prato": user_query[:50],
                            "calorias": "Premium Plan",
                            "macros": "Check PDF"
                        }).execute()
                        st.rerun() # Refresh to update credits
                    else:
                        st.error("AI service busy. Try again.")
            else:
                st.warning("Please enter your goal first!")

# --- 6. HISTORY ---
st.divider()
with st.expander("📂 My Recent Plans"):
    try:
        history = supabase.table("refeicoes").select("created_at, nome_prato").order("created_at", desc=True).limit(5).execute()
        for item in history.data:
            st.write(f"✅ {item['nome_prato']}")
    except:
        st.write("No history found.")
