import streamlit as st
import os
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip

# --- CONFIGURAÇÃO ESTÉTICA (ESTILO DASHBOARD LARGO) ---
st.set_page_config(page_title="VIDIOM AI | Dashboard", layout="wide")

st.markdown("""
    <style>
    /* 1. Fundo Escuro Profissional */
    .stApp {
        background-color: #05070a;
        color: #e2e8f0;
    }
    
    /* 2. Cabeçalho Estilo App (Alinhado à esquerda como na imagem) */
    .header-container {
        display: flex;
        align-items: center;
        gap: 15px;
        padding: 10px 0 30px 0;
    }
    .main-title {
        font-size: 24px;
        font-weight: 700;
        color: #ffffff;
        margin: 0;
    }

    /* 3. Área de Upload Larga (Estilo Dashboard) */
    div[data-testid="stFileUploader"] {
        background-color: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 20px;
    }
    
    /* 4. Cards de Opções e Vídeo */
    .stVideo {
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    }

    /* 5. Sliders e Inputs */
    .stSlider > div > div > div > div { background-color: #6366f1; }
    .stTextArea textarea {
        background-color: #0f172a;
        border: 1px solid #1e293b;
        color: white;
        border-radius: 8px;
    }

    /* 6. Botões de Legenda em Grade Larga */
    div[data-testid="column"] button {
        background-color: #1e293b;
        color: #ffffff;
        border: 1px solid #334155;
        border-radius: 8px;
        width: 100%;
    }

    /* 7. Botão Converter (Lado Direito inferior como no app) */
    .stButton>button {
        background: #ffffff;
        color: #000000 !important;
        border-radius: 8px;
        font-weight: 700;
        padding: 10px 40px;
        border: none;
        float: right;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO DE CORTE COM MARCA D'ÁGUA ---
def processar_corte(video_path, start, end):
    output = "vidiom_final.mp4"
    try:
        with VideoFileClip(video_path, audio=True).subclip(start, end) as video:
            # Tenta aplicar a logo que você enviou (precisa estar na pasta como VIDIOM.AI.png)
            if os.path.exists("VIDIOM.AI.png"):
                logo = (ImageClip("VIDIOM.AI.png")
                        .set_duration(video.duration)
                        .resize(height=35)
                        .margin(right=20, bottom=20, opacity=0)
                        .set_opacity(0.7)
                        .set_position(("right", "bottom")))
                video_final = CompositeVideoClip([video, logo])
            else:
                video_final = video
            
            video_final.write_videofile(output, codec="libx264", audio_codec="aac", logger=None, threads=1)
        return output
    except Exception as e:
        st.error(f"Erro: {e}")
        return None

# --- ESTRUTURA DA INTERFACE ---

# Cabeçalho com Ícone
st.markdown("""
    <div class="header-container">
        <span style="font-size: 30px;">🎬</span>
        <h1 class="main-title">Converta vídeos longos em vídeos curtos</h1>
    </div>
    """, unsafe_allow_html=True)

# 1. Upload em toda a largura
video_file = st.file_uploader("", type=["mp4", "mov"])

if video_file:
    with open("temp.mp4", "wb") as f:
        f.write(video_file.getbuffer())
    
    with VideoFileClip("temp.mp4") as v:
        duracao_max = int(v.duration)

    # 2. Player de Vídeo (Centralizado no dashboard)
    st.video("temp.mp4")
    
    st.write("### Selecione a parte que deseja converter vídeos curtos")
    tempo = st.slider("", 0, duracao_max, (0, min(60, duracao_max)))
    
    st.write("---")
    
    # 3. Grade de Legendas
    st.write("### Selecionar modelo de legenda")
    cols = st.columns(8) # Mais colunas para o estilo largo
    for i, label in enumerate(["Default", "Glow", "Impact", "Cyber", "Retro", "Clean", "Bold", "Future"]):
        with cols[i]: st.button(label, key=f"btn_{i}")

    st.write("---")

    # 4. Rodapé de Ação (Contexto + Botão de Conversão)
    col_ctx, col_btn = st.columns([3, 1])
    
    with col_ctx:
        contexto = st.text_area("Defina a duração ou contexto dos vídeos curtos", placeholder="Ex: Focar na parte da Porsche...")
    
    with col_btn:
        st.write("##") # Alinhamento
        if st.button("Converter"):
            with st.status("Processando...", expanded=False):
                res = processar_corte("temp.mp4", tempo[0], tempo[1])
                if res:
                    st.success("Pronto!")
                    with open(res, "rb") as f:
                        st.download_button("📥 BAIXAR VÍDEO", f, file_name="vidiom_output.mp4")

else:
    # Mostra a imagem de instrução quando não há vídeo (estilo o print que você mandou)
    st.info("Arraste um vídeo MP4 para começar a mágica.")

st.markdown("<br><center><small>VIDIOM.AI - O futuro da edição automática</small></center>", unsafe_allow_html=True)
