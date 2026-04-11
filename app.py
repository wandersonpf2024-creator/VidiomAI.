def baixar_e_cortar(url, start_time, end_time, output_name="corte_viral.mp4"):
    # CONFIGURAÇÃO ANTI-BOT
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': 'video_original.mp4',
        'quiet': True,
        'no_warnings': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'referer': 'https://www.google.com/',
        'nocheckcertificate': True
    }
    
    with st.status("Executando Protocolo de Download...", expanded=True) as status:
        try:
            st.write("📡 Conectando ao YouTube...")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            st.write("✂️ Ajustando o corte final...")
            # Usando a importação correta para evitar erros de versão
            from moviepy.video.io.VideoFileClip import VideoFileClip
            
            with VideoFileClip("video_original.mp4") as video:
                # Garante que o corte não passe do tempo total do vídeo
                fim_real = min(end_time, video.duration)
                corte = video.subclip(start_time, fim_real)
                corte.write_videofile(output_name, codec="libx264", audio_codec="aac", temp_audiofile='temp-audio.m4a', remove_temp=True)
            
            # Limpeza
            if os.path.exists("video_original.mp4"):
                os.remove("video_original.mp4")
            status.update(label="Vídeo Processado com Sucesso!", state="complete")
            return output_name
            
        except Exception as e:
            status.update(label="Falha no Processamento", state="error")
            st.error(f"Erro detalhado: {str(e)}")
            return None
