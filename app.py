import streamlit as st
from tavily import TavilyClient
from groq import Groq
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

# 1. Conexões Seguras
tavily = TavilyClient(api_key=st.secrets["TAVILY_API_KEY"])
groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def processar_post_completo(tema):
    # A. BUSCA REAL
    busca = tavily.search(query=tema, search_depth="advanced", include_images=True, max_results=1)
    if not busca['results']: return None
    
    noticia = busca['results'][0]
    url_img = busca.get('images', ["https://images.unsplash.com/photo-1492144534655-ae79c964c9d7"])[0]

    # B. IA GERA TÍTULO E HASHTAGS
    prompt = f"Crie um título curto e impactante para esta notícia: {noticia['title']}. Retorne apenas o título."
    res = groq_client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}])
    titulo_ia = res.choices[0].message.content

    # C. MONTAGEM DO CARD (PILLOW)
    response = requests.get(url_img)
    img = Image.open(BytesIO(response.content)).convert("RGB").resize((1080, 1080))
    draw = ImageDraw.Draw(img)
    
    # Barra escura e Texto (Headline)
    draw.rectangle([0, 800, 1080, 1080], fill=(0, 0, 0, 170))
    try:
        font = ImageFont.truetype("Arial.ttf", 50) # Certifique-se de ter a fonte ou use padrão
    except:
        font = ImageFont.load_default()
    
    draw.text((50, 880), titulo_ia, fill="white", font=font)
    
    return img, titulo_ia, noticia['url']

# --- Interface Streamlit ---
st.title("🚗 AutoNews Viral Generator")
comando = st.text_input("O que vamos postar hoje?", placeholder="ex: lançamentos da porsche 2026")

if st.button("GERAR CONTEÚDO 🚀"):
    img_final, txt, link = processar_post_completo(comando)
    st.image(img_final)
    st.write(f"🔗 Fonte: {link}")
    
    # Botão de Download
    buf = BytesIO()
    img_final.save(buf, format="PNG")
    st.download_button("📥 Baixar Imagem Pronta", buf.getvalue(), "post.png", "image/png")
