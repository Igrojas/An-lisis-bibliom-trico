import streamlit as st
from utils import *
from PIL import Image
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
import networkx as nx

st.title("Análisis de Redes de Coautoría en Psicología Chilena")

st.header("¿Qué es un Grafo?")

st.markdown("""
Un grafo es una estructura matemática que consiste en un conjunto de **vértices** (nodos) y **aristas** (enlaces) que los conectan. 
Se representa matemáticamente como \( G = (V, E) \), donde:
- \( V \) es un conjunto de vértices.
- \( E \) es un conjunto de aristas, que son pares de vértices que establecen una relación entre ellos.

### Tipos de Grafos:
1. **Grafo No Dirigido**: Las aristas no tienen dirección, es decir, la relación entre dos vértices es simétrica.
2. **Grafo Dirigido**: Las aristas tienen dirección, indicando que la relación entre dos vértices es unidireccional.
3. **Grafo Ponderado**: Las aristas tienen un peso o valor asociado que representa alguna medida entre los vértices.
4. **Grafo Bipartito**: Los vértices se dividen en dos conjuntos disjuntos, y las aristas solo conectan vértices de diferentes conjuntos.

### Ejemplo de Grafo:
""")

G = nx.Graph()

G.add_node(1)
G.add_node(2)
G.add_node(3)
G.add_node(4)

G.add_edge(1, 2)
G.add_edge(2, 3)
G.add_edge(3, 4)
G.add_edge(4, 1)
G.add_edge(1, 3)

nx.draw(G, with_labels=True, node_color='blue', node_size=700, font_size=15, font_color='white', edge_color='gray')

# Mostrar el grafo
st.pyplot(plt)

st.markdown("""
Los grafos son una herramienta fundamental en la teoría de redes y tienen aplicaciones extensas en diversas áreas del conocimiento y la tecnología.
""")

st.header("Análisis de la Estructura del Grafo de Coautoría en Psicología")
st.markdown("""
El grafo de coautoría es una representación visual de la colaboración científica entre autores, donde los nodos representan a los autores y las aristas indican la existencia de trabajos científicos en común. 

Al analizar la estructura del grafo de coautoría, se obtuvieron los siguientes resultados:

- **Densidad**: 0.0032
- **Camino Medio**: 5.50

Se identificaron un total de 662 componentes conexas:

- 506 componentes con la colaboración de dos o más autores, representando el 76.43% del total de autores y responsables del 94.30% de los artículos.
- 156 componentes compuestas por un solo autor, responsables de 171 artículos, representando el 5.69% del total de artículos.

La componente conexa más grande está formada por 6457 autores, quienes colaboraron en la publicación de artículos científicos:

- Representa el 68.7% del total de autores.
- Densidad de 0.0064, el doble que la densidad del grafo general.
- Diámetro de 14.
- Concentra el 60.60% del total de artículos científicos.

En contraste, la segunda componente más grande consta de 61 autores, representando un 0.65% del total de autores en el grafo.

Estos hallazgos proporcionan una visión detallada de la estructura y la colaboración en la red de coautoría en el campo de la psicología, destacando la diversidad y la distribución de la colaboración entre los investigadores.
""")

st.header("Análisis de AuthorRank y Comunidades en la Red de Coautoría")

st.markdown("""
Este análisis se centra en la componente conexa más grande de la red de coautoría, utilizando el algoritmo AuthorRank y el Algoritmo de Comunidades.
""")

st.markdown("""            
### [AuthorRank](https://an-lisis-bibliom-trico-q347mhuyf9j4wxsl9kdf2c.streamlit.app/)

Se utilizó el algoritmo AuthorRank para asignar un ranking a cada autor en la red de coautoría. Los tonos más oscuros indican un mayor ranking. 
Destacan autores como Agustín Ibáñez en el primer lugar de AuthorRank, seguido de Alfonso Urzúa, y similares rangos para Adolfo García, Felipe García y Marianne Krause.
        
""")


mostrar_tabla()

st.header("Grafo con autores con más de 10 artículos científicos")

with open('GrafoCoautoria.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

components.html(html_content, height=600)

st.markdown("""  
### Algoritmo de Comunidades

Se identificaron 16 comunidades de grandes productores en la red de coautoría. Cada comunidad incluye al menos un autor con una destacada producción científica. Por ejemplo:

- Agustín Ibáñez se encuentra en la comunidad 1.
- Alfonso Urzúa en la comunidad 2.
- Felipe García en la comunidad 3.
- Marianne Krause en la comunidad 4.

Este análisis proporciona una visión profunda de la estructura y la colaboración en la red de coautoría, destacando la importancia de los algoritmos utilizados para comprender mejor la dinámica entre los autores en el campo de estudio.
""")



st.header('Comunidades de Autores')

st.markdown("""
El análisis de comunidades de autores revela lo siguiente:

- Se identificaron 1996 comunidades, de las cuales el 77.7% están compuestas por dos o más autores.
- Estas comunidades representan el 95.3% de los autores y el 94.3% de los artículos científicos chilenos analizados.
- El 77.69% de las comunidades con dos o más autores incluyen al menos un autor de afiliación chilena.
- El grafo de comunidades tiene una densidad de 0.001 y un camino medio de 4.85.
- La componente más grande agrupa el 60.17% de las comunidades, destacándose la comunidad de Agustín Ibáñez.
- Se observa una agrupación de comunidades chilenas, con conexiones internacionales destacadas en el centro del grafo.

Estos hallazgos muestran la estructura y distribución de colaboraciones en la red de coautoría, resaltando la presencia significativa de comunidades chilenas y su conexión global en la investigación científica.
""")

st.header("Grafo de comunidades de autores de mayor productividad")

with open('GrafoComunidadAutores.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

components.html(html_content, height=600)

st.header('Red de Comunidades de Grandes Productores')

st.markdown("""
La red de comunidades de grandes productores muestra la estructura de colaboración entre autores destacados:

- Cada comunidad está liderada por un gran productor.
- Se observa una diversidad en la conexión de las comunidades, destacándose la centralidad de algunos autores.
- La presencia de autores con afiliación internacional y su impacto en la red.

Este análisis permite visualizar la distribución y conexiones dentro de la red de coautoría, evidenciando la influencia y colaboración entre autores destacados tanto nacionales como internacionales.
""")

img = Image.open('imagenes/clusters2_1000.png')
st.image(img, caption='Componentes Principales de Autores')
