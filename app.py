import streamlit as st
import os
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
# Importando as bibliotecas para desenhar o texto
from moviepy.video.VideoClip import TextClip

# --- 1. CONFIGURAÇÃO DA PÁGINA (WIDE MODE) ---
st.set_page_config(page_title="VIDIOM AI | Dashboard", layout="wide")

# --- 2. CSS CUSTOMIZADO (DASHBOARD + LOGO TOPO) ---
st.markdown("""
    <style>
    /* Nome do App no Topo (Estilo Minimalista) */
    .top-header {
        text-align: center;
        padding: 20px 0 5px 0;
        font-family: 'Inter', sans-serif;
        font-size: 34px;
        font-weight: 300;
        letter-spacing: 7px;
        color: #ffffff;
        text-transform: uppercase;
    }

    /* Forçar largura total do dashboard */
    .main .block-container {
        max-width: 95% !important;
        padding-left: 5% !important;
        padding-right: 5% !important;
    }
    
    .stApp {
        background-color: #05070a;
        color: #ffffff;
    }

    /* Linha divisória e Título com Claquete */
    .header-box {
        display: flex;
        align-items: center;
        margin-bottom: 25px;
        padding-top: 15px;
        border-top: 1px solid #1e293b;
    }
    .header-text {
        font-size: 22px;
        font-weight: bold;
        margin-left: 12px;
    }

    /* Estilização do Upload */
    div[data-testid="stFileUploader"] {
        background-color: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 10px;
    }

    /* Botão CONVERTER (Branco Estilo Pílula) */
    div.stButton > button:first-child {
        background-color: #ffffff !important;
        color: #000000 !important;
        border-radius: 30px !important;
        padding: 12px 50px !important;
        font-weight: bold !important;
        border: none !important;
        float: right;
        box-shadow: 0 4px 15px rgba(255,255,255,0.1);
    }

    /* Botões de Legenda (Grade) */
    .stButton > button {
        background-color: #0f172a;
        color: #94a3b8;
        border: 1px solid #1e293b;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LÓGICA DE PROCESSAMENTO (MARCA D'ÁGUA DE TEXTO INTERNO) ---
def processar_vidiom_no_image_externa(video_in, start, end):
    saida = "vidiom_export_text_watermark.mp4"
    try:
        with VideoFileClip(video_in, audio=True).subclip(start, end) as clip:
            
            # Recriando a sua logo apenas com texto (Sem arquivo .png)
            # Nota: No Streamlit Cloud (Linux), se a fonte 'Arial' não estiver instalada, 
            # ele vai usar a padrão do sistema, mas não vai quebrar.
            
            try:
                # Tentativa profissional com fonte estilizada
                marca_texto = (TextClip("VIDIOM.AI", fontsize=30, color='white', font='Arial-Bold', interline=5)
                               .set_opacity(0.6) # Transparência discreta
                               .set_duration(clip.duration)
                               .set_position(('right', 'bottom'))) # Canto inferior direito
            except:
                # Fallback se a fonte 'Arial' falhar (comum no plano grátis)
                # O MoviePy vai usar a fonte padrão do sistema para desenhar o texto.
                marca_texto = (TextClip("VIDIOM.AI", fontsize=30, color='white')
                               .set_opacity(0.6)
                               .set_duration(clip.duration)
                               .set_position(('right', 'bottom')))

            # Combina o vídeo com a marca d'água de texto interno
            clip_final = CompositeVideoClip([clip, marca_texto])
            
            # Exportação otimizada
            clip_final.write_videofile(saida, codec="libx264", audio_codec="aac", logger=None, threads=1)
        return saida
    except Exception as e:
        st.error(f"Erro no processamento técnico: {e}")
        return None

# --- 4. INTERFACE DO USUÁRIO ---

# Logo Centralizada no Topo
st.markdown('<div class="top-header">VIDIOM.AI</div>', unsafe_allow_html=True)

# Título com Claquete
st.markdown('<div class="header-box">🎬 <span class="header-text">Converta vídeos longos em vídeos curtos</span></div>', unsafe_allow_html=True)

# Upload de Vídeo
video_file = st.file_uploader("", type=["mp4", "mov"])

if video_file:
    # Salva o arquivo temporário
    with open("temp_input.mp4", "wb") as f:
        f.write(video_file.getbuffer())
    
    with VideoFileClip("temp_input.mp4") as v:
        duracao_total = int(v.duration)

    # Player de Preview
    st.video("temp_input.mp4")
    
    st.write("### Selecione a parte que deseja converter")
    tempo = st.slider("", 0, duracao_total, (0, min(60, duracao_total)))

    st.write("### Selecionar modelo de legenda")
    # Grade de 10 opções de legenda
    cols = st.columns(10)
    opcoes = ["Default", "Glow", "Impact", "Cyber", "Retro", "Clean", "Bold", "Future", "Minimal", "Pro"]
    for i, label in enumerate(opcoes):
        with cols[i]: st.button(label, key=f"btn_{i}")

    st.write("---")

    # Rodapé: Contexto + Botão de Ação
    c1, c2 = st.columns([3, 1])
    with c1:
        txt_contexto = st.text_area("Defina a duração ou contexto dos vídeos curtos", placeholder="Ex: Focar na conversa sobre a Porsche...")
    
    with c2:
        st.write("##") # Espaçador técnico
        if st.button("Converter"):
            with st.status("🎬 Gerando vídeo e desenhando marca d'água...", expanded=False):
                resultado = processar_vidiom_no_image_externa("temp_input.mp4", tempo[0], tempo[1])
                if resultado:
                    st.success("Corte finalizado!")
                    with open(resultado, "rb") as f:
                        st.download_button("📥 BAIXAR AGORA", f, file_name="vidiom_short.mp4")
else:
    # Estado inicial com instrução
    st.info("Arraste e solte seu vídeo MP4 ou MOV para começar a edição.")

# Rodapé simples
st.markdown("<br><center><small>© 2026 VIDIOM.AI | Edição Inteligente</small></center>", unsafe_allow_html=True)
