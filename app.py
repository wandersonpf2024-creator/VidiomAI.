import streamlit as st
from supabase import create_client
from groq import Groq

# --- 1. CONFIGURAÇÃO DA PÁGINA (WIDE para mais espaço) ---
st.set_page_config(page_title="NutriScan IA | Planner", layout="wide")

# --- CSS AVANÇADO: Novo Fundo Clean e Legibilidade Total ---
st.markdown("""
    <style>
    /* 1. Imagem de Fundo Clean com Bancada no Centro */
    .stApp {
        background-image: linear-gradient(rgba(255, 255, 255, 0.8), rgba(255, 255, 255, 0.9)), 
                          url('https://images.unsplash.com/photo-1543362906-acfc16c67564?q=80&w=2070'); /* Imagem de alta qualidade com espaço vazio */
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #1a1a1a; /* Texto escuro para fundo claro */
    }

    /* 2. Título Neon Verde Fitness */
    .main-title {
        text-align: center;
        background: linear-gradient(135deg, #16a34a 0%, #15803d 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem; font-weight: 900;
        margin-bottom: 5px;
        text-shadow: 0px 4px 10px rgba(22, 163, 74, 0.3);
    }
    .sub-title {
        text-align: center; color: #6b7280;
        font-size: 1.1rem; margin-bottom: 30px;
    }

    /* 3. Card de Resposta (Totalmente Legível com Fundo Escuro) */
    .result-card {
        background: rgba(0, 0, 0, 0.9) !important; /* Fundo escuro para contrastar com o texto branco */
        backdrop-filter: blur(15px);
        border-radius: 20px;
        border: 2px solid rgba(22, 163, 74, 0.5);
        padding: 40px;
        margin: 20px auto;
        max-width: 900px;
        line-height: 1.8;
        color: #ffffff;
        font-size: 1.1rem;
        white-space: pre-wrap;
        word-wrap: break-word;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
    }

    /* 4. Estilização dos Inputs e Botões */
    .stTextArea textarea {
        background-color: rgba(255, 255, 255, 0.8) !important;
        color: black !important;
        border: 2px solid #16a34a !important;
        border-radius: 15px !important;
    }
    .stButton > button {
        border-radius: 50px !important;
        font-weight: bold !important;
        text-transform: uppercase !important;
        background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%) !important;
        color: white !important;
        border: none !important;
        height: 50px;
    }

    /* Esconde elementos do Streamlit */
    #MainMenu, footer, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 2. CONEXÃO SEGURA ---
try:
    groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
except Exception as e:
    st.error("Erro nas chaves nos Secrets.")
    st.stop()

# --- 3. FUNÇÃO DE GERAÇÃO COM FALLBACK ---
def gerar_plano_fitness(comando_usuario):
    # Modelos estáveis da Groq hoje
    modelos = ["llama-3.3-70b-versatile", "llama-3.1-70b-versatile", "llama-3.1-8b-instant"]
    
    for modelo in modelos:
        try:
            response = groq_client.chat.completions.create(
                model=modelo,
                messages=[
                    {"role": "system", "content": "Você é um nutricionista expert. Gere planos de emagrecimento detalhados, com receitas passo a passo, treinos e dicas de saúde."},
                    {"role": "user", "content": comando_usuario}
                ],
                temperature=0.7
            )
            return response.choices[0].message.content
        except:
            continue
    return "❌ Erro ao conectar com a IA. Tente novamente em alguns instantes."

# --- 4. INTERFACE ---
st.markdown('<h1 class="main-title">NUTRISCAN IA</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Aponte sua câmera para a comida e deixe a IA cuidar da sua saúde.</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    comando = st.text_area("Digite seu objetivo fitness:", 
                          placeholder="Ex: Quero um plano de 7 dias para perder barriga com receitas baratas.", 
                          height=150)
    
    if st.button("GERAR MEU PLANO FITNESS 🚀", use_container_width=True):
        if comando:
            with st.spinner("🍳 A IA está preparando seu plano personalizado..."):
                plano = gerar_plano_fitness(comando)
                
                # --- EXIBIÇÃO NO CARD ESCURO (LEITURA GARANTIDA) ---
                st.markdown(f'<div class="result-card">{plano}</div>', unsafe_allow_html=True)
                
                # Salva no banco de dados
                try:
                    resumo_pedido = comando[:50] + "..." if len(comando) > 50 else comando
                    supabase.table("refeicoes").insert({
                        "nome_prato": resume_pedido,
                        "calorias": "Foco Fitness",
                        "macros": "Vários"
                    }).execute()
                except:
                    pass
        else:
            st.warning("Por favor, descreva o que você deseja para a IA!")

# --- 5. HISTÓRICO PERSONALIZADO ---
st.markdown("<br><br>", unsafe_allow_html=True)
with st.expander("📊 Ver Seus Últimos Pedidos", expanded=False):
    try:
        res = supabase.table("refeicoes").select("created_at, nome_prato").order("created_at", desc=True).limit(5).execute()
        if res.data:
            for item in res.data:
                # Formatação simples e limpa
                data = item['created_at'][:10]
                st.write(f"📝 **{data}** | Objetivo: {item['nome_prato']}")
        else:
            st.info("Nenhum pedido recente.")
    except Exception as e:
        st.write("Erro ao carregar histórico.")
