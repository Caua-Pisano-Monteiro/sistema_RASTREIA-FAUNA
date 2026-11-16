import os
from datetime import date

import pandas as pd
import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.title("Registrar ocorrência")
if st.button("📊 Voltar dashboard"):
    st.switch_page("dashboard.py")
st.caption("Os dados são gravados no banco e o dashboard passa a incluir o novo registro.")


def buscar_dados() -> pd.DataFrame:
    r = requests.get(f"{API_URL}/data-request", timeout=30)
    r.raise_for_status()
    return pd.DataFrame(r.json())


try:
    dados = buscar_dados()
except requests.RequestException:
    st.error("Não foi possível carregar os dados da API. Verifique se ela está no ar.")
    st.stop()

# Opções vindas dos próprios dados já cadastrados
ufs = sorted(dados["sg_uf"].dropna().unique())
infracoes = sorted(dados["tp_infracao"].dropna().unique())
estados_animal = sorted(dados["ds_estado_animal"].dropna().unique())
destinacoes = sorted(dados["ds_destinacao"].dropna().unique())
localizacoes = sorted(dados["ds_localizacao"].dropna().unique())
unidades = sorted(dados["sg_unidade_controle"].dropna().unique())

# Espécie -> (nome científico, classe, ameaçada)
especies = (
    dados.dropna(subset=["no_popular_especie"])
    .drop_duplicates("no_popular_especie")
    .set_index("no_popular_especie")[["no_cientifico_especie", "ds_classe", "st_especie_ameacada"]]
    .sort_index()
)

with st.form("form_ocorrencia", clear_on_submit=False):
    st.subheader("Apreensão")
    c1, c2 = st.columns(2)
    dt_apreensao = c1.date_input("Data da apreensão", value=date.today(), max_value=date.today(), format="DD/MM/YYYY")
    tp_infracao = c2.selectbox("Tipo de infração", infracoes)

    c1, c2, c3 = st.columns(3)
    sg_uf = c1.selectbox("UF", ufs)
    no_municipio = c2.text_input("Município")
    cd_municipio = c3.text_input("Código IBGE do município (7 dígitos)", max_chars=7)

    c1, c2 = st.columns(2)
    latitude = c1.number_input("Latitude", value=None, min_value=-34.0, max_value=6.0, format="%.6f", placeholder="-18.864786")
    longitude = c2.number_input("Longitude", value=None, min_value=-74.0, max_value=-28.0, format="%.6f", placeholder="-48.269540")
    ds_localizacao = st.selectbox("Local da apreensão", localizacoes)

    st.subheader("Animais")
    c1, c2, c3 = st.columns(3)
    especie = c1.selectbox("Espécie", list(especies.index))
    qt_animais = c2.number_input("Quantidade de animais", min_value=1, value=1, step=1)
    ds_estado_animal = c3.selectbox("Estado do animal", estados_animal)
    ds_destinacao = st.selectbox("Destinação", destinacoes)

    st.subheader("Autuado e multa")
    c1, c2 = st.columns([3, 1])
    no_pessoa = c1.text_input("Nome do autuado")
    tp_pessoa = c2.selectbox("Tipo de pessoa", ["F", "J"], format_func=lambda x: "Física" if x == "F" else "Jurídica")
    c1, c2 = st.columns(2)
    vl_multa = c1.number_input("Valor da multa (R$)", min_value=0.0, value=0.0, step=100.0, format="%.2f")
    sg_unidade = c2.selectbox("Unidade de controle", unidades)

    ds_tad = st.text_area("Descrição (opcional; se vazio, é gerada automaticamente)")
    enviar = st.form_submit_button("Salvar ocorrência", type="primary")

if enviar:
    erros = []
    if not no_municipio.strip():
        erros.append("Informe o município.")
    if cd_municipio and not (cd_municipio.isdigit() and len(cd_municipio) == 7):
        erros.append("O código IBGE deve ter 7 dígitos.")
    if latitude is None or longitude is None:
        erros.append("Informe latitude e longitude.")
    if not no_pessoa.strip():
        erros.append("Informe o nome do autuado.")
    if erros:
        for e in erros:
            st.warning(e)
        st.stop()

    cientifico, classe, ameacada = especies.loc[especie]
    descricao = ds_tad.strip() or (
        f"Fica apreendido: {qt_animais} exemplar(es) de {especie} ({cientifico})."
    )

    payload = {
        "dt_apreensao": dt_apreensao.isoformat(),
        "cd_municipio": cd_municipio or None,
        "no_municipio": no_municipio.strip(),
        "sg_uf": sg_uf,
        "nu_latitude_tad": latitude,
        "nu_longitude_tad": longitude,
        "ds_wkt_local_apreensao": f"POINT ({longitude} {latitude})",
        "ds_localizacao": ds_localizacao,
        "tp_infracao": tp_infracao,
        "ds_tad": descricao[:250],
        "no_popular_especie": especie,
        "no_cientifico_especie": cientifico,
        "ds_classe": classe,
        "st_especie_ameacada": ameacada,
        "qt_animais": int(qt_animais),
        "ds_estado_animal": ds_estado_animal,
        "ds_destinacao": ds_destinacao,
        "no_pessoa_apreensao": no_pessoa.strip().upper(),
        "tp_pessoa": tp_pessoa,
        "vl_multa": vl_multa,
        "sg_unidade_controle": sg_unidade,
        "st_cancelado": "N",
        "ds_sit_apreensao": "Lavrado",
    }

    # seq_apreensao não é autoincremento no banco: usa o próximo código livre
    r = None
    try:
        proximo = int(dados["seq_apreensao"].max()) + 1
        for _ in range(3):  # tenta de novo se outro usuário gravou o mesmo código
            r = requests.post(f"{API_URL}/formulario-apreensao", json={**payload, "seq_apreensao": proximo}, timeout=15)
            if r.status_code != 400:
                break
            proximo += 1
    except requests.RequestException:
        st.error("Não foi possível conectar à API.")
        st.stop()

    if r.status_code == 201:
        st.success(f"Ocorrência {proximo} registrada com sucesso.")
        st.session_state["ocorrencia_salva"] = True
    else:
        try:
            detalhe = r.json().get("detail", "")
        except ValueError:
            detalhe = ""
        st.error(f"Não foi possível salvar ({r.status_code}). {detalhe}")

if st.session_state.get("ocorrencia_salva"):
    if st.button("📊 Ver no dashboard"):
        st.session_state["ocorrencia_salva"] = False
        st.switch_page("dashboard.py")
