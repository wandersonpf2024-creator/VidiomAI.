import streamlit as st
import urllib.parse
import random

# Tenta importar o que falta
try:
    from supabase import create_client, Client
    import google.generativeai as genai
except:
    st.error("Instalando dependências... Aguarde um instante.")

st.set_page_config(page_title="Vidiom AI", layout="wide")

# Interface Simples para Teste de Imagem
st.title("🎨 Gerador de Imagem Ultra")

img_desc = st.text_input("Descreve a tua imagem (ex: Neon city)")

if st.button("🚀 Gerar Agora"):
    if img_desc:
        with st.spinner("A criar..."):
            # Criamos o link da imagem
            seed = random.randint(1, 99999)
            prompt_limpo = urllib.parse.quote(img_desc)
            url_final = f"https://image.pollinations.ai/prompt/{prompt_limpo}?width=1024&height=1024&nologo=true&seed={seed}"
            
            # Comando forçado para exibir
            st.markdown(f"### Resultado:")
            st.image(url_final, use_container_width=True)
            st.write(f"Link da imagem: {url_final}")
    else:
        st.warning("Escreve algo antes de clicar.")
