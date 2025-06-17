import pandas as pd
import streamlit as st
import plotly.express as px
from numerize import numerize
from functions import create_header

df = create_header()

#st.dataframe(df)

# Total
total_revenue = df['valor_total'].sum()
show_total_revenue = numerize.numerize(total_revenue)

# Ticket médio
mean_ticket = round(df['valor_total'].mean(), 2)

st.header('Informações Gerais', divider='grey')
col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
       st.metric(
            label='Receita total',
            value=f'R${show_total_revenue}'
        )
    
    with st.container(border=True):
        # Forma de pagamento mais lucrativa
        pay_choice = df.groupby(['forma_pagamento']).aggregate(receita=('valor_total','sum')).reset_index()
        most_revenue = pay_choice.iloc[pay_choice['receita'].idxmax()]
        most_revenue_name = most_revenue['forma_pagamento']
        most_revenue_amount = round(most_revenue['receita'],2)
        show_most_revenue_amout = numerize.numerize(most_revenue_amount)
        most_revenue_percentage = round((most_revenue_amount/total_revenue)*100,1)
        st.metric(
            label='Forma de pagamento mais lucrativa',
            value=f'{most_revenue_name} | {most_revenue_percentage}%'
        )

    with st.container(border=True):
        revenue_per_category = df.groupby(['categoria']).aggregate(receita=('valor_total','sum')).reset_index()
        most_revenue = revenue_per_category.iloc[revenue_per_category['receita'].idxmax()]
        most_revenue_name = most_revenue['categoria']
        most_revenue_amount = round(most_revenue['receita'],2)
        show_most_revenue_amout = numerize.numerize(most_revenue_amount)
        most_revenue_percentage = round((most_revenue_amount/total_revenue)*100,1)
        st.metric(
            label='Categoria mais lucrativa',
            value=f'{most_revenue_name} | {most_revenue_percentage}%'
        )
    

with col2:
    with st.container(border=True):
        st.metric(
            label='Ticket médio',
            value=f'R${mean_ticket}'
        )

    with st.container(border=True):
        # Produto mais lucrativo
        revenue_per_product = df.groupby(['produto']).aggregate(receita=('valor_total','sum')).reset_index()
        most_revenue = revenue_per_product.iloc[revenue_per_product['receita'].idxmax()]
        most_revenue_name = most_revenue['produto']
        most_revenue_amount = round(most_revenue['receita'],2)
        show_most_revenue_amout = numerize.numerize(most_revenue_amount)
        most_revenue_percentage = round((most_revenue_amount/total_revenue)*100,1)
        st.metric(
            label='Produto mais lucrativo',
            value=f'{most_revenue_name} | {most_revenue_percentage}%'
        )

st.header('Visuazilização dos dados', divider='grey')

# Evolução da receita através dos meses
revenue_per_month = df.groupby(['mes','mes_numero']).aggregate(receita=('valor_total','sum')).reset_index()
revenue_per_month = revenue_per_month.sort_values(by='mes_numero', ascending=True)
line_chart1 = px.line(revenue_per_month, x='mes', y='receita', markers=True, labels={'mes':'Mês', 'receita':'Receita'}, title='Receita mensal')
line_chart1.update_yaxes(ticklabelposition='inside top')
st.plotly_chart(line_chart1)

# Comparação da receita por produto
revenue_per_product = df.groupby(['produto']).aggregate(receita=('valor_total','sum')).reset_index()
bar_chart = px.bar(revenue_per_product, x='produto', y='receita', labels={'receita':'Receita', 'produto':'Produto'}, title='Receita por produto', text='receita')
bar_chart.update_yaxes(ticklabelposition='inside top')
st.plotly_chart(bar_chart)


revenue_column1, revenue_column2 = st.columns(2)

with revenue_column1:
    # Comparação da receita por forma de pagamento
    revenue_per_pay_choice = df.groupby(['forma_pagamento']).aggregate(receita=('valor_total', 'sum')).reset_index()
    bar_chart = px.bar(revenue_per_pay_choice, x='forma_pagamento', y='receita', labels={'receita':'Receita', 'forma_pagamento':'Forma de pagamento'}, title='Receita por forma de pagamento', text='receita')
    bar_chart.update_yaxes(ticklabelposition='inside top')
    st.plotly_chart(bar_chart)

    # Comparação de receita por categoria
    revenue_per_category = df.groupby(['categoria']).aggregate(receita=('valor_total','sum')).reset_index()
    bar_chart = px.bar(revenue_per_category, x='categoria', y='receita', labels={'categoria':'Categoria', 'receita':'Receita'}, title='Receita por categoria', text='receita')
    bar_chart = bar_chart.update_yaxes(ticklabelposition='inside top')
    st.plotly_chart(bar_chart)

with revenue_column2:
    # Ticket médio por forma de pagamento
    revenue_per_pay_choice = df.groupby(['forma_pagamento']).aggregate(ticket_medio=('valor_total', 'mean')).reset_index()
    revenue_per_pay_choice['ticket_medio'] = revenue_per_pay_choice['ticket_medio'].round(2)
    bar_chart = px.bar(revenue_per_pay_choice, x='forma_pagamento', y='ticket_medio', labels={'ticket_medio':'Ticket médio', 'forma_pagamento':'Forma de pagamento'}, title='Ticket médio por forma de pagamento', text='ticket_medio')
    bar_chart.update_yaxes(ticklabelposition='inside top')
    st.plotly_chart(bar_chart)

    # Ticket médio por categoria
    revenue_per_category = df.groupby(['categoria']).aggregate(ticket_medio=('valor_total','mean')).reset_index()
    revenue_per_category['ticket_medio'] = revenue_per_category['ticket_medio'].round(2)
    bar_chart = px.bar(revenue_per_category, x='categoria', y='ticket_medio', labels={'categoria':'Categoria', 'ticket_medio':'Receita'}, title='Ticket médio por categoria', text='ticket_medio')
    bar_chart = bar_chart.update_yaxes(ticklabelposition='inside top')
    st.plotly_chart(bar_chart)