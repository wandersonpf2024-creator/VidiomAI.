import streamlit as st
from supabase import create_client
import openai
import base64

# --- 1. CONEXÃO COM SEUS DADOS (Substitua pelos seus) ---
# Pegue esses dados no menu 'Settings' > 'API' do seu Supabase
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)
openai.api_key = st.secrets["OPENAI_API_KEY"]

# --- 2. DESIGN LANDING PAGE (Estilo Profissional Dark) ---
st.set_page_config(page_title="NutriScan IA", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at top, #121212 0%, #050505 100%);
        color: white;
    }
    .hero-title {
        font-size: 50px; font-weight: 800; text-align: center;
        margin-top: 40px; background: linear-gradient(to right, #fff, #6366f1);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .input-container {
        background: rgba(255,255,255,0.03); border: 1px solid #222;
        padding: 30px; border-radius: 20px; max-width: 800px; margin: 30px auto;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. LÓGICA DE IA ---
def analisar_comida(foto_bytes):
    base64_image = base64.b64encode(foto_bytes).decode('utf-8')
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": [
            {"type": "text", "text": "Retorne APENAS o nome do prato, calorias e macros. Exemplo: Picanha | 500kcal | P:50g, C:0g, G:30g"},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
        ]}]
    )
    return response.choices[0].message.content

# --- 4. INTERFACE ---
st.markdown('<h1 class="hero-title">NutriScan IA</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#888;">Tire uma foto e descubra o que você está comendo instantaneamente.</p>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    
    foto = st.camera_input("📸 Aponte para o prato")
    
    if foto:
        if st.button("ANALISAR E SALVAR NO HISTÓRICO 🚀", use_container_width=True, type="primary"):
            with st.spinner("IA analisando seu prato..."):
                # Analisa com GPT-4o
                resultado = analisar_comida(foto.getvalue())
                
                # Separa os dados para o Supabase
                partes = resultado.split('|')
                nome = partes[0].strip()
                cals = partes[1].strip()
                macs = partes[2].strip() if len(partes) > 2 else "N/A"
                
                # SALVA NA TABELA QUE VOCÊ CRIOU
                dados = {
                    "nome_prato": nome,
                    "calorias": cals,
                    "macros": macs
                }
                supabase.table("refeicoes").insert(dados).execute()
                
                st.success(f"Salvo! {nome} identificado.")
                st.info(f"🔥 {cals} | 🥩 {macs}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- 5. VISUALIZAR HISTÓRICO ---
if st.checkbox("Ver meu histórico de refeições"):
    res = supabase.table("refeicoes").select("*").order("created_at", desc=True).execute()
    if res.data:
        st.table(res.data)
