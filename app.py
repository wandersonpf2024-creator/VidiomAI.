import streamlit as st
from groq import Groq
from PIL import Image, ImageDraw, ImageFont

# Configuração da Groq (Pegue a chave nos Secrets do Streamlit)
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def processar_ia_groq(texto_noticia):
    # Usando o modelo Llama 3 da Groq (que é ultra rápido)
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {
                "role": "system", 
                "content": "Você é um especialista em Facebook. Retorne um JSON com: 'headline' (curta e impactante), 'legenda' e 'tags'."
            },
            {
                "role": "user", 
                "content": f"Transforme isso em post: {texto_noticia}"
            }
        ],
        response_format={"type": "json_object"} # Isso garante que venha certinho para o código
    )
    return completion.choices[0].message.content

# O restante da função de gerar imagem e interface continua igual!
