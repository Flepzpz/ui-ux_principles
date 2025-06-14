import pandas as pd
import streamlit as st
import plotly.express as px
from functions import return_weekday, return_month, return_unique, return_semester

df = pd.read_csv('csv_sheets\dados_vendas_acai.csv', parse_dates=['data_venda'])

df['dia_semana'] = df['data_venda'].apply(return_weekday)
df['dia_semana_numero'] = df['data_venda'].dt.dayofweek
df['mes'] = df['data_venda'].apply(return_month)
df['mes_numero'] = df['data_venda'].dt.month
df['ano'] = df['data_venda'].dt.year
df['hora'] = df['data_venda'].dt.hour
df['trimestre'] = df['data_venda'].dt.quarter
df['semestre'] = df['trimestre'].apply(return_semester)

df = df.drop(index=df.loc[df['mes'] == 'Junho'].index)

st.dataframe(df)

year = df['ano'].mode().iloc[0]
semester = df['semestre'].mode().iloc[0]
st.title(f'Visualização de Vendas ({year}/{semester})')
st.caption('Para todos os efeitos o mês de junho foi desconsiderado por não ter fechado suas vendas mensais.')

st.header('Informações Gerais', divider='grey')
column1, column2, column3 = st.columns(3)

with column1:
    st.subheader('Número de Vendas')
    total_sales = df.shape[0]
    st.markdown(f'<div class="big_numbers_container"><p>Total de Vendas</p><p class="big_numbers">{total_sales}</p></div>', unsafe_allow_html=True)

    frequency_per_product = df['produto'].value_counts().reset_index()
    most_frequent = frequency_per_product.iloc[frequency_per_product['count'].idxmax()]
    most_frequent_name = most_frequent['produto']
    most_frequent_quantity = most_frequent['count']
    most_frequent_percentage = round((most_frequent_quantity/total_sales)*100,1)
    st.markdown(f'<div class="big_numbers_container"><p>Produto Mais Frequente</p><p class="big_numbers">{most_frequent_name} - {most_frequent_quantity}/{most_frequent_percentage}%</p></div>', unsafe_allow_html=True)

        

with column2:
    st.subheader('Receita')
    total_income = df['valor_total'].sum()
    st.markdown(f'<div class="big_numbers_container"><p>Receita Total</p><p class="big_numbers">R${round(total_income,2)}</p></div>', unsafe_allow_html=True)

    income_per_product = df.groupby(['produto']).aggregate(receita=('valor_total','sum')).reset_index()
    most_income = income_per_product.iloc[income_per_product['receita'].idxmax()]
    most_income_name = most_income['produto']
    most_income_amount = round(most_income['receita'],2)
    most_income_percentage = round((most_income_amount/total_income)*100,1)
    st.markdown(f'<div class="big_numbers_container"><p>Produto Mais Lucrativo</p><p class="big_numbers">{most_income_name} - R${most_income_amount}/{most_income_percentage}%</p></div>', unsafe_allow_html=True)
    #mean_ticket = float(df['valor_total'].mean())
    

with column3:
    st.subheader('Quantidade de Produtos')
    total_amount = df['quantidade'].sum()
    st.markdown(f'<div class="big_numbers_container"><p>Quantidade Total de Produtos Vendidos</p><p class="big_numbers">{total_amount}</p></div>', unsafe_allow_html=True)

    sales_per_product = df.groupby(['produto']).aggregate(quantidade=('quantidade','sum')).reset_index()
    most_sold = sales_per_product.iloc[sales_per_product['quantidade'].idxmax()]
    most_sold_name = most_sold['produto']
    most_sold_quantity = most_sold['quantidade']
    most_sold_percentage = round((most_sold_quantity/total_amount)*100,1)
    st.markdown(f'<div class="big_numbers_container"><p>Produto Mais Vendido</p><p class="big_numbers">{most_sold_name} - {most_sold_quantity}/{most_sold_percentage}%</p></div>', unsafe_allow_html=True)

st.divider()

st.header('Vendas', divider='grey')
sales_column1, sales_column2 = st.columns(2)

with sales_column1:
    sales_per_month = df.groupby(['mes','mes_numero']).aggregate(vendas=('mes','count')).reset_index()
    sales_per_month = sales_per_month.sort_values(by='mes_numero', ascending=True)
    line_chart1 = px.line(sales_per_month, x='mes', y='vendas', markers=True, labels={'mes':'Mês', 'vendas':'Vendas'}, title='Vendas Mensais')
    line_chart1 = line_chart1.update_yaxes(ticklabelposition="inside top")
    st.plotly_chart(line_chart1)

with sales_column2:
    pass

st.header('Receita', divider='grey')
income_column1, income_column2 = st.columns(2)

with income_column1:
    income_per_month = df.groupby(['mes','mes_numero']).aggregate(receita=('valor_total','sum')).reset_index()
    income_per_month = income_per_month.sort_values(by='mes_numero', ascending=True)
    line_chart2 = px.line(income_per_month, x='mes', y='receita', markers=True, labels={'mes':'Mês', 'receita':'Receita'}, title='Receita Mensal')
    line_chart2 = line_chart2.update_yaxes(ticklabelposition="inside top")
    st.plotly_chart(line_chart2)

st.header('Produtos', divider='grey')
product_column1, product_column2 = st.columns(2)

with product_column1:
    sales_per_product = df.groupby(['produto']).aggregate(quantidade=('quantidade','sum')).reset_index()
    pie_chart1 = px.pie(sales_per_product, values='quantidade', names='produto', title='Produtos mais vendidos (quantidade)', color_discrete_sequence=px.colors.sequential.Blues_r)
    pie_chart1.update_traces(textposition='outside', textinfo='percent+label')
    st.plotly_chart(pie_chart1)

    st.divider()



with product_column2:
    frequency_per_product = df['produto'].value_counts().reset_index()
    pie_chart2 = px.pie(frequency_per_product, values='count', names='produto', title='Produtos mais vendidos (frequência)', color_discrete_sequence=px.colors.sequential.Blues_r)
    pie_chart2.update_traces(textposition='outside', textinfo='percent+label')
    st.plotly_chart(pie_chart2)

    st.divider()

st.header('Clientes', divider='grey')
