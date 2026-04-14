from tavily import TavilyClient
import streamlit as st

# O jeito seguro: pegando a chave dos Secrets do Streamlit
tavily = TavilyClient(api_key=st.secrets["TAVILY_API_KEY"])

def buscar_noticia_automotiva(comando_usuario):
    # Faz a busca real
    response = tavily.search(
        query=f"notícias automotivas recentes: {comando_usuario}",
        search_depth="advanced",
        max_results=1,
        include_images=True  # Isso aqui é o que vai trazer a foto do carro!
    )
    
    # Organiza o resultado
    if response['results']:
        resultado = response['results'][0]
        imagem = response.get('images', [None])[0]
        
        return {
            "titulo": resultado['title'],
            "link": resultado['url'],
            "conteudo": resultado['content'],
            "foto": imagem if imagem else "https://images.unsplash.com/photo-1503376780353-7e6692767b70"
        }
    return None

# --- Exemplo de como usar no seu botão ---
if st.button("GERAR POST AGORA 🚀"):
    dados_reais = buscar_noticia_automotiva(query)
    if dados_reais:
        st.write(f"Notícia encontrada: {dados_reais['titulo']}")
        # Aqui você passaria dados_reais['foto'] para a função que cria o card
