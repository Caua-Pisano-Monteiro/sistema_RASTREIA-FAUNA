import requests
import streamlit as st

# Use o mesmo API_URL que você já usa no login.py
API_URL = "http://127.0.0.1:8000"

st.title("Criar conta")

with st.form("form_cadastro"):
    usuario = st.text_input("Usuário")
    funcao = st.text_input("Função")
    email = st.text_input("E-mail")
    e_confimar = st.text_input("Confirme seu email")
    senha = st.text_input("Senha", type="password")
    confirmar = st.text_input("Confirmar senha", type="password")
    enviar = st.form_submit_button("Criar conta")

if enviar:
    if not usuario or not email or not senha:
        st.warning("Preencha usuário, e-mail e senha.")
        st.stop()

    if len(senha) < 3:
        st.warning("A senha precisa ter pelo menos 8 caracteres.")
        st.stop()

    if email != e_confimar:
        st.warning("Os emails não são iguais. Digite novamente")
        st.stop()

    if senha != confirmar:
        st.warning("As senhas não são iguais. Digite a mesma senha nos dois campos.")
        st.stop()

    try:
        r = requests.post(
            f"{API_URL}/usuarios",  # troque pelo endpoint da sua API
            json={"username": usuario, "email": email, "funcao": funcao, "password": senha},
            timeout=10,
        )
    except requests.RequestException:
        st.error("Não foi possível conectar à API.")
        st.stop()

    if r.status_code in (200, 201):
        st.success("Conta criada. Agora é só entrar.")
    elif r.status_code == 409:
        st.error("Já existe uma conta com esse usuário ou e-mail.")
    else:
        try:
            detalhe = r.json().get("detail", "")
        except ValueError:
            detalhe = ""
        st.error(f"Não foi possível criar a conta. {detalhe}".strip())

col1, col2 = st.columns(2)
with col1:
    if st.button("Já tenho conta"):
        st.switch_page("login.py")
with col2:
    if st.button("Voltar ao início"):
        st.switch_page("landing.py")
