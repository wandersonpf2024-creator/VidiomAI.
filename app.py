import streamlit as st
from supabase import create_client
from groq import Groq
import base64

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="VidiomAI | Nutri Vision", layout="centered")

# Estilo Dark Pro
st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at top, #121212 0%, #050505 100%);
        color: white;
    }
    .main-title {
        text-align: center;
        background: linear-gradient(90deg, #6366f1, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: bold;
    }
    .status-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #333;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. CONEXÃO COM SERVIÇOS (SECRETS) ---
try:
    GROQ_KEY = st.secrets["GROQ_API_KEY"]
    S_URL = st.secrets["SUPABASE_URL"]
    S_KEY = st.secrets["SUPABASE_KEY"]
    
    groq_client = Groq(api_key=GROQ_KEY)
    supabase = create_client(S_URL, S_KEY)
except Exception as e:
    st.error("⚠️ Erro nos Secrets: Verifique GROQ_API_KEY, SUPABASE_URL e SUPABASE_KEY no painel do Streamlit.")
    st.stop()

# --- 3. FUNÇÃO DE ANÁLISE (MODELOS ATUALIZADOS) ---
def analisar_imagem_com_ia(foto_bytes):
    img_b64 = base64.b64encode(foto_bytes).decode('utf-8')
    
    # Lista com os nomes oficiais e estáveis (sem o -preview)
    modelos_para_testar = [
        "llama-3.2-11b-vision",
        "llama-3.2-90b-vision"
    ]
    
    ultimo_erro = ""
    
    for modelo in modelos_para_testar:
        try:
            response = groq_client.chat.completions.create(
                model=modelo,
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Identifique o prato e estime calorias e macros. Responda APENAS no formato: Nome do Prato | Calorias | Macros"},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}}
                    ]
                }],
                temperature=0.2
            )
            return response.choices[0].message.content
        except Exception as e:
            ultimo_erro = str(e)
            continue 
            
    return f"ERRO_IA: {ultimo_erro}"

# --- 4. INTERFACE ---
st.markdown('<h1 class="main-title">NutriScan IA</h1>', unsafe_allow_html=True)
st.write("<p style='text-align:center;'>Análise instantânea com Groq Llama 3.2 Vision</p>", unsafe_allow_html=True)

foto = st.camera_input("")

if foto:
    if st.button("ANALISAR REFEIÇÃO 🚀", use_container_width=True, type="primary"):
        with st.spinner("IA processando imagem..."):
            
            resultado = analisar_imagem_com_ia(foto.getvalue())
            
            if "ERRO_IA" in resultado:
                st.error(f"Erro na Groq: {resultado}")
            else:
                try:
                    # Divisão dos dados recebidos
                    partes = resultado.split('|')
                    nome = partes[0].strip() if len(partes) > 0 else "Indefinido"
                    cals = partes[1].strip() if len(partes) > 1 else "N/A"
                    macs = partes[2].strip() if len(partes) > 2 else "N/A"
                    
                    # Exibição bonita
                    st.markdown(f"""
                    <div class="status-card">
                        <h3>🍽️ {nome}</h3>
                        <p>🔥 <b>Calorias:</b> {cals}</p>
                        <p>🥩 <b>Macros:</b> {macs}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Salvando no Supabase (Tabela: refeicoes)
                    dados_supabase = {
                        "nome_prato": nome,
                        "calorias": cals,
                        "macros": macs
                    }
                    supabase.table("refeicoes").insert(dados_supabase).execute()
                    st.success("✅ Salvo no banco de dados!")
                    
                except Exception as e:
                    st.warning(f"IA funcionou, mas houve erro ao salvar: {e}")

# --- 5. HISTÓRICO ---
st.divider()
if st.checkbox("Ver Histórico"):
    try:
        query = supabase.table("refeicoes").select("*").order("created_at", desc=True).limit(10).execute()
        if query.data:
            st.table(query.data)
        else:
            st.info("Nenhuma refeição encontrada.")
    except Exception as e:
        st.error(f"Erro ao carregar banco: {e}")
