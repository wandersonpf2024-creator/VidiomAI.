import streamlit as st
import os
import re
from groq import Groq
from moviepy.video.io.VideoFileClip import VideoFileClip

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="VIDIOM AI | PRO", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: white; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #ff4b4b; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO DE PROCESSAMENTO ---
def processar_corte(video_path, start, end):
    output_path = "corte_final.mp4"
    try:
        with VideoFileClip(video_path) as video:
            # Garante que o corte não exceda a duração do vídeo
            duration = video.duration
            fim_real = min(end, duration)
            
            # Realiza o corte
            corte = video.subclip(start, fim_real)
            # Renderiza o arquivo final
            corte.write_videofile(output_path, codec="libx264", audio_codec="aac", temp_audiofile='temp-audio.m4a', remove_temp=True)
        return output_path
    except Exception as e:
        st.error(f"Erro na edição: {e}")
        return None

# --- INTERFACE ---
st.title("🎬 VIDIOM AI - Editor de Cortes Automático")
st.info("Suba o vídeo e a IA cuidará do melhor momento para você.")

# 1. Configuração da API Key (Secret)
if "GROQ_API_KEY" not in st.secrets:
    st.error("ERRO: Configure a 'GROQ_API_KEY' nas Secrets do Streamlit!")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 2. Upload do Arquivo
video_file = st.file_uploader("📂 Escolha um vídeo (MP4)", type=["mp4", "mov"])

if video_file is not None:
    # Salva o arquivo temporariamente no servidor
    with open("video_input.mp4", "wb") as f:
        f.write(video_file.getbuffer())
    
    st.video("video_input.mp4")
    
    if st.button("🚀 ANALISAR E GERAR CORTE"):
        with st.status("IA Analisando conteúdo...", expanded=True) as status:
            
            # Aqui simulamos a análise da IA para o tempo (ou você pode integrar transcrição depois)
            # Para o corte sair agora, vamos pedir para a IA decidir o tempo baseada no nome do arquivo
            prompt = f"Sugira um tempo de início e fim em segundos para um corte de 30 segundos de um vídeo chamado: {video_file.name}. Responda apenas: INICIO:X, FIM:Y"
            
            try:
                chat = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama-3.3-70b-versatile"
                )
                res_ia = chat.choices[0].message.content
                
                # Extrai os tempos usando Regex
                start_time = int(re.search(r"INICIO:(\d+)", res_ia).group(1))
                end_time = int(re.search(r"FIM:(\d+)", res_ia).group(1))
                
                st.write(f"✨ IA Sugeriu: Início em {start_time}s e Fim em {end_time}s")
                
                # Executa o corte real
                resultado = processar_corte("video_input.mp4", start_time, end_time)
                
                if resultado:
                    status.update(label="Corte Concluído!", state="complete")
                    st.subheader("✅ Seu corte está pronto!")
                    
                    with open(resultado, "rb") as f:
                        st.video(f)
                        st.download_button(
                            label="📥 BAIXAR VÍDEO AGORA",
                            data=f,
                            file_name="meu_corte_viral.mp4",
                            mime="video/mp4"
                        )
                    # Limpeza de arquivos
                    os.remove("video_input.mp4")
            
            except Exception as e:
                st.error(f"Falha no processo: {e}")

# --- RODAPÉ ---
st.markdown("---")
st.caption("Vidiom AI - Transformando vídeos longos em virais.")
