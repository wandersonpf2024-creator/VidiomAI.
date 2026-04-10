import streamlit as st
import re
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

# --- 1. CONFIGURAÇÃO VISUAL (ESTILO PREMIUM DARK) ---
st.set_page_config(page_title="Vidiom AI | Viral Slicer", layout="centered", page_icon="✂️")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #e0e0e0; }
    h1 { background: -webkit-linear-gradient(#fff, #888); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; }
    .stButton>button { width: 100%; background: linear-gradient(135deg, #6366f1, #a855f7); color: white; border: none; padding: 18px; border-radius: 15px; font-weight: bold; font-size: 18px; transition: 0.3s; }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 10px 20px rgba(99, 102, 241, 0.4); }
    .stTextInput>div>div>input { background-color: #0f0f0f !important; border: 1px solid #333 !important; color: white !important; padding: 20px !important; border-radius: 12px !important; }
    .card { background-color: #0a0a0a; border: 1px solid #1a1a1a; padding: 25px; border-radius: 20px; margin-top: 20px; border-left: 5px solid #6366f1; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CONFIGURAÇÃO DA IA ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except:
    st.error("Erro: Adicione sua GEMINI_API_KEY nas configurações do Streamlit.")

def get_video_id(url):
    pattern = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
    match = re.search(pattern, url)
    return match.group(1) if match else None

# --- 3. INTERFACE PRINCIPAL ---
st.title("✂️ Vidiom AI: Viral Slicer")
st.write("Crie cortes virais para Instagram, TikTok, Reels e Kwai em segundos.")

url_video = st.text_input("Cole o link do vídeo aqui (YouTube):", placeholder="https://www.youtube.com/watch?v=...")

if st.button("🧬 Gerar Cortes e Legendas"):
    if not url_video:
        st.error("Por favor, cole um link.")
    else:
        vid_id = get_video_id(url_video)
        
        with st.spinner("Analisando conteúdo e gerando estratégia de legendas..."):
            transcript_text = ""
            # Tenta extrair a fala do vídeo
            if vid_id:
                try:
                    t_list = YouTubeTranscriptApi.list_transcripts(vid_id)
                    try:
                        t = t_list.find_transcript(['pt', 'en']).fetch()
                    except:
                        t = t_list.find_generated_transcripts().fetch()
                    transcript_text = " ".join([i['text'] for i in t])
                except:
                    transcript_text = None
            
            # IA GEMINI - Gerando o roteiro com foco em legendas
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Instrução poderosa para a IA
            instrucao = (
                f"Analise o vídeo: {url_video}. Contexto (se houver): {transcript_text[:5000] if transcript_text else 'Sem transcrição disponível'}. "
                "Crie 2 roteiros de cortes perfeitos para TikTok/Reels/Kwai. "
                "Para cada corte, você DEVE entregar:\n\n"
                "1. 📌 TÍTULO VIRAL: Um título que force o clique.\n"
                "2. 🧲 O GANCHO (HOOK): A frase exata que deve aparecer escrita no centro da tela nos primeiros 2 segundos.\n"
                "3. 📝 ROTEIRO DE FALA: O trecho do vídeo que deve ser cortado.\n"
                "4. 💬 GUIA DE LEGENDAS: Indique quais palavras devem ficar COLORIDAS ou EM NEGRITO para prender a atenção (Estilo Alex Hormozi)."
            )

            try:
                response = model.generate_content(instrucao)
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.subheader("✨ Estratégia de Corte Finalizada")
                st.markdown(response.text)
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.success("Dica: Use esses textos nos editores (CapCut, Premiere) para garantir a retenção!")
            except Exception as e:
                st.error("A IA está ocupada. Tente novamente em 30 segundos.")

st.markdown("---")
st.caption("Focado em maximizar sua retenção no Instagram, TikTok e Kwai.")
