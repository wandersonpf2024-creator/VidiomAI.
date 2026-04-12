import streamlit as st
from groq import Groq
import json

# 1. Configuração da Página
st.set_page_config(page_title="Health Chef AI 4K", page_icon="🥗", layout="wide")

# Estilo Dark Premium
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { background-color: #28a745; color: white; font-weight: bold; border-radius: 10px; height: 3em; }
    .card-nutri {
        background-color: #1c1f26;
        padding: 25px;
        border-radius: 20px;
        border: 1px solid #28a745;
        margin-bottom: 20px;
    }
    h1, h2, h3 { color: #28a745; }
    </style>
    """, unsafe_allow_html=True)

# 2. Inicialização Groq
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Erro: Verifique sua chave da Groq nos Secrets.")
    st.stop()

def gerar_receita(pergunta):
    prompt = f"""
    Crie uma receita saudável para: "{pergunta}".
    Retorne APENAS um JSON:
    {{
        "nome": "Nome do Prato",
        "calorias": "X kcal",
        "ingredientes": ["item 1", "item 2"],
        "preparo": "passo a passo curto",
        "macros": {{"p": "g", "c": "g", "g": "g"}},
        "keyword": "termo em ingles para busca de imagem"
    }}
    """
    completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile",
        response_format={"type": "json_object"}
    )
    return json.loads(completion.choices[0].message.content)

# 3. Interface
st.title("🥗 Health Chef AI: Receitas & Calorias")

pergunta = st.text_input("O que você quer comer?", placeholder="Ex: Panqueca de aveia com banana")

if st.button("GERAR RECEITA E IMAGEM"):
    if pergunta:
        with st.spinner("🍳 Calculando e buscando imagem..."):
            try:
                dados = gerar_receita(pergunta)
                
                st.divider()
                col_img, col_info = st.columns([1, 1])
                
                with col_img:
                    # Usa uma imagem real de alta qualidade baseada no prato
                    url_imagem = f"https://source.unsplash.com/800x800/?food,{dados['keyword']}"
                    st.image(url_imagem, caption=dados['nome'], use_container_width=True)
                
                with col_info:
                    st.header(f"🍴 {dados['nome']}")
                    st.markdown(f"""
                        <div class="card-nutri">
                            <h2 style='margin:0;'>🔥 {dados['calorias']}</h2>
                            <p>Calorias totais</p>
                            <hr>
                            <p>💪 <b>Proteínas:</b> {dados['macros']['p']}</p>
                            <p>🍞 <b>Carbos:</b> {dados['macros']['c']}</p>
                            <p>🥑 <b>Gorduras:</b> {dados['macros']['g']}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.subheader("🛒 Ingredientes")
                    for ing in dados['ingredientes']:
                        st.write(f"- {ing}")
                
                st.write("### 👨‍🍳 Modo de Preparo")
                st.info(dados['preparo'])
                
            except Exception as e:
                st.error(f"Erro: {e}")
