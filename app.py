import streamlit as st
from supabase import create_client

st.set_page_config(page_title="Admin Panel", layout="wide")

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

# 🔐 LOGIN ADMIN SIMPLES
password = st.text_input("Admin Password", type="password")

if password != "admin123":
    st.stop()

st.title("🧠 Admin Dashboard")

# 📊 BUSCAR USUÁRIOS
res = supabase.table("users").select("*").execute()
users = res.data

# 📋 LISTA
for user in users:
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.write(f"📧 {user['email']}")
    
    with col2:
        new_credits = st.number_input(
            f"Credits_{user['id']}",
            value=user["credits"]
        )
    
    with col3:
        new_plan = st.selectbox(
            f"Plan_{user['id']}",
            ["free", "pro", "elite"],
            index=["free","pro","elite"].index(user["plan"])
        )
    
    with col4:
        if st.button(f"Update {user['email']}"):
            supabase.table("users").update({
                "credits": new_credits,
                "plan": new_plan
            }).eq("id", user["id"]).execute()
            
            st.success("Updated!")

# 🔥 RESET GLOBAL
st.markdown("## ⚠️ Reset All Users")

if st.button("Reset Credits to 3"):
    supabase.table("users").update({
        "credits": 3
    }).neq("id", "0").execute()

    st.success("All users reset!")
