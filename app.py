import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

# --- FUNÇÃO PARA ESCREVER TEXTO NA IMAGEM ---
def criar_card(url_imagem, titulo):
    # Baixa a imagem da notícia
    response = requests.get(url_imagem)
    img = Image.open(BytesIO(response.content))
    
    # Redimensiona para um padrão (ex: Post de Instagram)
    img = img.resize((1080, 1080))
    draw = ImageDraw.Draw(img)
    
    # Adiciona uma camada escura no topo para o texto aparecer
    draw.rectangle([0, 0, 1080, 250], fill=(0, 0, 0, 180))
    
    # Escreve o título (Headline)
    # Nota: Você precisaria de um arquivo de fonte .ttf no seu projeto
    try:
        font = ImageFont.truetype("Arial.ttf", 60)
    except:
        font = ImageFont.load_default()
        
    draw.text((50, 50), titulo, fill="white", font=font)
    
    return img

# --- INTERFACE ---
st.title("🚗 AutoNews AI Poster")

comando = st.text_input("O que você quer postar?", placeholder="noticias de hoje do mundo automotivo")

if st.button("GERAR POST"):
    with st.spinner("Buscando notícias e criando arte..."):
        # 1. Aqui você chamaria uma API de busca (como Tavily)
        # Vamos simular que achamos uma notícia:
        noticia_titulo = "Novo SUV Elétrico bate recorde de vendas em 2026!"
        imagem_url = "https://images.unsplash.com/photo-1503376780353-7e6692767b70" # Exemplo
        
        # 2. IA gera as hashtags
        hashtags = "#automotive #news #future #electriccars"
        
        # 3. Cria o card visual
        card_pronto = criar_card(imagem_url, noticia_titulo)
        
        # 4. Exibe no App
        st.image(card_pronto, caption="Pronto para postar!")
        st.write(f"**Legenda sugerida:** {noticia_titulo}")
        st.code(hashtags)
        
        # 5. Botão de Download
        buf = BytesIO()
        card_pronto.save(buf, format="PNG")
        st.download_button("📥 Baixar Imagem", buf.getvalue(), "post_automotivo.png", "image/png")
