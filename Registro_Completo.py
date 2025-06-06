import pandas as pd
import streamlit as st
from functions import filter_df, return_unique

df = pd.read_csv('csv_sheets\dados_vendas_acai.csv', parse_dates=['data_venda'])

st.title('Registro de Vendas')
column1, column2, column3, column4 = st.columns(4)

enable_filters = st.checkbox('Filtros', value=False)

if enable_filters:
    with column1:
        date = st.date_input('Data da venda')
        pay_choice = st.selectbox('Forma de pagamento', return_unique(df, 'forma_pagamento'))
    with column2:
        client = st.text_input('Nome do cliente')
        unity_price = float(st.number_input('Preço unitário', min_value=0.0, step=0.01))
    with column3:
        product = st.selectbox('Produto', return_unique(df, 'produto'))
        total_price = float(st.number_input('Valor total', min_value=0.0, step=0.01))
    with column4:
        quantity = int(st.number_input('Quantidade', min_value=0, step=1))
        category = st.selectbox('Categoria', return_unique(df, 'categoria'))
        
else:
    date = None
    client = None
    product = None
    quantity = None
    pay_choice = None
    unity_price = None
    total_price = None
    category = None

filtered_df = filter_df(df, date=date, client=client, product=product, quantity=quantity, pay_choice=pay_choice, unity_price=unity_price, total_price=total_price, category=category)
st.dataframe(filtered_df, key='stDataframe')