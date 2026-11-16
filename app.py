import streamlit as st
 
st.set_page_config(page_title="Rastreia Fauna", page_icon="🐾", layout="wide")
st.session_state.setdefault("autenticado", False)
 
landing_page = st.Page("landing.py", title="Início", icon="🏠", default=True)
login_page = st.Page("login.py", title="Login", icon="🔒")
cadastro_page = st.Page("cadastro.py", title="Cadastro", icon="📝")
dashboard_page = st.Page("dashboard.py", title="Dashboard", icon="📊")
ocorrencias_page = st.Page("ocorrencias.py", title="Nova ocorrência", icon="➕")
 
if st.session_state["autenticado"]:
    pg = st.navigation([dashboard_page, ocorrencias_page])
else:
    pg = st.navigation([landing_page, login_page, cadastro_page], position="hidden")
 
pg.run()