import streamlit as st
from supabase import create_client
from groq import Groq
import base64

# --- 1. CONFIGURAÇÃO DA PÁGINA E DESIGN MODERNO ---
st.set_page_config(
    page_title="NutriScan IA | Fitness Style",
    layout="centered", # Mantém o conteúdo focado no meio da tela
    initial_sidebar_state="collapsed"
)

# --- CSS AVANÇADO PARA PLANO DE FUNDO E ESTILIZAÇÃO ---
st.markdown("""
    <style>
    /* 1. Imagem de Fundo com Overlay Escuro (Mulheres Fitness) */
    .stApp {
        background-image: linear-gradient(rgba(0, 0, 0, 0.85), rgba(0, 0, 0, 0.95)), 
                          url('https://images.unsplash.com/photo-1517836357463-d25dfeac3438?q=80&w=2070'); /* Link de imagem fitness profissional */
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: white;
    }

    /* 2. Título Principal com Gradiente Neon */
    .main-title {
        text-align: center;
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: -2px;
        margin-bottom: 5px;
        text-shadow: 0px 4px 15px rgba(79, 172, 254, 0.5);
    }
    
    .sub-title {
        text-align: center;
        color: #a1a1aa;
        font-size: 1.1rem;
        margin-bottom: 30px;
    }

    /* 3. Estilização dos Cards (Visual de Vidro / Glassmorphism) */
    .stDiv > div > div > .stMarkdown, .card, .recipe-card {
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        border-radius: 20px !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        padding: 25px !important;
        margin-top: 20px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37) !important;
    }

    /* Card específico da Receita (Verde Fitness) */
    .recipe-card {
        border: 1px solid rgba(16, 185, 129, 0.3) !important;
        background: rgba(16, 185, 129, 0.05) !important;
    }

1.    /* 4. Botões Modernos e Arredondos */
    .stButton > button {
        border-radius: 50px !important;
        font-weight: bold !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        transition: all 0.3s ease !important;
    }
    
    /* Botão Primário (Analisar) com Gradiente */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%) !important;
        border: none !important;
        color: black !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0px 5px 20px rgba(0, 242, 254, 0.6) !important;
    }

1.    /* 5. Inputs (Câmera, Checkbox) */
    .stCameraInput > div {
        border-radius: 20px !important;
        border: 2px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    .stCheckbox {
        color: #a1a1aa !important;
    }
    
    /* Esconde menus padrões do Streamlit para visual mais limpo */
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
    st.error("⚠️ Erro nos Secrets do Streamlit Cloud.")
    st.stop()

# --- 3. FUNÇÕES DE IA ---

def analisar_imagem_com_ia(foto_bytes):
    img_b64 = base64.b64encode(foto_bytes).decode('utf-8')
    # Usando o modelo mais estável Atualmente (Llava)
    modelo = "llava-v1.5-7b-4096-preview" 
    try:
        response = groq_client.chat.completions.create(
            model=modelo,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": "Nome do Prato | Calorias Estimadas | Macros"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}}
                ]
            }]
        )
        return response.choices[0].message.content
    except: return "ERRO_IA"

def gerar_receita_saudavel(nome_prato):
    try:
        response = groq_client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{
                "role": "user",
                "content": f"Sugira uma receita saudável e fitness inspirada no prato '{nome_prato}'. Liste ingredientes e preparo rápido."
            }]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Erro ao gerar receita: {e}"

# --- 4. INTERFACE ---
st.markdown('<h1 class="main-title">NUTRISCAN IA</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">A tecnologia que transforma sua foto em resultado fitness.</p>', unsafe_allow_html=True)

foto = st.camera_input("")

if foto:
    # Usando st.container para aplicar o estilo Glassmorphism
    with st.container():
        if st.button("ANALISAR AGORA 🚀", use_container_width=True, type="primary"):
            with st.spinner("Analisando..."):
                resultado = analisar_imagem_com_ia(foto.getvalue())
                
                if resultado != "ERRO_IA":
                    try:
                        partes = resultado.split('|')
                        nome = partes[0].strip() if len(partes) > 0 else "Prato"
                        cals = partes[1].strip() if len(partes) > 1 else "---"
                        macs = partes[2].strip() if len(partes) > 2 else "---"

                        st.session_state['ultimo_prato'] = nome
                        
                        # Exibição estilizada (Glassmorphism)
                        st.markdown(f"""
                        <div class="card">
                            <h2 style='color: #4facfe; margin-top:0;'>🍴 {nome}</h2>
                            <p style='font-size: 1.2rem;'>🔥 <b>{cals}</b></p>
                            <p style='font-size: 1.1rem; color: #a1a1aa;'>🥩 Macros: {macs}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        supabase.table("refeicoes").insert({"nome_prato": nome, "calorias": cals, "macros": macs}).execute()
                        st.success("✅ Salvo no histórico!")
                    except: st.error("Erro no formato da resposta da IA.")
                else: st.error("Falha na análise. Tente novamente.")

# --- 5. PARTE DAS RECEITAS ---
if 'ultimo_prato' in st.session_state:
    st.divider()
    if st.button(f"🥗 CRIAR RECEITA FITNESS DE {st.session_state['ultimo_prato'].upper()}", use_container_width=True):
        with st.spinner("Chef IA cozinhando..."):
            receita = gerar_receita_saudavel(st.session_state['ultimo_prato'])
            # Exibição estilizada da receita
            st.markdown(f"""
            <div class="recipe-card">
                <h3 style='color: #10b981; margin-top:0;'>🌱 Sugestão Saudável</h3>
                <div style='color: #e4e4e7; line-height: 1.6;'>{receita.replace('', '<br>')}</div>
            </div>
            """, unsafe_allow_html=True)

# --- 6. HISTÓRICO ---
st.divider()
with st.expander("📊 Ver Histórico Recente", expanded=False):
    try:
        res = supabase.table("refeicoes").select("*").order("created_at", desc=True).limit(5).execute()
        if res.data: 
            # Exibe histórico em formato simples
            for item in res.data:
                st.write(f"📖 {item['nome_prato']} - {item['calorias']}")
        else: st.info("Nenhuma refeição salva.")
    except: st.write("Erro ao carregar.")
