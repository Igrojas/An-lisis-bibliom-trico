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

st.set_page_config(page_title="Estudio Bibliométrico de la Actividad Científica en Psicología en Chile (2015-2020)", layout="wide")

st.title("Estudio Bibliométrico de la Actividad Científica en Psicología en Chile (2015-2020)")

st.markdown("""
Los resultados que se presentan a continuación corresponden a los obtenidos en mi memoria de título llamada Estudio Bibliométrico de las Redes de Coautoría de la Literatura en Psicología de Chile en el Período 2015-2020 para el Proyecto FONDECYT Regular 1201681
""")
st.write("""
El objetivo de este proyecto es realizar un estudio bibliométrico de la actividad científica en psicología en Chile durante el período de 2015 a 2020.
Utilizando datos de las reconocidas bases de datos Scielo, Scopus y WoS, este análisis se enfoca en la productividad y las redes sociales basadas en la coautoría.
""")
st.write("""
Este tipo de estudio permite obtener una perspectiva cuantitativa de la producción científica en el área de la psicología,
lo cual puede ser de gran utilidad para la toma de decisiones y la planificación estratégica en la investigación psicológica.
""")
st.write("""
Se recopilaron y analizaron datos de artículos publicados en las bases de datos mencionadas,
focalizándose en las redes de coautoría y en la productividad científica de los investigadores chilenos en psicología.
""")
st.write("""
Los resultados obtenidos proporcionan una visión detallada de la evolución de la actividad científica en psicología en Chile,
identificando las principales áreas de investigación, así como las colaboraciones entre investigadores y las instituciones más productivas.
""")
st.write("""
El análisis bibliométrico realizado ofrece valiosa información para la comunidad científica y las autoridades académicas,
facilitando la planificación de estrategias futuras en el ámbito de la investigación en psicología.
""")

st.write("""  
-------------------------------------------
""")

st.header("""
A continuación se muestran los principales indicadores bibliométricos""")

num_autores, num_articulos, n_autores_por_paper, n_paper_por_autores = principales_indicadores(salida_autores, salida_articulos)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Número de autores", num_autores)

with col2:
    st.metric("Número de artículos", num_articulos)

with col3:
    st.metric("Autores por paper", round(n_autores_por_paper, 2))

with col4:
    st.metric("Paper por autores", round(n_paper_por_autores, 2))

st.header("Análisis de datos bibliométricos utilizando gráficos interactivos")
st.subheader("Análisis de Productores, Afiliaciones y Revistas Más Productivas")
st.write("""
Entre los mayores productores con afiliación chilena, Agustín Ibáñez encabeza la lista con 60 artículos científicos, de los cuales 59 están firmados por investigadores chilenos. En segundo lugar se encuentra Adolfo García, con 38 artículos científicos, de los cuales 9 están firmados por investigadores chilenos. El primer investigador chileno en la lista es Alfonso Urzúa, en tercer lugar, con 36 artículos, todos ellos firmados por investigadores chilenos.

La Pontificia Universidad Católica de Chile se sitúa en el primer lugar del ranking de afiliaciones más productivas, con 637 artículos científicos, seguida por la Universidad de Chile con 462 artículos. Ambas instituciones representan el 36% de la producción científica del país.

Tres revistas principales se destacan por tener más de 100 artículos, superando al resto de las revistas. En primer lugar, encontramos Frontiers in Psychology, una revista de origen suizo, que lidera con el 31% de las publicaciones. En segundo lugar, está la revista chilena Psicoperspectivas, con el 21% de las publicaciones. Finalmente, la revista Universitas Psychologica representa el 18,24% de las publicaciones.
""")


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


st.subheader("Incremento en la Productividad Científica")
st.write("""
En los últimos años, se ha observado un notable incremento en la productividad científica en Chile,
con un aumento promedio anual del 10,46%. El año 2020 destacó por alcanzar el mayor número de publicaciones, con un total de 657 artículos.
En contraste, los años 2015 y 2016 tuvieron la menor productividad, con un total de 404 artículos publicados en cada uno de esos años.
Este aumento en la productividad se ha reflejado tanto en publicaciones en español como en inglés.
Sin embargo, se ha observado un ligero incremento en las publicaciones en español, con un aumento anual del 3,61%.
Por otro lado, las publicaciones en inglés han mostrado un crecimiento anual del 16,09%, representando un incremento significativamente mayor en comparación con las publicaciones en español.
""")


frecuencia_por_año = paper_por_año(salida_articulos)
df_resultado = prop_idiomas_por_año(salida_articulos)
df_resultado = df_resultado[['Año','Art_es', 'Art_en']]

rename_columns = {
    'Año': 'Año',
    'Art_es': 'Artículos español',
    'Art_en': 'Artículos inglés'
}

df_resultado = df_resultado.rename(columns=rename_columns)

df_agrupado_total = generar_df_agrupado_total(salida_articulos, salida_topicos)

grafico_articulos_por_año = crear_grafico_articulos_por_año(frecuencia_por_año)
grafico_idiomas_por_año = crear_grafico_idiomas_por_año(df_resultado)
grafico_publicaciones_area = crear_grafico_publicaciones_area(df_agrupado_total)



col4, col5 = st.columns(2)

with col4:
    st.altair_chart(grafico_articulos_por_año, use_container_width=True)

with col5:
    st.altair_chart(grafico_idiomas_por_año, use_container_width=True)

st.subheader("Crecimiento por Áreas de la Psicología")
st.write("""
Las áreas de la psicología que experimentaron los mayores aumentos en la cantidad de artículos fueron Psicología del trabajo y organizaciones,
con una tasa de crecimiento anual promedio del 18,04%, seguida de Psicología evolutiva y educacional, con un crecimiento del 15,20%.
Por otro lado, las áreas que mostraron los menores aumentos fueron Psicoterapia, con una tasa de crecimiento anual promedio del 3,47%,
y Psicometría, con un crecimiento del 7,16%. Estos resultados reflejan las diferencias en el crecimiento promedio entre las distintas áreas de la psicología durante el período analizado.
""")


st.altair_chart(grafico_publicaciones_area, use_container_width=True)





