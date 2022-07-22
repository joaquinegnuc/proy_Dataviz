import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

df = pd.read_csv("data_sales.csv",sep=",",decimal=".")
df = pd.read_csv("data_sales.csv",sep=",",decimal=".")
df = df[['Order Date','Segment','Country','State','Category','Sales']]
df = df[df['Sales'] < df['Sales'].quantile(.95)]
df = df[df['Sales'] > df['Sales'].quantile(.05)]
st.markdown('## Dashboard Ventas Super Store')
st.markdown('###### Super Store es una pequeña tienda de ventas minoristas, ubicados en USA. Ellos venden muebles, artículos de oficinas y productos de tecnologías.')
st.markdown('###### Los datos que contiene el dataset son los siguientes:')
st.markdown('- Order Date: Fecha creación de la Orden')
st.markdown('- Segment: Segmento del Cliente (Consumer, Corporate, Home Office)')
st.markdown('- State: Estado de despacho')
st.markdown('- Category: Categoría del producto')
st.markdown('- Sales: Venta Total ($ USD)')
df = df[['Order Date','Segment','Country','State','Category','Sales']]

st.write(df.head(5))


c = alt.Chart(df,title="Distribución total ventas ($USD)").mark_bar().encode(
    alt.X("Sales:Q", title='Total Sales ($USD)',bin=alt.Bin(extent=[df.Sales.min(), df.Sales.max()], step=50)),
    alt.Y('count()',title = 'Frequency'),
    #y='count()',
)
st.altair_chart(c, use_container_width=True)


#st.header("Dashboard Ventas Super Store")
#st.subheader("") 

#st.write('# Hello World from 1littlecoder, please subscribe')
