import os
import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")
MAX_TENTATIVAS = 3

st.session_state.setdefault("tentativas", 0)

st.title("Login")

# Bloqueio por tentativas
if st.session_state["tentativas"] >= MAX_TENTATIVAS:
    st.error("Número máximo de tentativas atingido.")
    st.stop()

# Formulário
with st.form("form_login"):
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    enviar = st.form_submit_button("Entrar")

if enviar:
    if not usuario or not senha:
        st.warning("Preencha usuário e senha.")
        st.stop()

    try:
        r = requests.post(
            f"{API_URL}/login",
            json={"username": usuario, "password": senha},
            timeout=10,
        )
    except requests.RequestException:
        st.error("Não foi possível conectar à API.")
        st.stop()

    if r.status_code == 200:
        dados = r.json()
        st.session_state["autenticado"] = True
        st.session_state["username"] = dados["username"]
        st.session_state["funcao"] = dados["funcao"]
        st.session_state["tentativas"] = 0
        st.rerun()
    elif r.status_code == 401:
        st.session_state["tentativas"] += 1
        restantes = MAX_TENTATIVAS - st.session_state["tentativas"]
        if restantes > 0:
            st.error(f"Usuário ou senha incorretos. Tentativas restantes: {restantes}")
        else:
            st.rerun()
    else:
        st.error(f"Erro inesperado ({r.status_code}).")