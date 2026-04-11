import streamlit as st
import requests

# Exemplo de como chamar uma API de vídeo
def gerar_video_ia(prompt, modelo):
    # Aqui você usaria a URL da API escolhida (Luma, Vidu, etc)
    api_url = f"https://api.provider.com/v1/{modelo}"
    headers = {"Authorization": "Bearer SUA_CHAVE_AQUI"}
    payload = {"prompt": prompt, "duration": 15}
    
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()['video_url']

# Na interface do VIDIOM.AI
modelo_escolhido = st.selectbox("Choose AI Model", ["Luma Ray 2", "Vidu Q2", "Jimeng 3.0"])
if st.button("Generate with AI"):
    url_final = gerar_video_ia("Car driving in the rain", modelo_escolhido)
    st.video(url_final)
