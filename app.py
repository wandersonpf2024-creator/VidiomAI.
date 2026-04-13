import streamlit as st
from supabase import create_client
from groq import Groq
from datetime import datetime

# --- 1. PAGE CONFIG & PREMIUM DARK DESIGN ---
st.set_page_config(page_title="NutriScan AI | Premium Fitness", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background-image: linear-gradient(rgba(0, 0, 0, 0.85), rgba(0, 0, 0, 0.95)), 
                          url('https://images.unsplash.com/photo-1490645935467-49f76bb62c27?q=80&w=2070');
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
        margin-bottom: 5px;
    }
    /* Pricing Cards Styling */
    .price-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        transition: 0.3s;
        height: 100%;
    }
    .price-card:hover {
        border: 1px solid #22c55e;
        transform: translateY(-5px);
        background: rgba(34, 197, 94, 0.05);
    }
    .best-seller {
        border: 2px solid #22c55e !important;
        position: relative;
    }
    .badge {
        background: #22c55e;
        color: black;
        padding: 5px 15px;
        border-radius: 50px;
        font-size: 0.8rem;
        font-weight: bold;
        position: absolute;
        top: -15px;
        left: 50%;
        transform: translateX(-50%);
    }
    .buy-button {
        display: block;
        width: 100%;
        padding: 12px;
        background: #22c55e;
        color: black !important;
        text-decoration: none;
        border-radius: 50px;
        font-weight: bold;
        margin-top: 20px;
    }
    .old-price {
        text-decoration: line-through;
        color: #a1a1aa;
        font-size: 0.9rem;
    }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 2. CONNECTIONS ---
try:
    groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
except:
    st.error("API Keys missing in Secrets.")
    st.stop()

# --- 3. DAILY LIMIT LOGIC ---
def check_daily_usage():
    today = datetime.now().strftime('%Y-%m-%d')
    try:
        res = supabase.table("refeicoes").select("id").gte("created_at", today).execute()
        return len(res.data)
    except: return 0

# --- 4. MAIN INTERFACE ---
st.markdown('<h1 class="main-title">NUTRISCAN AI</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:1.2rem;'>Your Personal AI Nutritionist & Workout Planner</p>", unsafe_allow_html=True)

usage = check_daily_usage()
limit = 3

col_main_1, col_main_2, col_main_3 = st.columns([1, 4, 1])

with col_main_2:
    if usage >= limit:
        st.warning("⚠️ Free daily limit reached. Upgrade to continue generating pro plans!")
    else:
        st.write(f"🔥 **Free Credits Today:** {usage}/{limit}")
        query = st.text_area("Describe your goal (e.g., 7-day keto plan for weight loss):", height=150)
        
        if st.button("GENERATE PLAN 🚀", use_container_width=True):
            if query:
                with st.spinner("AI is crafting your plan..."):
                    try:
                        resp = groq_client.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            messages=[{"role": "user", "content": query}]
                        )
                        plan = resp.choices[0].message.content
                        st.markdown(f'<div style="background:#111; padding:25px; border-radius:15px; border:1px solid #22c55e; white-space:pre-wrap;">{plan}</div>', unsafe_allow_html=True)
                        
                        # Save usage
                        supabase.table("refeicoes").insert({"nome_prato": query[:50], "calorias": "Free Tier"}).execute()
                        st.rerun()
                    except: st.error("Service busy.")
            else:
                st.info("Please enter your goal first.")

# --- 5. PRICING SECTION (THE "GRINGA" STYLE) ---
st.markdown("<br><br><h2 style='text-align:center;'>💎 UPGRADE TO PRO</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#a1a1aa;'>Unlock unlimited potential and reach your goals faster.</p>", unsafe_allow_html=True)

col_p1, col_p2, col_p3 = st.columns(3)

with col_p1:
    st.markdown(f"""
        <div class="price-card">
            <h3>Basic Pack</h3>
            <h2 style="margin:10px 0;">$3.99</h2>
            <p style="color:#22c55e; font-weight:bold;">10 AI Credits</p>
            <ul style="text-align:left; font-size:0.9rem; color:#a1a1aa;">
                <li>✓ Full Diet Plans</li>
                <li>✓ Recipe PDF Export</li>
                <li>✓ No Daily Limits</li>
            </ul>
            <a href="LINK_PAYPAL_1" class="buy-button">BUY NOW</a>
        </div>
    """, unsafe_allow_html=True)

with col_p2:
    st.markdown(f"""
        <div class="price-card best-seller">
            <div class="badge">MOST POPULAR</div>
            <h3>Fitness Pro</h3>
            <span class="old-price">$14.99</span>
            <h2 style="margin:5px 0;">$7.99</h2>
            <p style="color:#22c55e; font-weight:bold;">50 AI Credits</p>
            <ul style="text-align:left; font-size:0.9rem; color:#a1a1aa;">
                <li>✓ Everything in Basic</li>
                <li>✓ Custom Workout Routine</li>
                <li>✓ Priority AI Processing</li>
            </ul>
            <a href="LINK_PAYPAL_2" class="buy-button">GET 50% OFF</a>
        </div>
    """, unsafe_allow_html=True)

with col_p3:
    st.markdown(f"""
        <div class="price-card">
            <h3>Elite Annual</h3>
            <span class="old-price">$99.00</span>
            <h2 style="margin:5px 0;">$47.90</h2>
            <p style="color:#22c55e; font-weight:bold;">Unlimited/Year</p>
            <ul style="text-align:left; font-size:0.9rem; color:#a1a1aa;">
                <li>✓ Unlimited Generations</li>
                <li>✓ 24/7 AI Coaching</li>
                <li>✓ Save Over 50% Yearly</li>
            </ul>
            <a href="LINK_PAYPAL_3" class="buy-button">GO UNLIMITED</a>
        </div>
    """, unsafe_allow_html=True)

# --- 6. HISTORY ---
st.markdown("<br>", unsafe_allow_html=True)
with st.expander("📂 Recent Activity"):
    try:
        res = supabase.table("refeicoes").select("nome_prato").order("created_at", desc=True).limit(5).execute()
        for i in res.data: st.write(f"✅ {i['nome_prato']}")
    except: st.write("No history.")
