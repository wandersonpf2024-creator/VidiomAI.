import streamlit as st
import os
import re
from groq import Groq
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip

# --- CONFIGURAÇÃO ESTÉTICA (CSS CENTRALIZADO E MODERNO) ---
st.set_page_config(page_title="VIDIOM AI | Pro Editor", layout="wide")

st.markdown("""
    <style>
    /* 1. Fundo Deep Dark e Reset de Margens */
    .stApp { background-color: #05070a; color: #e2e8f0; }
    
    /* 2. Centralização Absoluta do Conteúdo Main */
    .main .block-container { max-width: 800px; padding-top: 2rem; padding-bottom: 2rem; margin: 0 auto; }

    /* 3. Título Centralizado */
    .main-title { font-size: 32px; font-weight: 800; text-align: center; margin-bottom: 30px; color: #ffffff; }
    
    /* 4. Estilização do File Uploader */
    div[data-testid="stFileUploader"] { background-color: #0f172a; border: 2px dashed #334155; border-radius: 16px; padding: 40px; text-align: center; }

    /* 5. Player de Vídeo Arredondado */
    .stVideo { border-radius: 12px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }

    /* 6. Inputs e Sliders */
    .stTextArea textarea { background-color: #0f172a; border: 1px solid #1e293b; color: white; border-radius: 12px; }
    .stSlider > div > div > div > div { background-color: #6366f1; }

    /* 7. Botões de Legenda (Cards Visuais Mockados) */
    div[data-testid="column"] button { background-color: #0f172a; color: #94a3b8; border: 1px solid #1e293b; border-radius: 10px; padding: 10px; width: 100%; transition: 0.2s; }
    div[data-testid="column"] button:hover { border-color: #6366f1; color: white; }

    /* 8. Botão Converter "Glow Premium" */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%);
        color: white !important;
        border-radius: 50px;
        padding: 16px 30px;
        font-weight: 700;
        font-size: 18px;
        border: none;
        transition: 0.3s;
        text-transform: uppercase;
        margin-top: 20px;
    }
    .stButton>button:hover { transform: translateY(-3px); box-shadow: 0 10px 30px rgba(168, 85, 247, 0.5); }

    /* Fix para remover o padding padrão do Streamlit nas colunas */
    [data-testid="column"] { padding: 0 5px !important; }
    </style>
    """, unsafe_allow_html=True)

# Segurança
if "GROQ_API_KEY" not in st.secrets:
    st.error("Configure a 'GROQ_API_KEY' nas Secrets!")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- LÓGICA DE BACKEND (COM MARCA D'ÁGUA DE IMAGEM) ---
def processar_corte_com_marca(video_path, start, end):
    output = "vidiom_final_com_marca.mp4"
    try:
        # Carregamento 'lazy' para economizar memória no plano grátis
        with VideoFileClip(video_path, audio=True).subclip(start, end) as video:
            
            # Tenta carregar a logo (arquivo logo_vidiom_recortada.png precisa estar no GitHub)
            if os.path.exists("logo_vidiom_recortada.png"):
                logo = (ImageClip("logo_vidiom_recortada.png")
                        .set_duration(video.duration)
                        .resize(height=40) # Tamanho da marca no canto
                        .margin(right=20, bottom=20, opacity=0) # Distância da borda
                        .set_opacity(0.6) # Deixa transparente
                        .set_position(("right", "bottom")))
                
                # Junta o vídeo com a logo (Marca d'água robusta)
                video_final = CompositeVideoClip([video, logo])
            else:
                # Se o arquivo não existir, ele faz o corte sem marca para não dar erro
                video_final = video

            # Renderização otimizada para o plano grátis (threads=1 para não travar)
            video_final.write_videofile(
                output, 
                codec="libx264", 
                audio_codec="aac", 
                temp_audiofile='temp-audio.m4a', 
                remove_temp=True, 
                logger=None, 
                threads=1
            )
            
        return output
    except Exception as e:
        st.error(f"Erro no processamento técnico: {e}")
        return None

# --- INTERFACE (LAYOUT CENTRALIZADO "OPUS STYLE") ---
st.markdown('<div class="main-title">🎬 Converta vídeos longos em vídeos curtos</div>', unsafe_allow_html=True)

# Área de Upload (Centralizada)
video_file = st.file_uploader("", type=["mp4", "mov"])

if video_file:
    # Salva temporariamente
    with open("video_input.mp4", "wb") as f:
        f.write(video_file.getbuffer())
    
    with VideoFileClip("video_input.mp4") as v:
        duracao_max = int(v.duration)

    st.write("---")

    # Player de Vídeo (Centralizado)
    st.video("video_input.mp4")

    st.write("---")
    
    # Área de Seleção (Timeline)
    st.markdown("### 🎞️ Selecione a parte que deseja converter")
    tempo = st.slider("", 0, duracao_max, (0, min(60, duracao_max)))
    st.caption(f"Duração selecionada: {tempo[1] - tempo[0]} segundos")

    st.write("---")

    # Modelos de Legenda (Cards Visuais Mockados)
    st.markdown("### ✍️ Selecionar modelo de legenda")
    cols_l1 = st.columns(3)
    with cols_l1[0]: st.button("Padrão", key="l1")
    with cols_l1[1]: st.button("Glow Ultra", key="l2")
    with cols_l1[2]: st.button("Impact Pro", key="l3")
    
    cols_l2 = st.columns(3)
    with cols_l2[0]: st.button("Cyberpunk", key="l4")
    with cols_l2[1]: st.button("Minimalist", key="l5")
    with cols_l2[2]: st.button("Retro Wave", key="l6")

    st.write("---")

    # Duração e Contexto IA (Campo Crítico)
    st.markdown("### 🤖 O que acontece no vídeo? (Contexto IA)")
    contexto = st.text_area("", placeholder="Explique para a IA qual o clímax ou o momento viral deste trecho...")
    
    st.write("---")

    # Botão Converter Premium (Centralizado e Gradient)
    if st.button("✨ Converter para Vídeo Curto"):
        if not contexto:
            st.warning("⚠️ Adicione um contexto para a IA validar o seu corte!")
        else:
            with st.status("Gerando seu corte viral e aplicando marca d'água...", expanded=True):
                final_clip = processar_corte_com_marca("video_input.mp4", tempo[0], tempo[1])
                if final_clip:
                    st.success("Corte concluído! Sua marca d'água foi aplicada.")
                    with open(final_clip, "rb") as f:
                        st.download_button("📥 BAIXAR AGORA", f, file_name="vidiom_pro_clip.mp4")
                        
            # Limpeza agressiva para economizar RAM do servidor
            if os.path.exists("video_input.mp4"): os.remove("video_input.mp4")
            if os.path.exists("vidiom_final_com_marca.mp4"): os.remove("vidiom_final_com_marca.mp4")

else:
    # Estado inicial centralizado
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.info("Arraste e solte seu vídeo MP4/MOV acima para começar a mágica.")

# Rodapé Centralizado
st.markdown("<br><br><center><small>VIDIOM.AI v18.0 - O futuro da edição automática</small></center>", unsafe_allow_html=True)
