import streamlit as st
from groq import Groq
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import json

# 1. Configuração da Página e Estilo
st.set_page_config(page_title="News2Post AI", page_icon="🚀", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #ff4b4b; color: white; }
    </style>
    """, unsafe_allow_html=True)

# 2. Inicialização do Cliente Groq
# Tenta pegar a chave dos Secrets do Streamlit
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("Erro: API Key da Groq não encontrada nos Secrets!")
    st.stop()

# 3. Função para processar o texto com Llama 3 (Groq)
def processar_conteudo_ia(tema_ou_link):
    prompt = f"""
    Você é um gerente de redes sociais de alto nível. 
    Analise o seguinte tema ou notícia: "{tema_ou_link}"
    Gere um post para Facebook/Instagram seguindo EXATAMENTE este formato JSON:
    {{
        "headline": "Uma frase curta, impactante e viral para ir escrita na imagem (máx 45 caracteres)",
        "legenda": "Um texto engajador com emojis e que termine com uma pergunta",
        "hashtags": "#tag1 #tag2 #tag3"
    }}
    Responda APENAS o JSON, sem textos adicionais.
    """
    
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama3-70b-8192",
        response_format={"type": "json_object"}
    )
    return json.loads(chat_completion.choices[0].message.content)

# 4. Função para gerar a imagem (O Motor de Design)
def gerar_imagem_post(headline):
    # Criar uma imagem quadrada 1080x1080 (Padrão Insta/FB)
    # Usando um degradê simples ou cor sólida de impacto (Vermelho Escuro)
    width, height = 1080, 1080
    image = Image.new('RGB', (width, height), color='#8B0000')
    draw = ImageDraw.Draw(image)
    
    # Tentativa de carregar fonte. Se falhar, usa a padrão.
    try:
        # No Streamlit Cloud, fontes .ttf precisam estar na pasta ou usar caminhos do sistema
        font = ImageFont.load_default() 
        # Para algo profissional, você subiria um arquivo 'font.ttf' pro GitHub e usaria:
        # font = ImageFont.truetype("font.ttf", 80)
    except:
        font = ImageFont.load_default()

    # Quebrar o texto para caber na imagem
    import textwrap
    linhas = textwrap.wrap(headline, width=20)
    
    y_text = 400
    for linha in linhas:
        # Desenha o texto centralizado (ajuste manual básico)
        draw.text((150, y_text), linha, fill="white", font=font)
        y_text += 100

    return image

# 5. Interface do Usuário (UI)
st.title("🚀 News2Post AI")
st.write("Insira um tema ou link de notícia para gerar seu post instantâneo.")

entrada = st.text_input("Notícia ou Assunto:", placeholder="Ex: Nova atualização do Facebook 2026")

if st.button("GERAR POST AGORA"):
    if entrada:
        with st.spinner("🤖 IA processando e desenhando..."):
            try:
                # Processamento
                resultado = processar_conteudo_ia(entrada)
                img_final = gerar_imagem_post(resultado['headline'])
                
                # Exibição
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.image(img_final, caption="Imagem Gerada", use_column_width=True)
                
                with col2:
                    st.subheader("Legenda:")
                    st.write(resultado['legenda'])
                    st.info(resultado['hashtags'])
                
                # Botão de Download
                buf = BytesIO()
                img_final.save(buf, format="PNG")
                byte_im = buf.getvalue()
                st.download_button(label="📥 Baixar Imagem para Postar", data=byte_im, file_name="post_ia.png", mime="image/png")
                
            except Exception as e:
                st.error(f"Ocorreu um erro: {e}")
    else:
        st.warning("Por favor, digite algo antes de gerar.")

st.markdown("---")
st.caption("Desenvolvido para escala global - Powered by Groq & Streamlit")
