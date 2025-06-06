import pandas as pd
import streamlit as st
import plotly.express as px
from functions import create_header

df = create_header()

total_income = df['valor_total'].sum()

# Produto mais lucrativo
income_per_product = df.groupby(['produto']).aggregate(receita=('valor_total','sum')).reset_index()
most_income = income_per_product.iloc[income_per_product['receita'].idxmax()]
most_income_name = most_income['produto']
most_income_amount = round(most_income['receita'],2)
most_income_percentage = round((most_income_amount/total_income)*100,1)

st.header('Informações Gerais', divider='grey')
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label='Receita Total',
        value=total_income
    )

with col2:
  pass
    

with col3:
    pass

st.divider()