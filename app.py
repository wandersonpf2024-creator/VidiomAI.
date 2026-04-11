import streamlit as st
from moviepy.video.io.VideoFileClip import VideoFileClip

# --- 1. CONFIGURAÇÃO E ESTILO ---
st.set_page_config(page_title="VIDIOM AI | Pricing", layout="wide")

st.markdown("""
    <style>
    /* Animações e Shimmer que você aprovou */
    @keyframes fadeInUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
    @keyframes shimmer { 0% { background-position: -200% 0; } 100% { background-position: 200% 0; } }

    .stApp { background-color: #0d0d0d; color: #ffffff; }
    
    .vidiom-logo-top {
        text-align: center; font-family: 'Inter', sans-serif; font-size: 30px;
        letter-spacing: 7px; text-transform: uppercase; padding: 20px 0;
        background: linear-gradient(to right, #d9d9d9 0%, #ffffff 50%, #d9d9d9 100%);
        background-size: 200% auto; -webkit-background-clip: text;
        -webkit-text-fill-color: transparent; animation: shimmer 4s infinite linear;
    }

    /* CARTÕES DE PREÇO ESTILO PREMIUM */
    .pricing-card {
        background: #1a1a1b;
        border: 1px solid #333;
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        transition: 0.3s;
        animation: fadeInUp 0.8s ease-out backwards;
    }
    .pricing-card:hover {
        border-color: #ffffff;
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(255,255,255,0.05);
    }
    .price-tag { font-size: 40px; font-weight: bold; margin: 15px 0; }
    .plan-name { color: #8e8e93; text-transform: uppercase; letter-spacing: 2px; }
    
    /* Botão de Upgrade */
    .stButton > button {
        border-radius: 25px !important;
        width: 100%;
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. MENU LATERAL (SIMULANDO O MINDVIDEO) ---
with st.sidebar:
    st.markdown('<div class="vidiom-logo-top" style="font-size:20px;">VIDIOM.AI</div>', unsafe_allow_html=True)
    st.write("---")
    st.write("### 👤 Account status")
    st.success("Free Member")
    st.write("**Credits left:** 05")
    st.write("---")
    menu = st.radio("Navigation", ["Video Editor", "Subscription Plans", "AI Models Settings"])

# --- 3. LOGICA DE NAVEGAÇÃO ---

if menu == "Subscription Plans":
    st.markdown("<h2 style='text-align: center;'>Choose your power</h2>", unsafe_allow_html=True)
    st.write("##")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="pricing-card">
                <div class="plan-name">Starter</div>
                <div class="price-tag">$0 <small>/mo</small></div>
                <p>• 5 AI Credits</p>
                <p>• Standard Speed</p>
                <p>• VIDIOM Watermark</p>
            </div>
        """, unsafe_allow_html=True)
        st.button("Current Plan", key="p1", disabled=True)

    with col2:
        st.markdown("""
            <div class="pricing-card" style="border-color: #ffffff;">
                <div class="plan-name" style="color: #ffffff;">Pro (Best Value)</div>
                <div class="price-tag">$29 <small>/mo</small></div>
                <p>• 100 AI Credits</p>
                <p>• No Watermark</p>
                <p>• Luma Ray 2.0 Access</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Upgrade to Pro", key="p2"):
            st.balloons()
            st.info("Redirecting to Stripe...")

    with col3:
        st.markdown("""
            <div class="pricing-card">
                <div class="plan-name">Agency</div>
                <div class="price-tag">$99 <small>/mo</small></div>
                <p>• Unlimited Credits</p>
                <p>• API Access</p>
                <p>• Dedicated Support</p>
            </div>
        """, unsafe_allow_html=True)
        st.button("Contact Sales", key="p3")

elif menu == "Video Editor":
    st.markdown('<div class="vidiom-logo-top">VIDIOM.AI</div>', unsafe_allow_html=True)
    st.markdown('<h4 style="color:#8e8e93; font-weight:normal; text-align:center;">Convert long videos into viral shorts</h4>', unsafe_allow_html=True)
    
    # Interface do Editor que já tínhamos (Simplificada aqui para teste)
    uploaded_file = st.file_uploader("Upload your video", type=["mp4"])
    if uploaded_file:
        st.video(uploaded_file)
        st.slider("Select segment", 0, 100, (0, 30))
        if st.button("Convert to 9:16"):
            st.warning("Please upgrade to PRO to remove watermark.")

else:
    st.write("### AI Models Configuration")
    st.selectbox("Default AI Engine", ["Vidu Q2", "Luma Ray 2.0", "Jimeng 3.0 Pro"])
    st.checkbox("Always use 4K resolution (Uses 2x credits)")
