import streamlit as st
from supabase import create_client
from groq import Groq

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="NutriScan IA | Planner", layout="centered")

# --- CSS PARA CORRIGIR O VISUAL E O TEXTO ---
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
        font-size: 3rem; font-weight: 900;
    }
    .card {
        background: rgba(255, 255, 255, 0.07);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 25px;
        margin-top: 20px;
        white-space: pre-wrap; /* EVITA O TEXTO VERTICAL */
        word-wrap: break-word;
    }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 2. CONEXÃO ---
try:
    groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
except Exception as e:
    st.error("Erro nas chaves de acesso.")
    st.stop()

# --- 3. FUNÇÃO COM MODELO ATUALIZADO (Llama 3.3) ---
def gerar_plano_fitness(comando_usuario):
    try:
        # Atualizado para o modelo Llama 3.3 70b (Versão mais recente)
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile", 
            messages=[
                {"role": "system", "content": "Você é um nutricionista e personal trainer expert. Crie planos de emagrecimento, receitas e treinos detalhados."},
                {"role": "user", "content": comando_usuario}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        # Fallback caso o 3.3 falhe, tenta o 3.1
        try:
            response = groq_client.chat.completions.create(
                model="llama-3.1-70b-versatile",
                messages=[{"role": "user", "content": comando_usuario}]
            )
            return response.choices[0].message.content
        except:
            return f"Erro na Groq: O modelo foi atualizado. Verifique o console.groq.com"

# --- 4. INTERFACE ---
st.markdown('<h1 class="main-title">NutriScan Planner</h1>', unsafe_allow_html=True)

comando = st.text_area("O que você deseja hoje?", placeholder="Ex: Dieta para perder 10kg em 30 dias...", height=150)

if st.button("GERAR PLANO AGORA 🚀", use_container_width=True):
    if comando:
        with st.spinner("IA Gerando seu plano..."):
            plano = gerar_plano_fitness(comando)
            
            # Exibição do Plano Gerado (Com CSS para não quebrar texto)
            st.markdown(f'<div class="card">{plano}</div>', unsafe_allow_html=True)
            
            # Tenta salvar no banco
            try:
                supabase.table("refeicoes").insert({"nome_prato": "Plano: " + comando[:20], "calorias": "Foco Fitness", "macros": "Vários"}).execute()
            except: pass
    else:
        st.warning("Escreva seu objetivo primeiro!")

st.divider()
if st.checkbox("Ver Histórico"):
    try:
        res = supabase.table("refeicoes").select("*").order("created_at", desc=True).limit(5).execute()
        st.table(res.data)
    except: st.write("Histórico vazio.")
