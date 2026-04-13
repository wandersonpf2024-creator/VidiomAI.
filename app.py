# ------------------ IMPORTS ------------------
import streamlit as st
from supabase import create_client
from groq import Groq

# ------------------ CONFIG ------------------
st.set_page_config(page_title="NutriScan AI", layout="wide")

# ------------------ API ------------------
supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ------------------ MENU ------------------
menu = st.sidebar.selectbox("Menu", ["App", "Admin"])

# =========================================================
# ======================= APP =============================
# =========================================================

if menu == "App":

    if "user" not in st.session_state:
        st.session_state.user = None

    if not st.session_state.user:
        st.title("Login")

        email = st.text_input("Enter your email")

        if st.button("Enter"):
            if email:

                try:
                    res = supabase.table("users").select("*").eq("email", email).execute()

                    # GARANTE QUE NÃO QUEBRE
                    if res.data and len(res.data) > 0:
                        user = res.data[0]
                    else:
                        supabase.table("users").insert({
                            "email": email,
                            "credits": 3
                        }).execute()

                        res2 = supabase.table("users").select("*").eq("email", email).execute()
                        user = res2.data[0]

                    st.session_state.user = user
                    st.rerun()

                except Exception as e:
                    st.error(f"Erro no login: {e}")

        st.stop()

    user = st.session_state.user

    # UI
    st.title("🥗 NutriScan AI")
    st.write(f"👤 {user['email']}")
    st.write(f"💰 Credits: {user.get('credits', 0)}")

    query = st.text_area("Describe your goal")

    if user.get("credits", 0) <= 0:
        st.warning("No credits left. Upgrade.")
    else:
        if st.button("GENERATE"):
            if query:
                try:
                    with st.spinner("AI working..."):
                        resp = groq_client.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            messages=[{"role":"user","content":query}]
                        )
                        plan = resp.choices[0].message.content

                    st.success("Done!")
                    st.write(plan)

                    # Atualiza créditos
                    new_credits = user["credits"] - 1

                    supabase.table("users").update({
                        "credits": new_credits
                    }).eq("email", user["email"]).execute()

                    st.session_state.user["credits"] = new_credits

                except Exception as e:
                    st.error(f"Erro IA: {e}")

# =========================================================
# ===================== ADMIN =============================
# =========================================================

if menu == "Admin":

    password = st.text_input("Admin Password", type="password")

    if password != "admin123":
        st.stop()

    st.title("🧠 Admin Dashboard")

    try:
        res = supabase.table("users").select("*").execute()
        users = res.data if res.data else []

        for user in users:
            st.markdown("---")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.write(user.get("email", "no email"))

            with col2:
                credits = st.number_input(
                    f"Credits_{user['id']}",
                    value=user.get("credits", 0)
                )

            with col3:
                if st.button(f"Update {user['email']}"):
                    supabase.table("users").update({
                        "credits": credits
                    }).eq("id", user["id"]).execute()
                    st.success("Updated")

    except Exception as e:
        st.error(f"Erro no admin: {e}")
