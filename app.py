with tab2:
        st.subheader("🎨 Gerador de Arte Visual")
        img_desc = st.text_input("O que você quer criar?", placeholder="Ex: Futuristic city neon lights")
        
        col1, col2 = st.columns(2)
        with col1:
            gerar_ia = st.button("🚀 Gerar com IA")
        with col2:
            gerar_foto = st.button("📸 Buscar Foto Real")

        if gerar_ia or gerar_foto:
            if img_desc:
                with st.spinner("Processando imagem..."):
                    # Limpa o texto para o link não quebrar
                    prompt_formatado = img_desc.replace(" ", ",") 
                    
                    if gerar_ia:
                        # Usando um link mais simples e direto
                        url = f"https://image.pollinations.ai/prompt/{prompt_formatado}"
                    else:
                        # Opção de foto real caso a IA falhe
                        url = f"https://source.unsplash.com/featured/?{prompt_formatado}"
                    
                    # Exibe a imagem de forma garantida usando HTML
                    st.markdown(f'<img src="{url}" width="100%" style="border-radius:15px; border: 2px solid #00f2fe;">', unsafe_allow_html=True)
                    st.write(f"Link para download: [Clique aqui]({url})")
            else:
                st.error("Escreva algo no campo de texto!")
