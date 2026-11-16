import pandas as pd 
import plotly.express as px
import requests
import streamlit as st

st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)

url = "http://127.0.0.1:8000/data-request"
response = requests.get(url)
dados = pd.DataFrame.from_dict(response.json())

def formatar(valor, prefixo=''):
    for unidade in ['','mil']:
        if valor < 1000:
            return f'{prefixo} {valor:.2f} {unidade}'
        valor /= 1000
    return f'{prefixo} {valor:.2f} mi'

st.title("Dashboard")

if st.button("➕ Registrar nova ocorrência"):
    st.switch_page("ocorrencias.py")

#----Tratamento dos dados
# transformando valores nulos em 0
dados['vl_multa'] = dados['vl_multa'].fillna(0)
# transformando data
dados['dt_apreensao'] = pd.to_datetime(dados['dt_apreensao'], format= '%Y-%m-%d')

#----tabelas
qtd_animais = dados.groupby('no_popular_especie')[['qt_animais']].count().reset_index()

qtd_estado = dados.groupby('sg_uf')[['qt_animais']].sum().sort_values('qt_animais', ascending=False)
coordenadas_estados = dados.drop_duplicates(subset='sg_uf')[['sg_uf', 'nu_latitude_tad', 'nu_longitude_tad']]
quantidade_estado = (
    coordenadas_estados
    .merge(qtd_estado, left_on='sg_uf', right_index=True)
    .sort_values('qt_animais', ascending=False)
    .reset_index(drop=True)
)

freq_tipoapreensao = dados.groupby('tp_infracao')[['qt_animais']].count().sort_values('qt_animais',ascending=False).reset_index()

quantidade_mensal = dados.set_index('dt_apreensao').groupby(pd.Grouper(freq='ME'))['qt_animais'].count().reset_index()
quantidade_mensal['ANO'] = quantidade_mensal['dt_apreensao'].dt.year
quantidade_mensal['MES'] = quantidade_mensal['dt_apreensao'].dt.month_name()

#----gráficos
fig_qtd_animais = px.bar(qtd_animais.sort_values('qt_animais', ascending=False), 
                         x='qt_animais', 
                         y='no_popular_especie',
                         labels={'no_popular_especie':'Nome Espécie', 'qt_animais': 'QTD'},
                         text_auto=True,
                         title = 'Quantidade que cada animal foi apreendido')
fig_qtd_animais.update_layout(xaxis_title = 'QTD')

fig_mapa_quantidade = px.scatter_geo(quantidade_estado,
                                     lat='nu_latitude_tad',
                                     lon='nu_longitude_tad',
                                     scope='south america',
                                     size='qt_animais',
                                     template='seaborn',
                                     hover_data={'nu_latitude_tad':False, 'nu_longitude_tad':False},
                                     hover_name='sg_uf',
                                     labels={'qt_animais':'quantidade'},
                                     title='Quantidede de apreensão por estado')

fig_frep_tipoapreensao = px.bar(freq_tipoapreensao.head(), 
                         x='qt_animais', 
                         y='tp_infracao',
                         labels={'tp_infracao':'Tipo Apreensão', 'qt_animais': 'QTD'},
                         text_auto=True,
                         title = 'TOP 5 tipo de apreensão mais efetuada')
fig_qtd_animais.update_layout(xaxis_title = 'QTD')

fig_qtd_mensal = px.line(quantidade_mensal,
                             x = 'MES',
                             y = 'qt_animais',
                             markers= True,
                             range_y=(0,quantidade_mensal['qt_animais'].max()),
                             color= 'ANO',
                             line_dash= 'ANO',
                             title= 'Quantidade mensal')
fig_qtd_mensal.update_layout(yaxis_title='QTD')

col1, col2, col3 = st.columns(3)
with col1:
    st.metric('QTD de animais apreendidos',formatar(dados['qt_animais'].count()))

with col2:
    st.metric('Total de ocorrências', formatar(dados.shape[0]))

with col3:
    st.metric('Valor total aplicado de multa',formatar(dados['vl_multa'].sum(), 'R$'))

st.plotly_chart(fig_mapa_quantidade, use_container_width=True)

colu1 , colu2 = st.columns(2)
with colu1:
    st.plotly_chart(fig_qtd_animais, use_container_width=True)

with colu2:
    st.plotly_chart(fig_frep_tipoapreensao, use_container_width=True)

st.plotly_chart(fig_qtd_mensal, use_container_width=True)

st.dataframe(dados)