import streamlit as st
from groq import Groq

st.set_page_config(page_title="NutriScan AI", layout="wide")

groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.title("🥗 NutriScan AI (TEST MODE)")

email = st.text_input("Enter your email")

if email:
    st.success(f"Logged as: {email}")

    credits = 3
    st.write(f"💰 Credits: {credits}")

    query = st.text_area("Describe your goal")

    if st.button("GENERATE"):
        if query:
            with st.spinner("AI working..."):
                resp = groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role":"user","content":query}]
                )
                plan = resp.choices[0].message.content

            st.success("Done!")
            st.write(plan)
