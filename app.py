import streamlit as st
import os
from moviepy.video.io.VideoFileClip import VideoFileClip
import moviepy.video.fx.all as vfx 
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.VideoClip import ImageClip # Importamos ImageClip para a logo no vídeo

# --- 1. CONFIGURAÇÃO DE TEMA DARK (ESTILO MINDVIDEO) ---
st.set_page_config(page_title="VIDIOM AI", layout="wide")

st.markdown("""
    <style>
    /* RESET DE CORES PARA PRETO ABSOLUTO */
    .stApp {
        background-color: #0d0d0d;
        color: #ffffff;
    }

    /* BARRA LATERAL (SIDEBAR) PRETA */
    [data-testid="stSidebar"] {
        background-color: #000000 !important;
        border-right: 1px solid #1e1e1e;
    }

    /* CONTAINER DA NOVA LOGO NA SIDEBAR */
    .logo-container-sidebar {
        text-align: center;
        padding: 10px 0;
        margin-bottom: 20px;
    }

    /* MENU ITEMS ESTILO MINDVIDEO */
    .menu-item {
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 5px;
        display: flex;
        align-items: center;
        gap: 12px;
        color: #d1d1d1;
        cursor: pointer;
    }
    .menu-item:hover {
        background-color: #1a1a1a;
    }
    .active-menu {
        background-color: #262626;
        color: white;
        font-weight: bold;
    }

    /* BOTÃO UPGRADE (ROXO/AZUL) */
    .btn-upgrade {
        background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%);
        color: white;
        padding: 12px;
        border-radius: 8px;
        text-align: center;
        font-weight: bold;
        margin-top: 20px;
        cursor: pointer;
        text-decoration: none;
        display: block;
    }

    /* ESTILO DO EDITOR (ÁREA CENTRAL) */
    .main-container {
        padding: 20px;
    }
    .video-card {
        background-color: #141414;
        border-radius: 15px;
        padding: 20px;
        border: 1px solid #262627;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. MOTOR DE VÍDEO (AGORA COM MARCA D'ÁGUA EM IMAGEM) ---
def process_vidiom_with_image_watermark(video_path, start, end):
    output = "vidiom_pro_branded.mp4"
    try:
        # Carrega o vídeo original
        clip = VideoFileClip(video_path).subclip(start, end)
        
        # 1. Ajuste de dimensões para 9:16 (Sempre Par)
        h = clip.h
        w = int(h * (9/16))
        if w % 2 != 0: w -= 1 # Garante dimensão par
        
        # 2. Corte centralizado
        final_clip = vfx.crop(clip, x_center=clip.w/2, width=w).copy()
        
        # --- APLICAÇÃO DA LOGO COMO MARCA D'ÁGUA ---
        logo_path = "lonova.png" # Caminho da sua logo
        
        if os.path.exists(logo_path):
            try:
                # Carrega a logo como ImageClip
                logo = ImageClip(logo_path).set_duration(final_clip.duration).set_opacity(0.7) # 70% de opacidade
                
                # Redimensiona a logo para ficar PEQUENA (ex: 20% da largura do vídeo)
                logo = vfx.resize(logo, width=int(final_clip.w * 0.20))
                
                # Posiciona no Canto Inferior Direito (com 20px de margem)
                logo = logo.set_position(("right", "bottom")).margin(right=20, bottom=20, opacity=0)
                
                # Sobrepõe a logo no vídeo
                result = CompositeVideoClip([final_clip, logo])
            except Exception as logo_err:
                st.warning(f"Note: Error applying logo watermark. Generating clean video. (Error: {logo_err})")
                result = final_clip
        else:
            st.error(f"Error: {logo_path} not found. Clean video generated.")
            result = final_clip

        # 3. Exportação com formato compatível
        result.write_videofile(
            output, 
            codec="libx264", 
            audio_codec="aac", 
            fps=24, 
            logger=None, 
            ffmpeg_params=["-pix_fmt", "yuv420p"] # Crítico para visibilidade no iOS/Chrome
        )
        
        clip.close()
        result.close()
        return output
    except Exception as e:
        st.error(f"Render Error: {e}")
        return None

# --- 3. BARRA LATERAL (SIDEBAR) ---
with st.sidebar:
    st.markdown('<div class="logo-container-sidebar">', unsafe_allow_html=True)
    # Tenta carregar sua imagem da logo na sidebar
    try:
        st.image("lonova.png", width=200)
    except:
        st.markdown("<h2 style='text-align:center; color:white;'>VIDIOM.AI</h2>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="menu-item active-menu">🏠 Estúdio Criativo</div>', unsafe_allow_html=True)
    st.markdown('<div class="menu-item">📁 Minhas Criações</div>', unsafe_allow_html=True)
    st.write("---")
    
    # Navegação de ferramentas
    nav = st.radio("Ferramentas", ["Cortar Vídeo", "Planos de Upgrade"], label_visibility="collapsed")
    
    st.write("---")
    st.markdown('<a class="btn-upgrade">🚀 Faça Upgrade Agora</a>', unsafe_allow_html=True)

# --- 4. ÁREA PRINCIPAL (DASHBOARD) ---

if nav == "Cortar Vídeo":
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.title("🎬 Estúdio de Cortes Virais")
    st.write("Converta vídeos longos em cortes de 9:16 com sua marca d'água profissional.")
    
    uploaded = st.file_uploader("", type=["mp4", "mov"])
    
    if uploaded:
        with open("input.mp4", "wb") as f: f.write(uploaded.getbuffer())
        
        col_v, col_edit = st.columns([1.5, 1])
        
        with col_v:
            st.markdown('<div class="video-card">', unsafe_allow_html=True)
            st.video("input.mp4")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_edit:
            with VideoFileClip("input.mp4") as v_temp:
                dur = int(v_temp.duration)
            
            st.write("### Configurações de Corte")
            cut_range = st.slider("Selecione o segmento (segundos)", 0, dur, (0, min(15, dur)))
            
            st.write("---")
            if st.button("Gerar Corte com Marca d'água", use_container_width=True, type="primary"):
                with st.status("🎬 Renderizando vídeo 9:16 com sua logo..."):
                    res_path = process_vidiom_with_image_watermark("input.mp4", cut_range[0], cut_range[1])
                    if res_path:
                        st.success("Vídeo pronto para download!")
                        with open(res_path, "rb") as file_res:
                            st.download_button(
                                "📥 BAIXAR AGORA", 
                                file_res, 
                                file_name="vidiom_short.mp4", 
                                use_container_width=True
                            )
    st.markdown('</div>', unsafe_allow_html=True)
else:
    # Interface de Planos que fizemos anteriormente pode entrar aqui
    st.markdown('<h2 style="text-align:center;">Página de Planos em Manutenção</h2>', unsafe_allow_html=True)
    st.info("O editor de vídeo está funcional. Clique em 'Cortar Vídeo' na barra lateral.")
