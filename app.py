import streamlit as st
from supabase import create_client
from groq import Groq

# --- 1. CONFIGURAÇÃO DA PÁGINA E DESIGN PREMIUM ---
st.set_page_config(
    page_title="NutriScan IA | Planner Fitness",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CSS PERSONALIZADO (Layout Moderno com Fundo Fitness) ---
st.markdown("""
    <style>
    .stApp {
        background-image: linear-gradient(rgba(0, 0, 0, 0.8), rgba(0, 0, 0, 0.9)), 
                          url('https://images.unsplash.com/photo-1517836357463-d25dfeac3438?q=80&w=2070');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: white;
    }

    .main-title {
        text-align: center;
        background: linear-gradient(135deg, #22c55e 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 900;
        margin-bottom: 0px;
    }

    .card {
        background: rgba(255, 255, 255, 0.07);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 25px;
        margin-top: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
    }

    .stTextArea textarea {
        background-color: rgba(0, 0, 0, 0.5) !important;
        color: white !important;
        border: 1px solid #22c55e !important;
        border-radius: 15px !important;
    }

    .stButton > button {
        border-radius: 50px !important;
        background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%) !important;
        color: white !important;
        font-weight: bold !important;
        border: none !important;
        height: 50px;
    }

    #MainMenu, footer, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 2. CONEXÃO (SECRETS) ---
try:
    GROQ_KEY = st.secrets["GROQ_API_KEY"]
    S_URL = st.secrets["SUPABASE_URL"]
    S_KEY = st.secrets["SUPABASE_KEY"]
    
    groq_client = Groq(api_key=GROQ_KEY)
    supabase = create_client(S_URL, S_KEY)
except Exception as e:
    st.error("⚠️ Verifique as chaves GROQ_API_KEY, SUPABASE_URL e SUPABASE_KEY nos Secrets.")
    st.stop()

# --- 3. FUNÇÃO DE GERAÇÃO DE PLANO/RECEITA ---
def gerar_plano_emagrecimento(comando_usuario):
    try:
        # Usando o modelo Llama 3 70b para respostas complexas e detalhadas
        response = groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {
                    "role": "system", 
                    "content": "Você é um nutricionista e personal trainer expert em emagrecimento rápido e saudável. Crie planos detalhados, com receitas, dicas de treino e motivação."
                },
                {"role": "user", "content": comando_usuario}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Erro ao processar comando: {e}"

# --- 4. INTERFACE ---
st.markdown('<h1 class="main-title">NutriScan Planner</h1>', unsafe_allow_html=True)
st.write("<p style='text-align:center; color:#a1a1aa;'>Digite seu objetivo (ex: 'Quero emagrecer 10kg em 30 dias')</p>", unsafe_allow_html=True)

# Campo de comando
comando = st.text_area("Descreva seu objetivo ou peça uma receita:", placeholder="Ex: Crie um cardápio para emagrecer 5kg em 15 dias com receitas baratas.")

if st.button("GERAR MEU PLANO FITNESS 🚀", use_container_width=True):
    if comando:
        with st.spinner("A IA está montando seu plano personalizado..."):
            plano = gerar_plano_emagrecimento(comando)
            
            # Exibição do Plano Gerado
            st.markdown(f"""
            <div class="card">
                <h3 style='color: #22c55e;'>📋 Seu Plano Personalizado:</h3>
                <div style='line-height: 1.6;'>{plano.replace('', '<br>')}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Salva a consulta no histórico do Supabase
            try:
                supabase.table("refeicoes").insert({
                    "nome_prato": "Plano Gerado: " + comando[:30] + "...",
                    "calorias": "Personalizado",
                    "macros": "Ver Plano"
                }).execute()
            except:
                pass
    else:
        st.warning("Por favor, digite um comando primeiro!")

# --- 5. HISTÓRICO ---
st.divider()
with st.expander("📚 Ver Histórico de Pedidos", expanded=False):
    try:
        res = supabase.table("refeicoes").select("*").order("created_at", desc=True).limit(5).execute()
        if res.data:
            for item in res.data:
                st.write(f"🔹 {item['nome_prato']}")
    except:
        st.write("Histórico indisponível.")
