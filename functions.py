import pandas as pd
import streamlit as st
import plotly.express as px
import sqlite3


def filter_df(df, date=None, client=None, product=None, quantity=None, pay_choice=None, unity_price=None, total_price=None, category=None):

    if date is not None:
        df = df.loc[df['data_venda'].dt.date == date]
    if client is not None and client != '':
        df = df.loc[df['cliente'].str.contains(client)]
    if product is not None and product != 'Todos':
        df = df.loc[df['produto'] == product]
    if quantity is not None and quantity > 0:
        df = df.loc[df['quantidade'] == quantity]
    if pay_choice is not None and pay_choice != 'Todos':
        df = df.loc[df['forma_pagamento'] == pay_choice]
    if unity_price is not None and unity_price > 0.0:
        df = df.loc[df['preco_unitario'] == unity_price]
    if total_price is not None and total_price > 0.0:
        df = df.loc[df['valor_total'] == total_price]
    if category is not None and category != 'Todos':
        df = df.loc[df['categoria'] == category]
    
    return df

def return_unique(df, column):
    choices = ['Todos']
    choices.extend(df[column].unique())
    return tuple(choices)

def return_weekday(date):
    
    match date.dayofweek:
        case 0:
            return 'Segunda'
        case  1:
            return 'Terça'
        case 2:
            return 'Quarta'
        case 3:
            return 'Quinta'
        case 4:
            return 'Sexta'
        case 5:
            return 'Sábado'
        case 6:
            return 'Domingo'
        
def return_month(date):

    match date.month:
        case 1:
            return 'Janeiro'
        case 2:
            return 'Fevereiro'
        case 3:
            return 'Março'
        case 4:
            return 'Abril'
        case 5:
            return 'Maio'
        case 6:
            return 'Junho'
        case 7:
            return 'Julho'
        case 8:
            return 'Agosto'
        case 9:
            return 'Setembro'
        case 10:
            return 'Outubro'
        case 11:
            return 'Novembro'
        case 12:
            return 'Dezembro'