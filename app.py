### `modules/scraper.py`

* Usa `newspaper3k` para extrair: título, texto principal, lista de imagens

* Fallback com `BeautifulSoup` + `requests` para sites que bloqueiam newspaper3k

* Filtra imagens por tamanho mínimo (evita logos/ícones)

* Retorna: `{ title, summary, images: [url, ...] }`

### 2. `modules/ai_generator.py`

* Conecta ao Groq com modelo `llama-3.3-70b-versatile`

* **Prompt 1**: gera texto chamativo curto (max 8 palavras) para overlay na imagem

* **Prompt 2**: gera 3 legendas virais por rede social:

  * Instagram: com emojis, hashtags, tom engajador

  * TikTok: curto, direto, com call-to-action

  * Facebook: mais descritivo, compartilhável

### 3. `modules/image_editor.py`

* Baixa a imagem selecionada com `requests`

* Com `Pillow`:

  * Adiciona gradiente escuro na parte inferior (legibilidade)

  * Escreve texto chamativo em fonte bold (BebasNeue ou Impact)

  * Adiciona borda/sombra no texto

  * Redimensiona para 1080x1080 (quadrado, padrão social)

* Retorna imagem como `bytes` (PNG)

### 4. `modules/supabase_client.py`

* Upload da imagem editada no **Supabase Storage** (bucket `news-images`)

* Salva no **Supabase DB** (tabela `history`):

  * `url_origem`, `titulo`, `url_imagem_editada`, `legendas_json`, `criado_em`

### 5. `app.py` — UI Streamlit

* Campo de input para URL da notícia

* Seletor de imagem extraída (thumbnail preview)

* Botão "Gerar conteúdo viral"

* Exibe: imagem editada + download button

* Abas para cada rede: Instagram | TikTok | Facebook com as legendas

* Sidebar: histórico das últimas edições (do Supabase)
