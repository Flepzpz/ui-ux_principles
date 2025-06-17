import pandas as pd
import streamlit as st
import plotly.express as px
from numerize import numerize
from functions import create_header

df = create_header()

#st.dataframe(df)

total_products_sold = df['quantidade'].sum()

st.header('Informações Gerais', divider='grey')
col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.metric(
            label='Quantidade total de produtos vendidos',
            value=total_products_sold
        )

with col2:
    with st.container(border=True):
        total_sold_per_product = df.groupby(['produto']).aggregate(quantidade=('quantidade','sum')).reset_index()
        most_sold = total_sold_per_product.iloc[total_sold_per_product['quantidade'].idxmax()]
        most_sold_name = most_sold['produto']
        most_sold_amount = most_sold['quantidade']
        most_sold_percentage = round((most_sold_amount/total_products_sold)*100,1)
        st.metric(
            label='Produto mais vendido',
            value=f'{most_sold_name} | {most_sold_percentage}%'
        )

st.header('Visuazilização dos dados', divider='grey')

amount_sold_per_month = df.groupby(['mes','mes_numero']).aggregate(quantidade=('quantidade','sum')).reset_index()
amount_sold_per_month = amount_sold_per_month.sort_values(by='mes_numero', ascending=True)
line_chart1 = px.line(amount_sold_per_month, x='mes', y='quantidade', markers=True, labels={'mes':'Mês', 'quantidade':'Quantidade'}, title='Quantidade de produtos vendidos por mês')
line_chart1.update_yaxes(ticklabelposition='inside top')
st.plotly_chart(line_chart1)

total_sold_per_product = df.groupby(['produto']).aggregate(quantidade=('quantidade','sum')).reset_index()
bar_chart = px.bar(total_sold_per_product, x='produto', y='quantidade', labels={'produto':'Produto', 'quantidade':'Quantidade'}, title='Quantidade vendida por produto', text='quantidade')
bar_chart.update_yaxes(ticklabelposition='inside top')
st.plotly_chart(bar_chart)

sold_col1, sold_col2 = st.columns(2)

    