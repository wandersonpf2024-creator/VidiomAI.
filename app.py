import streamlit as st
from supabase import create_client
from groq import Groq
import base64

# --- 1. INICIALIZAÇÃO SEGURA ---
try:
    # Busca as chaves nos Secrets do Streamlit Cloud
    GROQ_KEY = st.secrets["GROQ_API_KEY"]
    S_URL = st.secrets["SUPABASE_URL"]
    S_KEY = st.secrets["SUPABASE_KEY"]
    
    client = Groq(api_key=GROQ_KEY)
    supabase = create_client(S_URL, S_KEY)
except Exception as e:
    st.error("Erro nos Secrets: Verifique se as chaves GROQ_API_KEY, SUPABASE_URL e SUPABASE_KEY estão no painel do Streamlit.")
    st.stop()

# --- 2. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="VidiomAI Nutri", layout="centered")
st.markdown("<style>.stApp {background-color: #050505; color: white;}</style>", unsafe_allow_html=True)

st.title("📸 NutriScan Groq")

# --- 3. LÓGICA DE ANÁLISE ---
def analisar_prato(foto_bytes):
    img_b64 = base64.b64encode(foto_bytes).decode('utf-8')
    
    # Usando o modelo de visão da Groq
    chat_completion = client.chat.completions.create(
        model="llama-3.2-11b-vision-preview",
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": "Responda apenas: Nome do prato | Calorias | Macros. Ex: Frango com Arroz | 450 kcal | P:30g C:40g G:10g"},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}}
            ]
        }]
    )
    return chat_completion.choices[0].message.content

# --- 4. INTERFACE E AÇÃO ---
foto = st.camera_input("Tire uma foto da sua comida")

if foto:
    if st.button("ANALISAR AGORA 🚀", type="primary", use_container_width=True):
        with st.spinner("Analisando com Groq..."):
            try:
                # 1. Chama a IA
                resultado = analisar_prato(foto.getvalue())
                st.subheader("Resultado da IA:")
                st.info(resultado)

                # 2. Tenta separar os dados (Nome | Calorias | Macros)
                partes = resultado.split('|')
                nome = partes[0].strip() if len(partes) > 0 else "Prato Desconhecido"
                cals = partes[1].strip() if len(partes) > 1 else "Não informado"
                macs = partes[2].strip() if len(partes) > 2 else "Não informado"

                # 3. Tenta salvar no Supabase
                dados = {"nome_prato": nome, "calorias": cals, "macros": macs}
                supabase.table("refeicoes").insert(dados).execute()
                st.success("Dados salvos no Supabase com sucesso!")

            except Exception as e:
                st.error(f"Ocorreu um erro: {e}")

# --- 5. HISTÓRICO ---
if st.checkbox("Ver meu histórico salvo"):
    try:
        res = supabase.table("refeicoes").select("*").order("created_at", desc=True).execute()
        st.write(res.data)
    except:
        st.warning("Ainda não existem dados na tabela 'refeicoes'.")
