import streamlit as st
from supabase import create_client
from groq import Groq

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="NutriScan IA | Planner", layout="wide")

# --- CSS REVISADO: FUNDO ESCURO COM IMAGEM FITNESS ---
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

    /* Card de Resposta: Fundo escuro sólido para leitura perfeita */
    .result-card {
        background: #111111 !important; 
        border: 2px solid #22c55e;
        border-radius: 20px;
        padding: 30px;
        margin: 20px auto;
        max-width: 900px;
        line-height: 1.6;
        color: white !important;
        font-size: 1.1rem;
        white-space: pre-wrap;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }

    /* Estilo para os campos de entrada */
    .stTextArea textarea {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
        border: 1px solid #22c55e !important;
    }

    #MainMenu, footer, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 2. CONEXÃO ---
try:
    groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
except Exception as e:
    st.error("Erro nos Secrets.")
    st.stop()

# --- 3. FUNÇÃO DE IA ---
def gerar_plano_fitness(comando_usuario):
    modelos = ["llama-3.3-70b-versatile", "llama-3.1-70b-versatile"]
    for modelo in modelos:
        try:
            response = groq_client.chat.completions.create(
                model=modelo,
                messages=[
                    {"role": "system", "content": "Você é um nutricionista expert. Gere planos de emagrecimento e receitas detalhadas."},
                    {"role": "user", "content": comando_usuario}
                ],
                temperature=0.7
            )
            return response.choices[0].message.content
        except: continue
    return "❌ Erro ao conectar com a IA."

# --- 4. INTERFACE ---
st.markdown('<h1 class="main-title">NUTRISCAN IA</h1>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    comando = st.text_area("Descreva seu objetivo fitness:", placeholder="Ex: Dieta para 15 dias...", height=150)
    
    if st.button("GERAR PLANO AGORA 🚀", use_container_width=True):
        if comando:
            with st.spinner("IA processando..."):
                plano = gerar_plano_fitness(comando)
                st.markdown(f'<div class="result-card">{plano}</div>', unsafe_allow_html=True)
                
                try:
                    resumo = comando[:50]
                    supabase.table("refeicoes").insert({
                        "nome_prato": resumo,
                        "calorias": "Fitness",
                        "macros": "Vários"
                    }).execute()
                except: pass
        else:
            st.warning("Digite seu objetivo primeiro!")

# --- 5. HISTÓRICO ---
st.divider()
with st.expander("📊 Ver Histórico"):
    try:
        res = supabase.table("refeicoes").select("created_at, nome_prato").order("created_at", desc=True).limit(5).execute()
        for item in res.data:
            st.write(f"📝 {item['nome_prato']}")
    except: st.write("Histórico vazio.")
        
