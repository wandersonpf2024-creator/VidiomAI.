import streamlit as st
from supabase import create_client
from groq import Groq
import base64

# --- 1. CONFIGURAÇÃO DA PÁGINA E DESIGN ---
st.set_page_config(page_title="VidiomAI | Nutri Vision", layout="centered")

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

# --- 2. INICIALIZAÇÃO DE CLIENTES (SECRETS) ---
try:
    # Garanta que esses nomes existam no "Secrets" do Streamlit Cloud
    GROQ_KEY = st.secrets["GROQ_API_KEY"]
    S_URL = st.secrets["SUPABASE_URL"]
    S_KEY = st.secrets["SUPABASE_KEY"]
    
    groq_client = Groq(api_key=GROQ_KEY)
    supabase = create_client(S_URL, S_KEY)
except Exception as e:
    st.error("⚠️ Erro de Configuração: Verifique os 'Secrets' no painel do Streamlit.")
    st.stop()

# --- 3. FUNÇÃO DE ANÁLISE COM FALLBACK (PLANO B) ---
def analisar_imagem_com_ia(foto_bytes):
    img_b64 = base64.b64encode(foto_bytes).decode('utf-8')
    
    # Lista de modelos para tentar (caso o preview seja desativado)
    modelos_para_testar = [
        "llama-3.2-11b-vision-preview",
        "llama-3.2-90b-vision-preview"
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
                temperature=0.5,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            ultimo_erro = str(e)
            continue # Tenta o próximo modelo da lista
            
    return f"ERRO_IA: Não foi possível analisar a imagem. Detalhe: {ultimo_erro}"

# --- 4. INTERFACE DO USUÁRIO ---
st.markdown('<h1 class="main-title">NutriScan IA</h1>', unsafe_allow_html=True)
st.write("<p style='text-align:center;'>Aponte a câmera para o prato e deixe a Groq calcular tudo.</p>", unsafe_allow_html=True)

foto = st.camera_input("")

if foto:
    if st.button("ANALISAR REFEIÇÃO 🚀", use_container_width=True, type="primary"):
        with st.spinner("IA processando imagem..."):
            
            resultado = analisar_imagem_com_ia(foto.getvalue())
            
            if "ERRO_IA" in resultado:
                st.error(resultado)
            else:
                # 5. PROCESSAMENTO E SALVAMENTO NO SUPABASE
                try:
                    partes = resultado.split('|')
                    nome = partes[0].strip() if len(partes) > 0 else "Indefinido"
                    cals = partes[1].strip() if len(partes) > 1 else "N/A"
                    macs = partes[2].strip() if len(partes) > 2 else "N/A"
                    
                    # Exibe para o usuário
                    st.markdown(f"""
                    <div class="status-card">
                        <h3>🍽️ {nome}</h3>
                        <p>🔥 <b>Calorias:</b> {cals}</p>
                        <p>🥩 <b>Macros:</b> {macs}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Insere na tabela 'refeicoes' (conforme sua imagem anterior)
                    dados_supabase = {
                        "nome_prato": nome,
                        "calorias": cals,
                        "macros": macs
                    }
                    supabase.table("refeicoes").insert(dados_supabase).execute()
                    st.success("✅ Salvo no histórico do Supabase!")
                    
                except Exception as e:
                    st.warning(f"IA funcionou, mas houve erro ao salvar no banco: {e}")

# --- 6. HISTÓRICO EM TEMPO REAL ---
st.divider()
if st.checkbox("Ver Histórico de Refeições"):
    try:
        query = supabase.table("refeicoes").select("*").order("created_at", desc=True).limit(10).execute()
        if query.data:
            st.dataframe(query.data, use_container_width=True)
        else:
            st.info("Nenhuma refeição salva ainda.")
    except Exception as e:
        st.error(f"Erro ao carregar histórico: {e}")
