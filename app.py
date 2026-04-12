import streamlit as st
from groq import Groq
import openai  # Para a imagem
import requests

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="VIDIOM AI | Groq + Image", layout="wide")

# Inicialize as APIs (Coloque suas chaves aqui ou no secrets)
client_groq = Groq(api_key="SUA_CHAVE_GROQ")
openai.api_key = "SUA_CHAVE_OPENAI"

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    .neon-box {
        background: #111; border: 1px solid #222;
        border-radius: 15px; padding: 25px;
    }
    .stats-card {
        border-left: 4px solid #6366f1;
        background: rgba(99, 102, 241, 0.05);
        padding: 15px; border-radius: 8px; margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# --- INTERFACE ---
st.markdown("<h1 style='text-align:center;'>🍎 NutriIA + Gerador de Imagem</h1>", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="neon-box">', unsafe_allow_html=True)
    prato = st.text_input("O que você quer comer hoje?", placeholder="Ex: Bife de Picanha com batatas")
    
    if st.button("GERAR ANALISE E IMAGEM 🚀", use_container_width=True, type="primary"):
        col1, col2 = st.columns(2)
        
        with col1:
            with st.spinner("Groq calculando nutrientes..."):
                # 1. GROQ GERA OS DADOS (Rápido demais!)
                chat_completion = client_groq.chat.completions.create(
                    messages=[{"role": "user", "content": f"Calcule calorias, proteina, carbo e gordura para: {prato}. Responda apenas os números separados por vírgula."}],
                    model="llama3-8b-8192",
                )
                dados = chat_completion.choices[0].message.content
                st.subheader(f"🍴 {prato}")
                st.markdown(f'<div class="stats-card">🔥 <b>{dados} kcal</b></div>', unsafe_allow_html=True)
        
        with col2:
            with st.spinner("IA Gerando Imagem 4K..."):
                # 2. OPENAI GERA A IMAGEM
                response = openai.images.generate(
                    model="dall-e-3",
                    prompt=f"Fotografia gastronômica profissional, 4k, ultra realista, iluminação de estúdio de: {prato}",
                    n=1, size="1024x1024"
                )
                img_url = response.data[0].url
                st.image(img_url, caption="Resultado Final em 4K")
                
    st.markdown('</div>', unsafe_allow_html=True)
