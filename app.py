import streamlit as st
from supabase import create_client
from groq import Groq

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="NutriScan IA | Planner", layout="wide")

# --- CSS PARA DESIGN MODERNO E TEXTO LARGO ---
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
        font-size: 3.5rem; font-weight: 900;
        margin-bottom: 10px;
    }
    .result-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 30px;
        margin: 20px auto;
        max-width: 900px;
        line-height: 1.6;
        color: #ffffff;
        font-size: 1.1rem;
        white-space: pre-wrap;
    }
    /* Estilização da Tabela de Histórico */
    .stDataFrame, .stTable {
        background: rgba(0, 0, 0, 0.5) !important;
        border-radius: 10px;
    }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 2. CONEXÃO SEGURA ---
try:
    groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
except Exception as e:
    st.error("Erro nas chaves: Verifique os Secrets no Streamlit Cloud.")
    st.stop()

# --- 3. FUNÇÃO DE GERAÇÃO COM FALLBACK ---
def gerar_plano_fitness(comando_usuario):
    modelos = ["llama-3.3-70b-versatile", "llama-3.1-70b-versatile"]
    
    for modelo in modelos:
        try:
            response = groq_client.chat.completions.create(
                model=modelo,
                messages=[
                    {"role": "system", "content": "Você é um nutricionista expert. Gere planos de emagrecimento com receitas detalhadas e passo a passo."},
                    {"role": "user", "content": comando_usuario}
                ],
                temperature=0.7
            )
            return response.choices[0].message.content
        except:
            continue
    return "❌ Erro ao conectar com a IA. Tente novamente."

# --- 4. INTERFACE ---
st.markdown('<h1 class="main-title">NUTRISCAN IA</h1>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    comando = st.text_area("Descreva seu objetivo ou peça uma receita:", 
                          placeholder="Ex: Plano para perder 5kg em 15 dias com foco em proteínas.", 
                          height=150)
    
    if st.button("GERAR MEU PLANO FITNESS 🚀", use_container_width=True):
        if comando:
            with st.spinner("🍳 A IA está criando sua estratégia..."):
                plano = gerar_plano_fitness(comando)
                
                # Exibe o resultado
                st.markdown(f'<div class="result-card">{plano}</div>', unsafe_allow_html=True)
                
                # --- SALVANDO NO SUPABASE (Com o nome real da consulta) ---
                try:
                    # Aqui usamos o próprio comando do usuário como nome no histórico
                    resumo_pedido = comando[:50] + "..." if len(comando) > 50 else comando
                    supabase.table("refeicoes").insert({
                        "nome_prato": resumo_pedido, # Agora aparece o que o usuário pediu!
                        "calorias": "Plano Gerado",
                        "macros": "Consultar IA"
                    }).execute()
                except Exception as e:
                    pass 
        else:
            st.warning("Por favor, digite seu objetivo primeiro!")

# --- 5. HISTÓRICO PERSONALIZADO ---
st.markdown("<br><br>", unsafe_allow_html=True)
with st.expander("📚 Ver Seus Últimos Pedidos", expanded=False):
    try:
        # Busca os dados no Supabase
        res = supabase.table("refeicoes").select("created_at, nome_prato").order("created_at", desc=True).limit(10).execute()
        
        if res.data:
            # Exibe de forma mais amigável
            for item in res.data:
                data_formatada = item['created_at'][:10] # Pega apenas a data YYYY-MM-DD
                st.write(f"🕒 **{data_formatada}** | 📝 {item['nome_prato']}")
        else:
            st.info("Você ainda não gerou nenhum plano.")
    except Exception as e:
        st.write("Erro ao carregar histórico.")
