import streamlit as st
import os
import re
from groq import Groq
from moviepy.video.io.VideoFileClip import VideoFileClip

# --- SETUP E ESTILIZAÇÃO (MUDOU O TÍTULO) ---
st.set_page_config(page_title="VIDIOM AI | MVP Funcional", layout="wide")
st.markdown("""<style>.stTextArea textarea { background-color: #1e2129; color: white; }.stButton>button { background-color: #ff4b4b; color: white; }.stVideo { width: 100%; border-radius: 5px; margin-bottom: 20px; }</style>""", unsafe_allow_html=True)

# Segurança
if "GROQ_API_KEY" not in st.secrets:
    st.error("Configure a 'GROQ_API_KEY' nas Secrets!")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- FUNÇÃO DE EDIÇÃO (MUDOU, MAIS LEVE) ---
def fazer_corte_ia(video_path, start, end):
    output_path = "corte_viral.mp4"
    try:
        # Força o MoviePy a ler o arquivo de forma "preguiçosa" para salvar memória
        with VideoFileClip(video_path, audio=True).subclip(start, end) as corte:
            # Reduz a qualidade para 720p (vertical) para garantir o download no grátis
            st.write("Processando o vídeo para download...")
            # codec libx264 é universalmente aceito no TikTok/Reels
            corte.write_videofile(output_path, codec="libx264", audio_codec="aac", temp_audiofile='temp-audio.m4a', remove_temp=True, logger=None, threads=1)
        return output_path
    except Exception as e:
        st.error(f"Erro técnico no corte: {e}")
        return None

# --- INTERFACE ---
st.title("🤖 VIDIOM AI - Validador de Negócio")
st.markdown("### 1️⃣ Suba o seu vídeo curto (MP4/MOV)")
st.info("No plano grátis, vídeos menores que 3 minutos funcionam melhor.")
video_file = st.file_uploader("", type=["mp4", "mov"])

if video_file:
    # Salva temporariamente
    with open("temp_input.mp4", "wb") as f: f.write(video_file.getbuffer())
    
    # Validação de duração (Crucial para o grátis)
    with VideoFileClip("temp_input.mp4") as v:
        duracao_real = int(v.duration)
    
    if duracao_real > 180: # Limite de 3 minutos no MVP grátis
        st.error("Desculpe, no plano grátis do MVP, vídeos de até 3 minutos são processados. Tente um arquivo menor.")
        st.stop()
        
    st.markdown("### 2️⃣ O que acontece no vídeo?")
    contexto = st.text_area(label="Descreva o vídeo:", placeholder="Ex: Silver Cop vai comprar a Porsche do Balestrin e fala sobre o motor.", height=150)

    if st.button("✨ GERAR VÍDEO COMPLETO"):
        if not contexto:
            st.warning("A IA precisa do contexto!")
        else:
            with st.status("IA Analisando e Processando...", expanded=True) as status:
                # Prompt SUPER simplificado (NÃO TIRA A CAPA)
                prompt = f"""
                Duração total: {duracao_real}s.
                Contexto: "{contexto}".
                
                Com base na descrição, escolha o melhor intervalo de até 30 segundos.
                Responda APENAS: INICIO:X, FIM:Y.
                Onde X e Y são números inteiros.
                Não escreva mais nada.
                """
                
                # Chamada da Groq (Llama 3.3)
                try:
                    chat = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model="llama-3.3-70b-versatile")
                    resposta = chat.choices[0].message.content
                    
                    st.write(f"🧠 IA Definiu o Corte: {resposta}")
                    
                    # Regex mais robusto para pegar os números
                    start_ia = int(re.search(r"INICIO:(\d+)", resposta).group(1))
                    end_ia = int(re.search(r"FIM:(\d+)", resposta).group(1))
                    
                    # Chama o processador de corte puro
                    video_pronto = fazer_corte_ia("temp_input.mp4", start_ia, end_ia)
                    
                    if video_pronto:
                        status.update(label="O corte está pronto para download!", state="complete")
                        with open(video_pronto, "rb") as f:
                            st.video(f)
                            st.download_button("📥 BAIXAR CORTE VIRAL", f, file_name="vidiom_ia_corte.mp4")
                        
                        # Limpeza dos arquivos para libertar RAM do servidor
                        if os.path.exists("temp_input.mp4"): os.remove("temp_input.mp4")
                        if os.path.exists("corte_viral.mp4"): os.remove("corte_viral.mp4")

                except Exception as e:
                    # Melhoria no feedback de erro para o usuário
                    if "timed out" in str(e) or "overload" in str(e):
                        st.error("A IA demorou demais para pensar devido à alta demanda do servidor gratuito. Tente novamente mais tarde.")
                    else:
                        st.error(f"Erro na análise: {e}. A IA se confundiu na resposta ou o tempo expirou. Tente novamente.")
