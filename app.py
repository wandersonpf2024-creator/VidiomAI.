import streamlit as st

# --- 1. CONFIGURAÇÃO E CSS AVANÇADO ---
st.set_page_config(page_title="VIDIOM AI | Plans", layout="wide")

st.markdown("""
    <style>
    /* Animações e Shimmer */
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

    /* BOTOES DE ALTERNANCIA (Mensal/Anual) */
    .toggle-container {
        background: #1a1a1b; border-radius: 10px; padding: 5px;
        display: inline-flex; gap: 10px; margin-bottom: 30px;
    }

    /* CARTÕES DE PLANO (LADO ESQUERDO) */
    .plan-card {
        background: #252526; border-radius: 12px; padding: 20px;
        margin-bottom: 15px; border: 2px solid transparent;
        cursor: pointer; position: relative; transition: 0.3s;
    }
    .plan-card.active { border-color: #3b82f6; background: #2d2d2e; }
    .plan-badge { 
        position: absolute; top: -10px; left: -5px; background: #ff4b4b;
        color: white; font-size: 10px; padding: 2px 8px; border-radius: 4px;
        transform: rotate(-5deg); font-weight: bold;
    }
    .price-large { font-size: 28px; font-weight: bold; float: right; }
    .credits-info { color: #3b82f6; font-weight: bold; display: flex; align-items: center; gap: 5px; }

    /* LISTA DE BENEFÍCIOS (LADO DIREITO) */
    .benefits-box {
        background: #1a1a1b; border-radius: 15px; padding: 30px; height: 100%;
    }
    .benefit-item { margin-bottom: 12px; display: flex; align-items: center; gap: 10px; color: #d1d1d1; }
    .check-icon { color: #22c55e; font-weight: bold; }

    /* BOTÃO OBTENHA AGORA */
    .btn-get-now {
        background: #3b82f6; color: white; border: none; padding: 15px;
        border-radius: 30px; width: 100%; font-size: 18px; font-weight: bold;
        margin-top: 20px; cursor: pointer; box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOGICA DE INTERFACE ---

st.markdown('<div class="vidiom-logo-top">VIDIOM.AI</div>', unsafe_allow_html=True)

# Seleção Mensal / Anual
col_t1, col_t2, col_t3 = st.columns([2, 1, 2])
with col_t2:
    billing = st.radio("", ["Monthly", "Annual (57% OFF 🥳)"], horizontal=True, label_visibility="collapsed")

st.write("##")

# Grid Principal (Dois lados como no seu print)
col_left, col_right = st.columns([1, 1.2])

with col_left:
    # Plano Lite
    st.markdown(f"""
        <div class="plan-card">
            <span class="price-large">${'16.9' if 'Monthly' in billing else '9.9'}</span>
            <div style="font-size: 24px; font-weight: bold;">Lite</div>
            <div class="credits-info">✦ 400 <span style="color:#8e8e93; font-size:12px;">+ 100 bonus</span></div>
            <div style="color:#8e8e93; font-size:12px; margin-top:10px;">{'Billed monthly' if 'Monthly' in billing else 'Billed annually: 53% OFF ↗'}</div>
        </div>
    """, unsafe_allow_html=True)

    # Plano Pro (Ativo por padrão no seu print)
    st.markdown(f"""
        <div class="plan-card active">
            <div class="plan-badge">Popular</div>
            <span class="price-large">${'29.9' if 'Monthly' in billing else '15.9'}</span>
            <div style="font-size: 24px; font-weight: bold;">Pro</div>
            <div class="credits-info">✦ 1000 <span style="color:#8e8e93; font-size:12px;">+ 200 bonus</span></div>
            <div style="color:#8e8e93; font-size:12px; margin-top:10px;">{'Billed monthly' if 'Monthly' in billing else 'Billed annually: 57% OFF ↗'}</div>
        </div>
    """, unsafe_allow_html=True)

    # Plano Max
    st.markdown(f"""
        <div class="plan-card">
            <span class="price-large">${'69.9' if 'Monthly' in billing else '39.9'}</span>
            <div style="font-size: 24px; font-weight: bold;">Max</div>
            <div class="credits-info">✦ 2500 <span style="color:#8e8e93; font-size:12px;">+ 300 bonus</span></div>
            <div style="color:#8e8e93; font-size:12px; margin-top:10px;">{'Billed monthly' if 'Monthly' in billing else 'Billed annually: 49% OFF ↗'}</div>
        </div>
    """, unsafe_allow_html=True)

with col_right:
    st.markdown(f"""
        <div class="benefits-box">
            <h3 style="margin-top:0;">What are the Pro benefits?</h3>
            <div class="benefit-item"><span class="check-icon">✔</span> Cost: <b>$0.029 / credit</b></div>
            <div class="benefit-item"><span class="check-icon">✔</span> Up to <b>100 videos</b> per month</div>
            <div class="benefit-item"><span class="check-icon">✔</span> Or up to <b>990,000</b> images</div>
            <div class="benefit-item"><span class="check-icon">✔</span> <b>New:</b> Sora 2 HD Video Support (15s/25s)</div>
            <div class="benefit-item"><span class="check-icon">✔</span> 3 Parallel tasks</div>
            <div class="benefit-item"><span class="check-icon">✔</span> HD 1080P Output</div>
            <div class="benefit-item"><span class="check-icon">✔</span> <b>No Watermarks</b></div>
            <div class="benefit-item"><span class="check-icon">✔</span> No queues & instant generation</div>
            <div class="benefit-item"><span class="check-icon">✔</span> Access to <b>All AI Models</b></div>
            <p style="font-size:10px; color:#8e8e93; margin-top:20px;">
                By subscribing, you agree to the Terms of Service.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Get it Now", use_container_width=True, type="primary"):
        st.success("Redirecting to Secure Checkout...")

# Footer de Segurança (Igual ao seu print)
st.write("---")
st.markdown("""
    <center>
        <p style="color:#8e8e93; font-size:12px;">
            🛡️ Supported by <b>PayPal</b> and <b>Airwallex</b> | PCI DSS Compliant
        </p>
    </center>
""", unsafe_allow_html=True)
