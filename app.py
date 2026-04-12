import streamlit as st
from supabase import create_client
import openai
import base64

# --- 1. CONEXÃO COM SEU ECOSSISTEMA ---
# Substitua pelos seus dados do painel do Supabase
SUPABASE_URL = "https://sua-url.supabase.co"
SUPABASE_KEY = "sua-chave-anon-public"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

openai.api_key = "SUA_CHAVE_OPENAI"

# --- 2. ESTILO DARK (Sem Laranja) ---
st.set_page_config(page_title="VIDIOM AI | Nutri Vision", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    .stCamera { border: 2px solid #6366f1; border-radius: 15px; overflow: hidden; }
    .metric-card {
        background: #111; border: 1px solid #222;
        padding: 20px; border-radius: 12px; text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. LÓGICA DE VISÃO ---
def analisar_prato(image_bytes):
    base64_image = base64.b64encode(image_bytes).decode('utf-8')
    
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Apenas retorne: Alimento, Calorias, Proteínas. Formato: Nome | Kcal | Prot"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]
            }
        ]
    )
    return response.choices[0].message.content

# --- 4. INTERFACE ---
st.title("📸 Scanner Nutricional")

foto = st.camera_input("Tire foto do seu prato")

if foto:
    bytes_data = foto.getvalue()
    
    if st.button("ANALISAR AGORA 🚀", type="primary", use_container_width=True):
        with st.spinner("IA e Supabase trabalhando..."):
            
            # Passo 1: IA analisa
            resultado = analisar_prato(bytes_data)
            
            # Passo 2: Salvar no Supabase Database
            # Criamos um registro na sua tabela 'refeicoes'
            data = {
                "nome_prato": resultado.split('|')[0],
                "calorias": resultado.split('|')[1],
                "status": "Finalizado"
            }
            supabase.table("refeicoes").insert(data).execute()
            
            # Exibir Resultado
            st.markdown(f'<div class="metric-card"><h2>{resultado}</h2></div>', unsafe_allow_html=True)
            st.success("Salvo no seu histórico do Supabase!")

# --- 5. HISTÓRICO (Lendo do Supabase) ---
if st.checkbox("Ver meu histórico"):
    response = supabase.table("refeicoes").select("*").execute()
    st.table(response.data)
