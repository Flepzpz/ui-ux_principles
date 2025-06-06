import pandas as pd
import streamlit as st
import plotly.express as px
from functions import return_weekday, return_month, return_unique

df = pd.read_csv('csv_sheets\dados_vendas_acai.csv', parse_dates=['data_venda'])
df['dia_semana'] = df['data_venda'].apply(return_weekday)
df['mes'] = df['data_venda'].apply(return_month)
df['ano'] = df['data_venda'].dt.year
df['hora'] = df['data_venda'].dt.hour
st.dataframe(df)

st.title('Visualização de Vendas')

st.header('Informações Gerais', divider='grey')
column1, column2, column3 = st.columns(3)

with column1:
    total_sales = df.shape[0]
    st.markdown(f'<div class="big_numbers_container"><p>Total de Vendas</p><p class="big_numbers">{total_sales}</p></div>', unsafe_allow_html=True)

with column2:
    mean_ticket = df['valor_total'].mean()
    st.markdown(f'<div class="big_numbers_container"><p>Ticket Médio</p><p class="big_numbers">{mean_ticket}</p></div>', unsafe_allow_html=True)

with column3:
    total_amount = df['quantidade'].sum()
    st.markdown(f'<div class="big_numbers_container"><p>Quantidade Total Vendida</p><p class="big_numbers">{total_amount}</p></div>', unsafe_allow_html=True)

st.divider()