import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

df = pd.read_csv("data_sales.csv",sep=",",decimal=".")
df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d/%m/%Y')
df = df[['Order Date','Segment','State','Category','Sub-Category','Sales']]
df = df[df['Sales'] < df['Sales'].quantile(.95)]
df = df[df['Sales'] > df['Sales'].quantile(.05)]
df['month_year'] = df['Order Date'].dt.to_period('M').astype(str)
df_sales_group = df.groupby(by=['month_year','Segment','Category','State'], dropna=False).sum('Sales')
df_sales_group.reset_index(drop=False,inplace=True)
states = df_sales_group.State.unique()
segments = df_sales_group.Segment.unique()

st.markdown('## Dashboard Ventas Super Store')
st.markdown('###### Reporte Ventas por Segmento Cliente y Estado')
st.markdown('###### Información de ventas desde 2015 a 2018, con frecuencia mensual')
st.markdown('- Segment: Segmento del Cliente (Consumer, Corporate, Home Office)')
st.markdown('- State: Estado de despacho')
st.markdown('- Category: Categoría del producto (Furniture, Office Supplies, Technology)')
df = df[['Order Date','Segment','State','Category','Sales']]

#st.write(df.head(5))

state_choice = st.sidebar.selectbox('Selecciona Estado:', states)
segment_choice = st.sidebar.selectbox('Selecciona Segmento:', segments)

c = alt.Chart(df_sales_group[(df_sales_group.State == state_choice) & (df_sales_group.Segment == segment_choice)],title="Ventas Mensuales por Categorías").mark_area().encode(
    x=alt.X("month_year:T",title='Fecha'),
    y=alt.Y("sum(Sales):Q",title='Ventas Totales ($USD)'),
    color="Category:N"
)
st.altair_chart(c, use_container_width=True)

d= alt.Chart(df_sales_group[(df_sales_group.State == state_choice) & (df_sales_group.Segment == segment_choice)],title="Ventas Porcentuales por Categorías").transform_joinaggregate(
    TotalSales='sum(Sales)',).transform_calculate(
    PercentOfTotal="datum.Sales / datum.TotalSales").mark_bar().encode(
    alt.X('PercentOfTotal:Q', axis=alt.Axis(format='.0%'),title='Porcentaje de Ventas del Total ($USD)'),
    y=alt.Y('Category:N',title='Categorías')
  )
st.altair_chart(d, use_container_width=True)