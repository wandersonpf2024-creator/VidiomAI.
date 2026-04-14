from tavily import TavilyClient

# No seu bloco de API SETUP, adicione:
tavily = TavilyClient(api_key=st.secrets["TAVILY_API_KEY"])

def buscar_noticias_reais(tema):
    try:
        # Busca notícias recentes do dia
        # search_depth="advanced" traz resultados mais precisos
        busca = tavily.search(
            query=f"notícias automotivas de hoje {tema}",
            search_depth="advanced",
            max_results=1,
            include_images=True # ESSENCIAL para pegar a foto da notícia
        )
        
        if busca['results']:
            noticia = busca['results'][0]
            link_imagem = busca.get('images', [None])[0] # Pega a primeira imagem da busca
            
            # Se a busca não retornar imagem, usamos uma reserva (fallback)
            if not link_imagem:
                link_imagem = "https://images.unsplash.com/photo-1503376780353-7e6692767b70"
                
            return {
                "titulo": noticia['title'],
                "resumo": noticia['content'],
                "url": noticia['url'],
                "imagem": link_imagem
            }
    except Exception as e:
        st.error(f"Erro na busca: {e}")
        return None

# --- DENTRO DO SEU BOTÃO DE GERAR ---
if st.button("GERAR POST REAL 🚀"):
    dados = buscar_noticias_reais(query)
    
    if dados:
        # Agora mandamos o CONTEÚDO REAL da notícia para o Groq
        prompt_ia = f"""
        Com base nesta notícia: {dados['resumo']}
        Gere um título curto (máx 50 caracteres) para colocar na imagem e 5 hashtags.
        """
        # ... resto do código para gerar o card usando dados['imagem']
