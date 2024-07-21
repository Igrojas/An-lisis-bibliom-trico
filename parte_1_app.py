import streamlit as st
import pandas as pd
import altair as alt
from utils import *

# Datos

salida_autores = pd.read_excel("data/salida_autores.xlsx")
salida_articulos = pd.read_excel("data/output_articles.xlsx")
salida_revistas = pd.read_excel("data/salida_revistas.xlsx")
salida_filiaciones = pd.read_excel("data/salida_filiaciones.xlsx")
salida_topicos = pd.read_excel("data/salidas_topicos_CB.xlsx")
salida_authorrank = pd.read_excel("data/salida_AuthorRank.xlsx",index_col= 0)

st.title("Análisis de Redes de Coautoría y Productividad Científica en Psicología Chilena (2015-2020)")

st.markdown("""
## Introducción
            
En este portafolio, presento un resumen del análisis realizado en mi memoria de título sobre la estructura de la red de coautoría y la productividad científica de psicólogos chilenos entre 2015 y 2020.
Utilicé metodologías avanzadas como unificación de datos de Scopus, Web of Science (WOS) y Scielo, algoritmos como AuthorRank y NMF,
y evalué la colaboración mediante el coeficiente modificado. Este trabajo destaca los hallazgos clave y la metodología utilizada, 
proporcionando una comprensión exhaustiva de la productividad científica en psicología, enfatizando la importancia de los algoritmos empleados,
especialmente el análisis de temas mediante NMF, en el estudio de la red de coautoría.
""")

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

st.header("""Productividad científica""")

# principales_indicadores(salida_autores, salida_articulos)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

st.header('Número de artículos por autor')

st.markdown("""
**Principales Productores con Afiliación Chilena**

En la tabla de los principales productores con afiliación chilena, se destacan los siguientes autores:

1. **Agustín Ibáñez**: Autor argentino que lidera la lista con 60 artículos científicos, de los cuales 59 están firmados por Chile.
2. **Adolfo García**: También autor argentino, ocupa el segundo lugar con 38 artículos científicos, de los cuales 9 están firmados por Chile.
3. **Alfonso Urzúa**: Primer chileno en la lista, con 36 artículos, todos ellos firmados por Chile.
""")


top_autores = n_articulos_por_autor(salida_autores)

chart = alt.Chart(top_autores).mark_bar().encode(
    y=alt.Y('name_author', sort='-x', title='Autor'),
    x=alt.X('n_articles_total', title='Número de artículos totales'),
    tooltip=['name_author', 'n_articles_total', 'n_articulos_chile']
).properties(
    width=650, 
    height=600  
).configure_axis(
    labelFontSize=12,
    titleFontSize=14
)

st.altair_chart(chart)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

st.header('Análisis de Artículos por Filiación')


filiaciones_ordenadas = paper_por_filiacion(salida_filiaciones)

st.markdown("""
**Ranking de Afiliaciones Más Productivas**

Según el análisis de la producción científica, las siguientes universidades destacan por su cantidad de artículos publicados:

1. **Pontificia Universidad Católica de Chile**: Ocupa el primer lugar con 637 artículos científicos.
2. **Universidad de Chile**: En segundo lugar con 462 artículos.

Ambas instituciones representan el 36% de la producción científica del país.
""")


chart = alt.Chart(filiaciones_ordenadas).mark_bar().encode(
    y=alt.Y('name_affiliation', sort='-x', title='Filiación'),
    x=alt.X('n_articles', title='Número de Artículos'),
    tooltip=['name_affiliation', 'n_articles', 'Porcentaje de Artículos']
).properties(
    width=650,
    height=600
).configure_axis(
    labelFontSize=12,
    titleFontSize=14
)

st.altair_chart(chart)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

st.header('Artículos por Revista')

st.markdown("""
**Revistas Destacadas en la Investigación**

En el análisis de la literatura, se identificaron tres revistas principales que sobresalen por su alta cantidad de publicaciones, con más de 100 artículos cada una. Estas son:

1. **Frontiers in Psychology**: Una revista suiza que lidera con el 31% de las publicaciones.
2. **Psicoperspectivas**: Una revista chilena que ocupa el segundo lugar con el 21% de las publicaciones.
3. **Universitas Psychologica**: Esta revista contribuye con el 18,24% de las publicaciones.
""")

revistas_ordenadas = paper_por_revistas(salida_revistas)
chart_revistas = alt.Chart(revistas_ordenadas).mark_bar().encode(
    y=alt.Y('title', sort='-x', title='Revista'),
    x=alt.X('n', title='Número de Artículos'),
    tooltip=['title', 'n', 'Porcentaje de Artículos']
).properties(
    width=650,
    height=600
).configure_axis(
    labelFontSize=12,
    titleFontSize=14
)
st.altair_chart(chart_revistas)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

st.header('Artículos por Año')

st.markdown("""
**Tendencia de Publicaciones Científicas por Año**

El gráfico de líneas muestra la evolución del número de artículos científicos publicados anualmente entre 2015 y 2020. A continuación, se destacan algunos cambios porcentuales notables:

- Entre 2016 y 2017, hubo un incremento del 15.10% en el número de artículos, pasando de 404 a 465 publicaciones.
- Entre 2017 y 2018, el aumento fue del 13.12%, con las publicaciones subiendo de 465 a 526.
- Entre 2018 y 2019, el crecimiento se desaceleró, registrando un incremento del 3.99%, de 526 a 547 artículos.
- Entre 2019 y 2020, se observó el mayor aumento porcentual, con un crecimiento del 20.11%, alcanzando los 657 artículos.

Estos datos reflejan una tendencia general de crecimiento en la producción científica, con un aumento especialmente notable en el último año analizado.
""")


