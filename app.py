import streamlit as st
from groq import Groq
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import json
import textwrap

# 1. Configuração da Página
st.set_page_config(page_title="News2Post AI", page_icon="🚀", layout="centered")

# Estilização CSS para deixar o app com visual moderno
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #ff4b4b; color: white; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. Inicialização do Cliente Groq
try:
    # Busca a chave nos Secrets do Streamlit ou localmente
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except Exception:
    st.error("ERRO: API Key da Groq não encontrada. Configure nos 'Secrets' do Streamlit.")
    st.stop()

# 3. Função para processar o conteúdo com a IA da Groq
def processar_conteudo_ia(entrada_usuario):
    prompt = f"""
    Você é um gerente de redes sociais especializado em viralização.
    Analise o seguinte conteúdo ou link: "{entrada_usuario}"
    
    Gere um post para Facebook seguindo EXATAMENTE este formato JSON:
    {{
        "headline": "Uma frase curta e agressiva para a imagem (máx 40 caracteres)",
        "legenda": "Um texto curto, informativo e com emojis para a descrição",
        "hashtags": "#noticias #carros #tech"
    }}
    Responda APENAS o objeto JSON.
    """
    
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile",
        response_format={"type": "json_object"}
    )
    
    return json.loads(chat_completion.choices[0].message.content)

# 4. Função para desenhar a imagem do post
def gerar_imagem_post(headline):
    width, height = 1080, 1080
    image = Image.new('RGB', (width, height), color='#A50000')
    draw = ImageDraw.Draw(image)
    
    try:
        # Tenta carregar a fonte que você subiu (mude o nome se necessário)
        # Se não tiver o arquivo ainda, ele vai para o except
        font = ImageFont.truetype("Montserrat-Bold.ttf", 90) 
    except:
        # Se falhar, ele usa a padrão mas tenta aumentar (o que é limitado)
        font = ImageFont.load_default()

    # Quebra o texto mais curto para as letras ficarem grandes
    linhas = textwrap.wrap(headline.upper(), width=12)
    
    # Calcula a altura total do bloco de texto para centralizar verticalmente
    y_text = 540 - (len(linhas) * 50) 
    
    for linha in linhas:
        # Centraliza horizontalmente (ajuste aproximado para 1080px)
        draw.text((100, y_text), linha, fill="white", font=font)
        y_text += 110 # Espaçamento entre linhas

    return image

# 5. Interface do Usuário (Frontend)
st.title("🚀 Gerador de Post Viral")
st.write("Insira um tema ou link e a IA criará a imagem e a legenda para você.")

# Campo de entrada
entrada = st.text_input("Cole o link da notícia ou o tema aqui:", placeholder="Ex: Novo carro elétrico da Toyota faz 2000km")

if st.button("GERAR POST COMPLETO"):
    if entrada:
        with st.spinner("🤖 A IA está lendo a notícia e desenhando o post..."):
            try:
                # Chama a Groq
                dados_post = processar_conteudo_ia(entrada)
                
                # Gera a Imagem
                imagem_pronta = gerar_imagem_post(dados_post['headline'])
                
                # Exibe os resultados na tela
                st.divider()
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.image(imagem_pronta, caption="Preview da Imagem", use_container_width=True)
                
                with col2:
                    st.subheader("📝 Legenda Gerada:")
                    st.write(dados_post['legenda'])
                    st.write(f"**{dados_post['hashtags']}**")
                
                # Preparar download
                img_buffer = BytesIO()
                imagem_pronta.save(img_buffer, format="PNG")
                byte_im = img_buffer.getvalue()
                
                st.download_button(
                    label="📥 Baixar Imagem para o Facebook",
                    data=byte_im,
                    file_name="post_viral_ia.png",
                    mime="image/png"
                )
                
                st.success("✅ Post pronto para publicação!")

            except Exception as e:
                st.error(f"Ocorreu um erro no processamento: {e}")
    else:
        st.warning("Por favor, digite um tema ou cole um link.")

st.markdown("---")
st.caption("Ferramenta Pro para Donos de Páginas - Versão 1.0")
