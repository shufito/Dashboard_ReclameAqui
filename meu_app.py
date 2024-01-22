import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Reclame Aqui")

st.title("RECLAME AQUI DASHBOARD")

barra_lateral = st.sidebar

dados = pd.read_csv("RECLAMEAQUI.csv")
dados['Num_Caracteres'] = dados['DESCRICAO'].apply(len)

lista_estado=list(dados['ESTADO'].unique())
estado = barra_lateral.selectbox(
    'SELECIONE O ESTADO',
    lista_estado)

lista_empresa=list(dados['Empresa'].unique())
empresa = barra_lateral.selectbox(
    'SELECIONE A EMPRESA',
    lista_empresa)

lista_status=list(dados['STATUS'].unique())
status = barra_lateral.multiselect(
    'SELECIONE OS STATSUS',
    lista_status,
    lista_status)

Start = dados['Num_Caracteres'].min().astype(int)
End = dados['Num_Caracteres'].max().astype(int)
Mid = dados['Num_Caracteres'].mean().astype(int)

NumCaracteres = barra_lateral.slider('Número de caracteres',Start,End,Mid)

container = st.container()
col1, col2, col3, col4, col5 = container.columns(5)

cards = dados[(dados['ESTADO'] == estado) & (dados['Empresa'] == empresa)]

with col1:
        st.metric(label='Respondida', value=cards['STATUS'].value_counts()['Respondida'])
with col2:       
        st.metric(label='Resolvido',value=cards['STATUS'].value_counts()['Resolvido'])
with col3:       
        st.metric(label='Não respondida',value=cards['STATUS'].value_counts()['Não respondida'])
with col4:       
        st.metric(label='Em réplica',value=cards['STATUS'].value_counts()['Em réplica'])
with col5:       
        st.metric(label='Não resolvido',value=cards['STATUS'].value_counts()['Não resolvido'])

df_filtrado = dados[(dados['ESTADO'] == estado) & (dados['Empresa'] == empresa) & (dados['STATUS'].isin(status))]
media_contagem = df_filtrado.groupby(['TEMPO'])['ID'].nunique().mean()
df_contagem_casos = df_filtrado.groupby('TEMPO')['ID'].nunique()
df_contagem_casos = df_contagem_casos[df_contagem_casos > media_contagem].reset_index(name='NumeroReclamacoes')
fig_serie_temporal = px.line(df_contagem_casos, x='TEMPO', y='NumeroReclamacoes', title='Série Temporal de Reclamações ('+empresa+' - '+estado+')')
st.plotly_chart(fig_serie_temporal)


fig_estados = px.histogram(dados, x='ESTADO', title='Frequência de Reclamações por Estado', category_orders={'ESTADO': dados['ESTADO'].value_counts().index})
st.plotly_chart(fig_estados)

fig_status = px.histogram(df_filtrado, x='STATUS', title='Frequência de status ('+empresa+' - '+estado+')', category_orders={'STATUS': dados['STATUS'].value_counts().index})
st.plotly_chart(fig_status)


df_filtrado_palavras = df_filtrado[df_filtrado['Num_Caracteres'] <= NumCaracteres]
fig_palavras = px.histogram(df_filtrado_palavras, x='Num_Caracteres', title='Distribuição do Tamanho do Texto')
st.plotly_chart(fig_palavras)