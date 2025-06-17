import pandas as pd
import streamlit as st
import plotly.express as px
from numerize import numerize
from functions import create_header

df = create_header()

#st.dataframe(df)

total_sales = df.shape[0]

st.header('Informações Gerais', divider='grey')
col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.metric(
            label='Número de vendas',
            value=total_sales
        )

    with st.container(border=True):
        category_frequency = df.groupby(['categoria']).aggregate(vendas=('valor_total','count')).reset_index()
        most_frequent_category = category_frequency.iloc[category_frequency['vendas'].idxmax()]
        most_frequent_name = most_frequent_category['categoria']
        most_frequent_amount = most_frequent_category['vendas']
        most_frequent_percentage = round((most_frequent_amount/total_sales)*100, 2)
        st.metric(
            label='Categoria mais frequente',
            value=f'{most_frequent_name} | {most_frequent_percentage}%'
        )

with col2:
    with st.container(border=True):
        product_frequency = df.groupby(['produto']).aggregate(vendas=('valor_total','count')).reset_index()
        most_frequent_product = product_frequency.iloc[product_frequency['vendas'].idxmax()]
        most_frequent_name = most_frequent_product['produto']
        most_frequent_amount = most_frequent_product['vendas']
        most_frequent_percentage = round((most_frequent_amount/total_sales)*100, 2)
        st.metric(
            label='Produto mais frequente',
            value=f'{most_frequent_name} | {most_frequent_percentage}%'
        )

st.header('Visuazilização dos dados', divider='grey')

# Evolução do número de vendas através dos meses
sales_per_month = df.groupby(['mes','mes_numero']).aggregate(vendas=('valor_total','count')).reset_index()
sales_per_month = sales_per_month.sort_values(by='mes_numero', ascending=True)
line_chart1 = px.line(sales_per_month, x='mes', y='vendas', markers=True, labels={'mes':'Mês', 'vendas':'Vendas'}, title='Vendas mensais')
line_chart1.update_yaxes(ticklabelposition='inside top')
st.plotly_chart(line_chart1)

# Evolução do número de vendas através dos meses
sales_per_weekday = df.groupby(['dia_semana','dia_semana_numero']).aggregate(vendas=('valor_total','count')).reset_index()
sales_per_weekday = sales_per_weekday.sort_values(by='dia_semana_numero', ascending=True)
line_chart2 = px.line(sales_per_weekday, x='dia_semana', y='vendas', markers=True, labels={'dia_semana':'Dia da semana', 'vendas':'Vendas'}, title='Vendas por dia da semana')
line_chart2.update_yaxes(ticklabelposition='inside top')
st.plotly_chart(line_chart2)

sales_per_hour = df.groupby(['hora']).aggregate(vendas=('valor_total','count')).reset_index().sort_values(by='hora', ascending=True)
line_chart3 = px.line(sales_per_hour, x='hora', y='vendas', markers=True, labels={'hora':'Hora do dia', 'vendas':'Vendas'}, title='Vendas por hora do dia')
line_chart3.update_yaxes(ticklabelposition='inside top')
st.plotly_chart(line_chart3)