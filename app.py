import streamlit as st
import os
import re
from groq import Groq
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import ImageClip, TextClip
from moviepy.video.compositing.concatenate import concatenate_videoclips
from PIL import Image, ImageDraw, ImageFont

# --- SETUP E ESTILIZAÇÃO ---
st.set_page_config(page_title="VIDIOM AI | MVP", layout="wide")
st.markdown("""<style>.stTextArea textarea { background-color: #1e2129; color: white; }.stButton>button { background-color: #ff4b4b; color: white; }</style>""", unsafe_allow_html=True)

# Segurança
if "GROQ_API_KEY" not in st.secrets:
    st.error("Configure a 'GROQ_API_KEY' nas Secrets!")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- FUNÇÕES TÉCNICAS NÍVEL HARD ---

# 1. Cria a imagem da capa simples
def criar_imagem_capa(titulo_texto):
    width, height = 720, 1280  # Resolução vertical padrão
    image = Image.new("RGB", (width, height), color="#101319") # Fundo Escuro
    draw = ImageDraw.Draw(image)
    
    # Texto grande e centralizado
    margin = 50
    offset = height / 3
    # Nota: No grátis, não temos fontes instaladas, então usamos a padrão.
    # Em produção (pago), você instalaria uma fonte como Arial Black.
    for line in titulo_texto.split('\n'):
        # Simplificação: sem fonte customizada no grátis
        draw.text((margin, offset), line, fill="white")
        offset += 50 # Espaçamento
    
    capa_path = "temp_capa.png"
    image.save(capa_path)
    return capa_path

# 2. Processa o corte E a capa
def processar_vidiom(video_path, start, end, titulo):
    output_final = "vidiom_pronto.mp4"
    capa_img = criar_imagem_capa(titulo)
    
    try:
        # Criamos o clipe de 2 segundos da capa
        with ImageClip(capa_img).set_duration(2) as capa_clip:
            
            # Cortamos o vídeo original
            with VideoFileClip(video_path) as video:
                # Fallback de segurança para 1 minuto (grátis)
                duration = min(video.duration, 60) 
                fim_real = min(end, duration)
                if start >= fim_real: start = 0
                
                # Renderiza o corte em resolução menor para economizar
                st.write("Processando o corte do vídeo...")
                with video.subclip(start, fim_real).resize(height=720) as corte:
                    
                    # Concatena (capa de 2s + corte de 30s)
                    st.write("Concatenando a capa ao vídeo...")
                    vidiom_final = concatenate_videoclips([capa_clip, corte], method="compose")
                    
                    # Salva o arquivo final
                    vidiom_final.write_videofile(output_final, codec="libx264", audio_codec="aac", temp_audiofile='temp-audio.m4a', remove_temp=True, logger=None)
        
        return output_final
        
    except Exception as e:
        st.error(f"Erro na edição: {e}")
        return None
    finally:
        # Limpeza agressiva para economizar memória
        if os.path.exists("temp_capa.png"): os.remove("temp_capa.png")

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
    contexto = st.text_area(label="Descreva o vídeo:", placeholder="Ex: O apresentador está puto com o custo de vida e fala sobre ter mais de uma fonte de renda.")

    if st.button("✨ GERAR VÍDEO COMPLETO"):
        if not contexto:
            st.warning("A IA precisa do contexto!")
        else:
            with st.status("IA Pensando...", expanded=True) as status:
                # Prompt reforçado para criar o título da capa
                prompt = f"""
                Analise o vídeo sobre: "{contexto}" (Duração: {duracao_real}s).
                Objetivo: Criar um corte viral e uma capa chamativa.
                Responda APENAS: TÍTULO:X, INICIO:Y, FIM:Z.
                O título deve ser um 'hook' curto e agressivo de até 5 palavras.
                X e Y são números inteiros (máximo 30s de corte).
                """
                
                chat = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model="llama-3.3-70b-versatile")
                resposta = chat.choices[0].message.content
                
                try:
                    titulo_ia = re.search(r"TÍTULO:(.*?),", resposta).group(1)
                    start_ia = int(re.search(r"INICIO:(\d+)", resposta).group(1))
                    end_ia = int(re.search(r"FIM:(\d+)", resposta).group(1))
                    
                    st.write(f"🧠 IA Decidiu: Título para capa: '{titulo_ia}' e corte de {start_ia}s a {end_ia}s.")
                    
                    # Chama o processador completo
                    video_pronto = processar_vidiom("temp_input.mp4", start_ia, end_ia, titulo_ia)
                    
                    if video_pronto:
                        status.update(label="O corte está pronto!", state="complete")
                        with open(video_pronto, "rb") as f:
                            st.video(f)
                            st.download_button("📥 BAIXAR MEU VÍDEO COMPLETO", f, file_name="vidiom_mvp.mp4")
                except:
                    st.error("A IA se confundiu na resposta ou o tempo expirou. Tente novamente.")
                    
            if os.path.exists("temp_input.mp4"): os.remove("temp_input.mp4")
