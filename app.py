import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

def scrape_news(url: str) -> dict:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"}
    title, text, images = "", "", []
    try:
        from newspaper import Article
        article = Article(url, language="pt")
        article.download()
        article.parse()
        title = article.title or ""
        text = article.text or ""
        images = list(article.images) if article.images else []
    except Exception:
        pass
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(resp.content, "lxml")
        if not title:
            tag = soup.find("h1")
            title = tag.get_text(strip=True) if tag else ""
        if not text:
            text = " ".join(p.get_text(strip=True) for p in soup.find_all("p")[:10])
        for img in soup.find_all("img"):
            src = img.get("src") or img.get("data-src") or img.get("data-lazy-src") or ""
            if src:
                full_url = urljoin(url, src)
                if full_url not in images:
                    images.append(full_url)
    except Exception:
        pass
    skip = re.compile(r"(logo|icon|banner|sprite|pixel|tracking|avatar|badge|1x1|spacer)", re.IGNORECASE)
    filtered = [u for u in images if u.startswith("http") and not skip.search(u)]
    return {"title": title, "text": text[:2000], "images": filtered[:10]}
import json
import streamlit as st
from groq import Groq

def _client():
    return Groq(api_key=st.secrets["GROQ_API_KEY"])

def generate_overlay_text(title: str, text: str) -> str:
    prompt = (
        "Você é um especialista em marketing viral brasileiro.\n\n"
        f"Título: {title}\nResumo: {text[:500]}\n\n"
        "Crie UM texto CURTÍSSIMO (máximo 8 palavras) em MAIÚSCULAS para colocar sobre a imagem. "
        "Deve ser impactante e provocativo.\nResponda APENAS com o texto, sem aspas."
    )
    resp = _client().chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=50, temperature=0.9,
    )
    return resp.choices[0].message.content.strip().upper()

def generate_captions(title: str, text: str) -> dict:
    prompt = (
        "Você é um especialista em marketing viral brasileiro.\n\n"
        f"Título: {title}\nResumo: {text[:800]}\n\n"
        "Gere legendas virais. Retorne SOMENTE este JSON:\n"
        '{"instagram":"legenda com emojis e 5 hashtags","tiktok":"legenda curta com CTA e 3 hashtags","facebook":"legenda descritiva com pergunta"}\n'
        "Em português do Brasil."
    )
    resp = _client().chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=600, temperature=0.85,
    )
    content = resp.choices[0].message.content.strip()
    s, e = content.find("{"), content.rfind("}") + 1
    try:
        return json.loads(content[s:e])
    except Exception:
        return {"instagram": content, "tiktok": content, "facebook": content}
import io, os, textwrap, requests
from PIL import Image, ImageDraw, ImageFont

def _download(url):
    resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
    resp.raise_for_status()
    return Image.open(io.BytesIO(resp.content)).convert("RGB")

def _font(size):
    for path in ["assets/fonts/BebasNeue-Regular.ttf","C:/Windows/Fonts/impact.ttf","C:/Windows/Fonts/arialbd.ttf","C:/Windows/Fonts/arial.ttf"]:
        if os.path.exists(path):
            try: return ImageFont.truetype(path, size)
            except: continue
    return ImageFont.load_default()

def add_text_overlay(img, text):
    img = img.resize((1080, 1080), Image.LANCZOS)
    w, h = img.size
    grad = Image.new("RGBA", (w, 420), (0,0,0,0))
    gd = ImageDraw.Draw(grad)
    for i in range(420):
        gd.line([(0,i),(w,i)], fill=(0,0,0,int(210*i/420)))
    base = img.convert("RGBA")
    base.paste(grad, (0, h-420), grad)
    img = base.convert("RGB")
    draw = ImageDraw.Draw(img)
    font = _font(95)
    lines = textwrap.fill(text, width=14).split("\n")
    y = h - (107)*len(lines) - 70
    for line in lines:
        try: tw = draw.textlength(line, font=font)
        except: tw = len(line)*57
        x = (w-tw)/2
        for dx,dy in [(-3,-3),(3,-3),(-3,3),(3,3),(0,3),(0,-3),(3,0),(-3,0)]:
            draw.text((x+dx,y+dy), line, font=font, fill=(0,0,0))
        draw.text((x,y), line, font=font, fill=(255,220,0))
        y += 107
    return img

def process_image(image_url, overlay_text):
    buf = io.BytesIO()
    add_text_overlay(_download(image_url), overlay_text).save(buf, format="PNG")
    return buf.getvalue()
import uuid
from datetime import datetime
import streamlit as st
from supabase import create_client

def _client():
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

def upload_image(image_bytes, filename=None):
    filename = filename or f"{uuid.uuid4()}.png"
    try:
        _client().storage.from_("news-images").upload(filename, image_bytes, {"content-type":"image/png"})
        return _client().storage.from_("news-images").get_public_url(filename)
    except: return ""

def save_history(url_origem, titulo, url_imagem, legendas):
    try:
        _client().table("history").insert({
            "url_origem":url_origem,"titulo":titulo,
            "url_imagem_editada":url_imagem,"legendas_json":legendas,
            "criado_em":datetime.utcnow().isoformat()
        }).execute()
    except: pass

def get_history(limit=10):
    try:
        return _client().table("history").select("*").order("criado_em",desc=True).limit(limit).execute().data or []
    except: return []
