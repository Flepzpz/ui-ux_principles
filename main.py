import pandas as pd
import streamlit as st
import plotly.express as px
from functions import filter_df

st.set_page_config(layout='wide')

with open('styles/style.css') as file:
    css = file.read()
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

pg = st.navigation(['Registro_Completo.py', 'Dashboard_Vendas.py', 'Dashboard_Receita.py', 'Dashboard_Produtos.py', 'Dashboard_Categorias.py', 'Dashboard_Clientes.py', 'Lista_de_Produtos.py'])
pg.run()