frecuencia_por_año = paper_por_año(salida_articulos)
chart_año = alt.Chart(frecuencia_por_año).mark_line(point=True).encode(
    x=alt.X('Año:O', title='Año'),
    y=alt.Y('n_articulos', title='Número de Artículos'),
    tooltip=['Año', 'n_articulos']
).properties(
    width=650,
    height=400
).configure_axis(
    labelFontSize=12,
    titleFontSize=14
)

st.altair_chart(chart_año)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

st.header('Análisis de Idiomas de Artículos')

st.markdown("""
**Distribución de Publicaciones por Idioma**

La tabla muestra la distribución de las publicaciones según el idioma utilizado. Se destacan los siguientes datos:

- **Inglés**: La mayoría de las publicaciones están en inglés, con un total de 1823 artículos.
- **Español**: En segundo lugar, con 1137 publicaciones.
- **Múltiples Idiomas**:
  - Inglés y español: 17 publicaciones.
  - Inglés y francés: 1 publicación.
  - Inglés, portugués y español: 1 publicación.
- **Otros Idiomas**:
  - Francés: 10 publicaciones.
  - Portugués: 8 publicaciones.
  - Alemán: 4 publicaciones.
  - Estonio: 1 publicación.

Estos datos resaltan la predominancia del inglés en las publicaciones científicas, seguido por el español. También se observa una diversidad de idiomas en menor medida.
""")

idiomas_counts = cambiar_idioma(salida_articulos)
idiomas_counts_df = pd.DataFrame(idiomas_counts.reset_index())
idiomas_counts_df.columns = ['Idioma', 'Número de Artículos']

st.subheader('Número de Artículos por Idioma')
chart_idiomas = alt.Chart(idiomas_counts_df).mark_bar().encode(
    y=alt.Y('Idioma:N', sort='-x', title='Idioma'),
    x=alt.X('Número de Artículos:Q', title='Número de Artículos'),
    tooltip=['Idioma', 'Número de Artículos']
).properties(
    width=650,
    height=600
).configure_axis(
    labelFontSize=12,
    titleFontSize=14
)
st.altair_chart(chart_idiomas)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

st.header('Análisis de Idiomas por Año')
st.markdown("""
**Incremento en la Productividad Científica en Chile**

De acuerdo con los datos, se ha observado un notable incremento en la productividad científica en Chile en los últimos años, con un aumento promedio anual del 10.46%. 

- **Año 2020**: Destacó al alcanzar el mayor número de publicaciones, con un total de 657 artículos.
- **Años 2015 y 2016**: Se caracterizaron por tener la menor productividad, con un total de 404 artículos publicados en cada año.

Este aumento en la productividad se ha reflejado tanto en las publicaciones en español como en inglés:

- **Publicaciones en Español**: Se ha observado un ligero incremento anual del 3.61%.
- **Publicaciones en Inglés**: Se ha registrado un mayor interés por publicar en inglés, con un crecimiento anual del 16.09%, lo cual representa un incremento significativamente mayor en comparación con las publicaciones en español.

Estos datos destacan el crecimiento sostenido de la producción científica en Chile y el creciente interés por publicar en inglés.
""")

df_resultado = prop_idiomas_por_año(salida_articulos)

st.dataframe(df_resultado[['Año', 'n_art', 'Art_es', 'Prop_es', 'Art_en', 'Prop_en']])

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

st.header('Análisis de Artículos por Área')
st.markdown("""
**Análisis de Tasas de Crecimiento en Áreas de Psicología**

En cuanto a las tasas de crecimiento, se calcularon utilizando la fórmula de la tasa promedio de crecimiento anual mencionada anteriormente. A continuación se presentan los resultados destacados:

- **Psicología del Trabajo y Organizaciones**: Experimentó un notable crecimiento anual promedio del 18.04% en la cantidad de artículos.
- **Psicología Evolutiva y Educacional**: Mostró un crecimiento anual promedio del 15.20%.
- **Psicoterapia**: Registró un menor aumento con una tasa de crecimiento anual promedio del 3.47%.
- **Psicometría**: También mostró un crecimiento moderado del 7.16%.

Estos resultados reflejan las diferencias significativas en el crecimiento promedio entre las distintas áreas de la psicología durante el período analizado. Es evidente el crecimiento sostenido en áreas específicas como Psicología del Trabajo y Organizaciones y Psicología Evolutiva y Educacional.
""")


df_agrupado_total = generar_df_agrupado_total(salida_articulos, salida_topicos)

chart_areas = alt.Chart(df_agrupado_total).mark_line(point=True).encode(
    x='Year:N',
    y=alt.Y('n_art:Q', title='Número de Artículos'),
    color='Area:N',
    tooltip=['Year:N', 'Area:N', 'n_art:Q']
).properties(
    width=650,
    height=600,
    title='Evolución de Publicaciones por Área de Investigación (2015-2020)'
).configure_axis(
    labelFontSize=12,
    titleFontSize=14
).configure_legend(
    orient='top-left',  
    title=None )

st.altair_chart(chart_areas)
