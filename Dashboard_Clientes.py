import pandas as pd
import streamlit as st
import plotly.express as px
from numerize import numerize
from functions import create_header

df = create_header()

st.dataframe(df)

unique_clients = df['cliente'].nunique()

st.header('Informações Gerais', divider='grey')
_, col1, _ = st.columns(3)
col2, col3, col4 = st.columns(3)

with col1:
    with st.container(border=True):
        st.metric(
            label='Número de clientes únicos',
            value=unique_clients
        )

with col2:
    with st.container(border=True):
        revenue_per_client = df.groupby(['cliente']).aggregate(receita=('valor_total','sum')).reset_index()
        most_profitable_client = revenue_per_client.iloc[revenue_per_client['receita'].idxmax()]
        most_profitable_name = most_profitable_client['cliente']
        most_profitable_amount = most_profitable_client['receita']
        total = df['valor_total'].sum()
        most_profitable_percentage = round((most_profitable_amount/total)*100, 2)
        st.metric(
            label='Cliente mais lucrativo',
            value=f'{most_profitable_name} | {most_profitable_percentage}%'
        )

with col3:
    with st.container(border=True):
        buys_per_client = df.groupby(['cliente']).aggregate(compras=('valor_total','count')).reset_index()
        most_frequent_client = buys_per_client.iloc[buys_per_client['compras'].idxmax()]
        most_frequent_name = most_frequent_client['cliente']
        most_frequent_amount = most_frequent_client['compras']
        total = df.shape[0]
        most_frequent_percentage = round((most_frequent_amount/total)*100, 2)
        st.metric(
            label='Cliente mais frequente',
            value=f'{most_frequent_name} | {most_frequent_percentage}%'
        )

with col4:
    with st.container(border=True):
        amount_per_client = df.groupby(['cliente']).aggregate(quantidade=('quantidade','sum')).reset_index()
        biggest_buyer = amount_per_client.iloc[amount_per_client['quantidade'].idxmax()]
        biggest_buyer_name = biggest_buyer['cliente']
        biggest_buyer_amount = biggest_buyer['quantidade']
        total = df['quantidade'].sum()
        biggest_buyer_percentage = round((biggest_buyer_amount/total)*100, 2)
        st.metric(
            label='Maior comprador',
            value=f'{biggest_buyer_name} | {biggest_buyer_percentage}%'
        )

st.header('Visuazilização dos dados', divider='grey')

mean_ticket_per_client = df.groupby(['cliente']).aggregate(ticket_medio=('valor_total','mean')).reset_index().sort_values(by='ticket_medio', ascending=False).head(10)
mean_ticket_per_client['ticket_medio'] = mean_ticket_per_client['ticket_medio'].round(2)
barchart = px.bar(mean_ticket_per_client, x='cliente', y='ticket_medio', labels={'cliente':'Cliente', 'ticket_medio':'Ticket Médio'}, title='Top 10 ticket médio por cliente', text='ticket_medio')
st.plotly_chart(barchart)