import streamlit as st
import requests
from io import BytesIO
from PIL import Image
from modules.scraper import scrape_news
from modules.ai_generator import generate_overlay_text, generate_captions
from modules.image_editor import process_image
from modules.supabase_client import upload_image, save_history, get_history

st.set_page_config(page_title="ViralNews Editor", page_icon="🔥", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;600;800&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif;background:#0a0a0f;color:#f0f0f0}
.title{font-family:'Bebas Neue',sans-serif;font-size:3.8rem;background:linear-gradient(135deg,#ff6b35,#f7c59f,#ff6b35);-webkit-background-clip:text;-webkit-text-fill-color:transparent;text-align:center;letter-spacing:4px}
.sub{text-align:center;color:#777;margin-bottom:2rem}
.stButton>button{background:linear-gradient(135deg,#ff6b35,#e63946);color:#fff;border:none;border-radius:8px;font-weight:800;font-size:1.05rem;letter-spacing:1px;width:100%}
.stButton>button:hover{transform:translateY(-2px);box-shadow:0 8px 25px rgba(255,107,53,.45)}
.box{background:#13131f;border:1px solid #2a2a40;border-radius:10px;padding:1rem 1.2rem;margin:.4rem 0 1rem;font-size:.93rem;line-height:1.65;white-space:pre-wrap}
.tag{display:inline-block;padding:.2rem .9rem;border-radius:20px;font-size:.72rem;font-weight:800;letter-spacing:1.2px;margin-bottom:.4rem}
.ig{background:linear-gradient(135deg,#833ab4,#fd1d1d,#fcb045);color:#fff}
.tt{background:#000;color:#fff;border:1px solid #444}
.fb{background:#1877f2;color:#fff}
.hc{background:#0f0f1c;border:1px solid #1e1e35;border-radius:8px;padding:.75rem;margin-bottom:.5rem;font-size:.8rem;color:#999}
</style>""", unsafe_allow_html=True)

st.markdown('<div class="title">VIRALNEWS EDITOR</div>', unsafe_allow_html=True)
st.markdown('<div class="sub">Cole o link de qualquer noticia e gere conteudo viral com IA em segundos</div>', unsafe_allow_html=True)
st.markdown("---")

with st.sidebar:
    st.markdown("### Historico")
    try:
        for item in get_history(8):
            t = (item.get("titulo") or "Sem titulo")[:55]
            u = item.get("url_origem","#")
            st.markdown(f'<div class="hc"><b>{t}...</b><br><a href="{u}" target="_blank" style="color:#ff6b35;font-size:.75rem">Ver noticia</a></div>', unsafe_allow_html=True)
    except: st.caption("Configure o Supabase para ver o historico.")

c1,_ = st.columns([3,1])
with c1:
    url = st.text_input("", placeholder="https://www.automotivo.com.br/noticia/...", label_visibility="collapsed")
b1,_ = st.columns([1,3])
with b1:
    gerar = st.button("GERAR CONTEUDO VIRAL")

if gerar:
    if not url or not url.startswith("http"):
        st.error("Insira uma URL valida."); st.stop()
    with st.spinner("Extraindo noticia..."): data = scrape_news(url)
    if not data["title"] and not data["images"]:
        st.error("Nao foi possivel extrair. Tente outro link."); st.stop()
    st.success(f"**{data['title'][:90]}**")
    if not data["images"]:
        st.warning("Nenhuma imagem encontrada."); st.stop()

    st.markdown("#### Escolha a imagem:")
    n = min(4, len(data["images"]))
    cols = st.columns(n)
    sel = st.session_state.get("sel", data["images"][0])
    for i in range(n):
        with cols[i]:
            try:
                r = requests.get(data["images"][i], timeout=8, headers={"User-Agent":"Mozilla/5.0"})
                st.image(Image.open(BytesIO(r.content)), use_container_width=True)
                if st.button("Usar", key=f"s{i}"):
                    st.session_state["sel"] = data["images"][i]; sel = data["images"][i]
            except: st.caption("indisponivel")

    st.markdown("---")
    with st.spinner("Criando texto chamativo..."): overlay = generate_overlay_text(data["title"], data["text"])
    overlay = st.text_input("Texto na imagem (edite se quiser):", value=overlay)

    with st.spinner("Editando imagem..."):
        try: img_bytes = process_image(sel, overlay)
        except Exception as e: st.error(f"Erro: {e}"); st.stop()

    with st.spinner("Gerando legendas virais..."): caps = generate_captions(data["title"], data["text"])

    st.markdown("## Resultado Final")
    L, R = st.columns(2)
    with L:
        st.markdown("**Imagem 1080x1080:**")
        st.image(img_bytes, use_container_width=True)
        st.download_button("BAIXAR IMAGEM", img_bytes, "viral_news.png", "image/png")
    with R:
        st.markdown("**Legendas Virais:**")
        for key, label, cls in [("instagram","INSTAGRAM","ig"),("tiktok","TIKTOK","tt"),("facebook","FACEBOOK","fb")]:
            st.markdown(f'<span class="tag {cls}">{label}</span>', unsafe_allow_html=True)
            st.markdown(f'<div class="box">{caps.get(key,"")}</div>', unsafe_allow_html=True)
            st.code(caps.get(key,""), language=None)

    try:
        with st.spinner("Salvando..."): save_history(url, data["title"], upload_image(img_bytes), caps)
        st.success("Salvo no historico!")
    except: st.info("Supabase nao configurado — historico nao salvo.")
