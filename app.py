import streamlit as st
from supabase import create_client
from groq import Groq
import base64

# --- CONEXÃO COM SEUS DADOS ---
# Agora buscando GROQ_API_KEY
client = Groq(api_key=st.secrets["GROQ_API_KEY"])
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

# --- DESIGN DARK PRO ---
st.set_page_config(page_title="VidiomAI | Nutri", layout="wide")
st.markdown("<style>.stApp {background-color: #050505; color: white;}</style>", unsafe_allow_html=True)

# --- FUNÇÃO DE VISÃO COM GROQ ---
def analisar_com_groq(foto_bytes):
    base64_image = base64.b64encode(foto_bytes).decode('utf-8')
    
    # Usando o modelo de visão da Groq (llama-3.2-11b-vision-preview)
    completion = client.chat.completions.create(
        model="llama-3.2-11b-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Analise a imagem e retorne apenas: Nome do prato | Calorias | Macros (P, C, G)"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]
            }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=False,
        stop=None,
    )
    return completion.choices[0].message.content

# --- INTERFACE ---
st.title("📸 Scanner Nutricional (Groq Edition)")

foto = st.camera_input("Tire foto do seu prato")

if foto:
    if st.button("ANALISAR COM GROQ 🚀", type="primary", use_container_width=True):
        with st.spinner("A Groq está processando a imagem em milissegundos..."):
            try:
                resultado = analisar_com_groq(foto.getvalue())
                
                # Tratamento simples do texto para o Supabase
                partes = resultado.split('|')
                nome = partes[0].strip() if len(partes) > 0 else "Prato Identificado"
                cals = partes[1].strip() if len(partes) > 1 else "---"
                macs = partes[2].strip() if len(partes) > 2 else "---"

                # SALVA NA TABELA DO SUPABASE
                dados = {
                    "nome_prato": nome,
                    "calorias": cals,
                    "macros": macs
                }
                supabase.table("refeicoes").insert(dados).execute()
                
                st.success("Salvo no histórico!")
                st.subheader(f"🍴 {nome}")
                st.write(f"🔥 {cals} | 🥩 {macs}")
            
            except Exception as e:
                st.error(f"Erro na Groq: {e}")

# Histórico
if st.checkbox("Ver Histórico"):
    res = supabase.table("refeicoes").select("*").order("created_at", desc=True).execute()
    st.table(res.data)
