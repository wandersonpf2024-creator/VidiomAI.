# ... (mesmo CSS e imports)

# ------------------ API SETUP ------------------
try:
    groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
except Exception as e:
    st.error("Check your Secrets: GROQ_API_KEY, SUPABASE_URL, SUPABASE_KEY")
    st.stop()

def check_usage(email):
    try:
        # CORREÇÃO: Filtra apenas pelo e-mail do usuário atual
        res = supabase.table("refeicoes").select("id").eq("user_email", email).execute()
        return len(res.data)
    except: return 0

# ------------------ MAIN GENERATOR ------------------
# Passamos o e-mail do usuário para a contagem
usage = check_usage(st.session_state.user)
limit = 3

col_m1, col_m2, col_m3 = st.columns([1, 4, 1])
with col_m2:
    st.subheader(f"Welcome, {st.session_state.user}")
    query = st.text_area("What's your goal?", placeholder="Ex: 7-day keto plan...", height=120)

    if usage >= limit:
        st.warning("⚠️ Daily limit reached. Please upgrade to Pro below.")
    else:
        st.write(f"Credits used: **{usage}/{limit}**")
        if st.button("GENERATE PLAN 🚀", use_container_width=True):
            if query:
                placeholder = st.empty()
                with placeholder.container():
                    st.write("🤖 AI is analyzing your goals...")
                    bar = st.progress(0)
                    for i in range(100):
                        time.sleep(0.005) # Mais rápido para não irritar o usuário
                        bar.progress(i+1)
                
                try:
                    resp = groq_client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role":"system","content":"You are a pro nutritionist. English only."},
                                  {"role":"user","content":query}]
                    )
                    plan = resp.choices[0].message.content
                    placeholder.empty()

                    # OTIMIZAÇÃO: Digitação por chunks (pedaços) para fluidez
                    out = st.empty()
                    chunks = plan.split(' ')
                    text = ""
                    for word in chunks:
                        text += word + " "
                        out.markdown(f'<div style="background:rgba(255,255,255,0.05);padding:25px;border-radius:15px;border:1px solid #22c55e;">{text}</div>', unsafe_allow_html=True)
                        time.sleep(0.05) # Delay suave por palavra
                    
                    # CORREÇÃO: Salva com o e-mail do usuário
                    supabase.table("refeicoes").insert({
                        "nome_prato": query[:50], 
                        "user_email": st.session_state.user
                    }).execute()
                    
                    st.success("Plan generated! Review below.")
                    st.button("Update Credits") # Força o rerun para atualizar contador
                    
                except Exception as e:
                    st.error(f"AI Error: {e}")
