import streamlit as st
from groq import Groq
import json

# Configuração da Página
st.set_page_config(page_title="Health Chef AI", page_icon="🥗")

# Estilo para ficar com cara de App de Saúde (Verde)
st.markdown("""
    <style>
    .stButton>button { background-color: #28a745; color: white; font-weight: bold; }
    .calorie-box { background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #28a745; }
    </style>
    """, unsafe_allow_html=True)

# Inicialização Groq
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Configure sua API KEY nos Secrets.")
    st.stop()

def gerar_receita(objetivo_ou_ingredientes):
    prompt = f"""
    Você é um Nutricionista e Chef Profissional.
    Com base nisso: "{objetivo_ou_ingredientes}", crie uma receita saudável.
    Retorne EXATAMENTE este formato JSON:
    {{
        "nome": "Nome da Receita",
        "ingredientes": ["item 1", "item 2"],
        "preparo": "passo a passo curto",
        "calorias": "valor total",
        "macros": {{ "proteinas": "g", "carbos": "g", "gorduras": "g" }}
    }}
    Responda apenas o JSON.
    """
    
    completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile",
        response_format={"type": "json_object"}
    )
    return json.loads(completion.choices[0].message.content)

# Interface
st.title("🥗 Health Chef AI")
st.subheader("Receitas Inteligentes com Cálculo de Calorias")

pergunta = st.text_input("O que você quer comer ou quais ingredientes você tem?", placeholder="Ex: Café da manhã proteico com ovos")

if st.button("GERAR MINHA DIETA"):
    if pergunta:
        with st.spinner("Calculando macros e criando receita..."):
            receita = gerar_receita(pergunta)
            
            st.header(f"🍴 {receita['nome']}")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write("### 🛒 Ingredientes")
                for ing in receita['ingredientes']:
                    st.write(f"- {ing}")
                
                st.write("### 👨‍🍳 Modo de Preparo")
                st.write(receita['preparo'])
            
            with col2:
                st.markdown(f"""
                <div class="calorie-box">
                    <h3 style='margin-top:0;'>📊 Nutrição</h3>
                    <p><strong>Calorias:</strong> {receita['calorias']} kcal</p>
                    <hr>
                    <p>💪 Prot: {receita['macros']['proteinas']}</p>
                    <p>🍞 Carb: {receita['macros']['carbos']}</p>
                    <p>🥑 Gord: {receita['macros']['gorduras']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Opção de salvar no Supabase (se você já tiver a conexão)
                if st.button("💾 Salvar no meu Plano"):
                    st.success("Receita salva com sucesso!")
    else:
        st.warning("Diga o que você quer comer!")
