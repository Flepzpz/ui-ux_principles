import pandas as pd
import streamlit as st
import plotly.express as px
from numerize import numerize
from functions import create_header

df = create_header()

#st.dataframe(df)

# Total
total_income = df['valor_total'].sum()
show_total_income = numerize.numerize(total_income)

# Ticket médio
mean_ticket = round(df['valor_total'].mean(), 2)

st.header('Informações Gerais', divider='grey')
col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
       st.metric(
            label='Receita total',
            value=f'R${show_total_income}'
        )
    
    with st.container(border=True):
        # Forma de pagamento mais lucrativa
        pay_choice = df.groupby(['forma_pagamento']).aggregate(receita=('valor_total','sum')).reset_index()
        most_income = pay_choice.iloc[pay_choice['receita'].idxmax()]
        most_income_name = most_income['forma_pagamento']
        most_income_amount = round(most_income['receita'],2)
        show_most_income_amout = numerize.numerize(most_income_amount)
        most_income_percentage = round((most_income_amount/total_income)*100,1)
        st.metric(
            label='Forma de pagamento mais lucrativa',
            value=f'{most_income_name} | {most_income_percentage}%'
        )
    

with col2:
    with st.container(border=True):
        st.metric(
            label='Ticket médio',
            value=f'R${mean_ticket}'
        )

    with st.container(border=True):
        # Produto mais lucrativo
        income_per_product = df.groupby(['produto']).aggregate(receita=('valor_total','sum')).reset_index()
        most_income = income_per_product.iloc[income_per_product['receita'].idxmax()]
        most_income_name = most_income['produto']
        most_income_amount = round(most_income['receita'],2)
        show_most_income_amout = numerize.numerize(most_income_amount)
        most_income_percentage = round((most_income_amount/total_income)*100,1)
        st.metric(
            label='Produto mais lucrativo',
            value=f'{most_income_name} | {most_income_percentage}%'
        )

st.header('Visuazilização dos dados', divider='grey')

# Evolução da receita através dos meses
income_per_month = df.groupby(['mes','mes_numero']).aggregate(receita=('valor_total','sum')).reset_index()
income_per_month = income_per_month.sort_values(by='mes_numero', ascending=True)
line_chart1 = px.line(income_per_month, x='mes', y='receita', markers=True, labels={'mes':'Mês', 'receita':'Receita'}, title='Receita mensal')
line_chart1.update_yaxes(ticklabelposition='inside top')
st.plotly_chart(line_chart1)

income_column1, income_column2 = st.columns(2)

with income_column1:
    # Comparação da receita por produto
    income_per_product = df.groupby(['produto']).aggregate(receita=('valor_total','sum')).reset_index()
    bar_chart = px.bar(income_per_product, x='produto', y='receita', labels={'receita':'Receita', 'produto':'Produto'}, title='Receita por produto', text='receita')
    bar_chart.update_yaxes(ticklabelposition='inside top')
    st.plotly_chart(bar_chart)

    # Ticket médio por forma de pagamento
    income_per_pay_choice = df.groupby(['forma_pagamento']).aggregate(ticket_medio=('valor_total', 'mean')).reset_index()
    income_per_pay_choice['ticket_medio'] = income_per_pay_choice['ticket_medio'].round(2)
    bar_chart = px.bar(income_per_pay_choice, x='forma_pagamento', y='ticket_medio', labels={'ticket_medio':'Ticket médio', 'forma_pagamento':'Forma de pagamento'}, title='Ticket médio por forma de pagamento', text='ticket_medio')
    bar_chart.update_yaxes(ticklabelposition='inside top')
    st.plotly_chart(bar_chart)

with income_column2:
    # Comparação da receita por forma de pagamento
    income_per_pay_choice = df.groupby(['forma_pagamento']).aggregate(receita=('valor_total', 'sum')).reset_index()
    bar_chart = px.bar(income_per_pay_choice, x='forma_pagamento', y='receita', labels={'receita':'Receita', 'forma_pagamento':'Forma de pagamento'}, title='Receita por forma de pagamento', text='receita')
    bar_chart.update_yaxes(ticklabelposition='inside top')
    st.plotly_chart(bar_chart)