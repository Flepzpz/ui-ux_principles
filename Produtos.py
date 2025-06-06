import pandas as pd
import streamlit as st
from functions import filter_df, return_unique

df = pd.read_csv('csv_sheets\dados_vendas_acai.csv', parse_dates=['data_venda'])

df = df.groupby(['produto']).aggregate(preco=('preco_unitario','mean'), categoria=('categoria',lambda x: x.mode()[0])).reset_index()

st.title('Lista de Produtos')
st.dataframe(df)