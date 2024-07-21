import streamlit as st
import pandas as pd
import altair as alt
from utils import *
from visualizaciones import * 
# Datos

salida_autores = pd.read_excel("data/salida_autores.xlsx")
salida_articulos = pd.read_excel("data/output_articles.xlsx")
salida_revistas = pd.read_excel("data/salida_revistas.xlsx")
salida_filiaciones = pd.read_excel("data/salida_filiaciones.xlsx")
salida_topicos = pd.read_excel("data/salidas_topicos_CB.xlsx")
salida_authorrank = pd.read_excel("data/salida_AuthorRank.xlsx",index_col= 0)

st.set_page_config(page_title="Dashboard de Bibliometría de psicología en Chile entre los años 2015 a 2020", layout="wide")


st.title("Dashboard de Bibliometría de psicología en Chile entre los años 2015 a 2020")

num_autores, num_articulos, n_autores_por_paper, n_paper_por_autores = principales_indicadores(salida_autores, salida_articulos)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Número de autores", num_autores)

with col2:
    st.metric("Número de artículos", num_articulos)

with col3:
    st.metric("Autores por paper", round(n_autores_por_paper, 2))

with col4:
    st.metric("Paper por autores", round(n_autores_por_paper, 2))

st.subheader("Análisis de datos bibliométricos utilizando gráficos interactivos")

top_autores = n_articulos_por_autor(salida_autores)
filiaciones_ordenadas = paper_por_filiacion(salida_filiaciones)
revistas_ordenadas = paper_por_revistas(salida_revistas)

grafico_autores = crear_grafico_autores(top_autores)
grafico_filiaciones = crear_grafico_filiaciones(filiaciones_ordenadas)
grafico_revistas = crear_grafico_revistas(revistas_ordenadas)

col1, col2, col3 = st.columns(3)

with col1:
    st.altair_chart(grafico_autores, use_container_width=True)

with col2:
    st.altair_chart(grafico_filiaciones, use_container_width=True)

with col3:
    st.altair_chart(grafico_revistas, use_container_width=True)

st.markdown("""
    ### Artículos por año y proporción de artículos en ingles y español por año
""")

frecuencia_por_año = paper_por_año(salida_articulos)
df_resultado = prop_idiomas_por_año(salida_articulos)
df_resultado = df_resultado[['Año','Art_es', 'Art_en']]
df_agrupado_total = generar_df_agrupado_total(salida_articulos, salida_topicos)

grafico_articulos_por_año = crear_grafico_articulos_por_año(frecuencia_por_año)
grafico_idiomas_por_año = crear_grafico_idiomas_por_año(df_resultado)
grafico_publicaciones_area = crear_grafico_publicaciones_area(df_agrupado_total)
col4, col5 = st.columns(2)

# Mostrar los gráficos en las columnas
with col4:
    st.altair_chart(grafico_articulos_por_año, use_container_width=True)

with col5:
    st.altair_chart(grafico_idiomas_por_año, use_container_width=True)

st.altair_chart(grafico_publicaciones_area, use_container_width=True)
