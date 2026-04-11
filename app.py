import streamlit as st
from supabase import create_client
import tempfile

# ==============================
# CONFIG
# ==============================
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ==============================
# TESTE DE CONEXÃO
# ==============================
st.write("🔍 Testing connection...")

try:
    test = supabase.table("users").select("*").limit(1).execute()
    st.success("✅ Connected to Supabase!")
except Exception as e:
    st.error("❌ Connection failed")

# ==============================
# APP CONFIG
# ==============================
st.set_page_config(page_title="VideoAI Cut", layout="wide")

# ==============================
# STYLE
# ==============================
st.markdown("""
<style>
body {background-color: #0e1117; color: white;}
.stButton>button {
    background: linear-gradient(90deg, #6C63FF, #4A90E2);
    color: white;
    border-radius: 10px;
    height: 3em;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# SESSION
# ==============================
if "user" not in st.session_state:
    st.session_state.user = None

# ==============================
# MENU
# ==============================
st.sidebar.title("VideoAI Cut")
menu = st.sidebar.radio("Menu", ["Login", "Dashboard", "Upload", "Plans"])

# ==============================
# LOGIN
# ==============================
if menu == "Login":
    st.title("🔐 Login / Sign Up")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Login"):
            try:
                res = supabase.auth.sign_in_with_password({
                    "email": email,
                    "password": password
                })
                if res.user:
                    st.session_state.user = res.user
                    st.success("Logged in successfully!")
            except:
                st.error("Login error")

    with col2:
        if st.button("Create Account"):
            try:
                res = supabase.auth.sign_up({
                    "email": email,
                    "password": password
                })
                if res.user:
                    supabase.table("users").insert({
                        "email": email,
                        "credits": 30
                    }).execute()
                    st.success("Account created!")
            except:
                st.error("Signup error")

# ==============================
# DASHBOARD
# ==============================
elif menu == "Dashboard":
    if not st.session_state.user:
        st.warning("Please login first")
    else:
        st.title("🚀 Dashboard")

        email = st.session_state.user.email

        data = supabase.table("users").select("credits").eq("email", email).execute()

        if data.data:
            credits = data.data[0]["credits"]
        else:
            credits = 0

        st.metric("Credits", credits)

# ==============================
# UPLOAD
# ==============================
elif menu == "Upload":
    if not st.session_state.user:
        st.warning("Please login first")
    else:
        st.title("📤 Upload Video")

        email = st.session_state.user.email

        uploaded_file = st.file_uploader("Upload your video", type=["mp4", "mov"])

        if uploaded_file:
            st.video(uploaded_file)

            st.write("Cost:")
            st.write("✂️ Cut = 3 credits")
            st.write("📝 Captions = 2 credits")

            if st.button("Process Video"):
                data = supabase.table("users").select("credits").eq("email", email).execute()
                credits = data.data[0]["credits"]

                if credits >= 5:
                    # descontar créditos
                    supabase.table("users").update({
                        "credits": credits - 5
                    }).eq("email", email).execute()

                    # salvar arquivo temporário
                    with tempfile.NamedTemporaryFile(delete=False) as tmp:
                        tmp.write(uploaded_file.read())
                        file_path = tmp.name

                    # upload storage
                    supabase.storage.from_("videos").upload(uploaded_file.name, open(file_path, "rb"))

                    # salvar no banco
                    supabase.table("videos").insert({
                        "user_email": email,
                        "file_name": uploaded_file.name
                    }).execute()

                    st.success("Video processed successfully!")
                else:
                    st.error("Not enough credits")

        st.subheader("🧠 AI Captions (Coming Soon)")

        if st.button("Generate Captions"):
            st.info("AI captions will be added soon")

# ==============================
# PLANS
# ==============================
elif menu == "Plans":
    st.title("💳 Plans")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Free")
        st.write("30 credits")
        st.write("Max 2 minutes")

    with col2:
        st.subheader("Basic - $9.99")
        st.write("60 credits")

    with col3:
        st.subheader("Pro - $19.99")
        st.write("150 credits")

st.sidebar.write("---")
st.sidebar.write("© 2026 VideoAI Cut")
