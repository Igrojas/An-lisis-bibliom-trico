import streamlit as st
from utils import *
from PIL import Image
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
import networkx as nx
from grafos import *

st.title("""Análisis de Redes de Sociales""")
st.header("Redes de Coautoría")

st.markdown(""" 
Cuando analizamos redes sociales, es interesante ver que nodos son más "importantes" en una red, esto es responder a las preguntas:
- ¿Cuales son los nodos con mas conexiones en al red?
- ¿Por cual nodo tengo que pasar para llegar de un nodo a otro pasando por la menor cantidad de nodos?
- ¿Cual es el nodo que poseé los caminos mas cortos para llegar a otros nodos, es decir el nodo mas cercano a los otros nodos?
            
Estas 3 respuestas tiene un nombre, **CENTRALIDAD**, que para cada respuesta en especifico nos encontramos con:
- Centralidad de Grado
- Centralidad de intermediacón
- Centralidad de cercanía
            
Por lo que para aplicar estos conceptos, necesitamos saber a que estructura matemática son aplicables, para ello veamos que es un **GRAFO**
              """)

st.header("¿Qué es un Grafo?")

st.markdown("""
Un grafo es una estructura matemática que consiste en un conjunto de **vértices** (nodos) y **aristas** (enlaces) que los conectan. 
Se representa matemáticamente como $G = (V, E) $, donde:
- $V$ es un conjunto de vértices.            
- $E$ es un conjunto de aristas, que son pares de vértices que establecen una relación entre ellos.

### Hay muchos tipos de grafos:
1. **Grafo No Dirigido**: Las aristas no tienen dirección, es decir, la relación entre dos vértices es simétrica.
2. **Grafo Dirigido**: Las aristas tienen dirección, indicando que la relación entre dos vértices es unidireccional.
3. **Grafo Ponderado**: Las aristas tienen un peso o valor asociado que representa alguna medida entre los vértices.
4. **Grafo Bipartito**: Los vértices se dividen en dos conjuntos disjuntos, y las aristas solo conectan vértices de diferentes conjuntos.

Para el caso de una red social, podemos considerar un grafo no dirigido, o un grafo dirigido, otro grafo ponderado o el grafo bipartito,
todo dependerá del tipo de problemas que estemos analizando.
            
### Ejemplos de cada uno de los grafos:
""")

EjemploDeGrafos()




st.markdown("""
Los grafos son una herramienta fundamental en la teoría de redes y tienen aplicaciones extensas en diversas áreas del conocimiento y la tecnología.
""")


st.header("Apliquemos las centralidades")

st.markdown("""
Consideremos el siguiente grafo no dirido y respondamos a las 3 preguntas que teniamos el inicio
- ¿Cuales son los nodos con mas conexiones en al red?
- ¿Por cual nodo tengo que pasar para llegar de un nodo a otro pasando por la menor cantidad de nodos?
- ¿Cual es el nodo que poseé los caminos mas cortos para llegar a otros nodos, es decir el nodo mas cercano a los otros nodos?
            """)
G = GrafoCentralidad()

st.markdown("""
Primero debemos conocer que es cada centralidad y como se calculan 

**Centralidad de Grado:** La centralidad de grado mide la cantidad de conexiones directas que tiene un nodo en una red.
Si eligo un nodo al azar del grafo, es muy probable que este nodo este conectado con el nodo con mayor centralidad de grado.

Lo único que necesitamos para saber la centralidad de grado de un nodo es cuantas aristas tiene ese nodo, entonces diremos que
$grado(v)$ va ser el total de aristas de un nodo $v$, y para todo nodo $u \in V$
""")

st.latex(r''' 
C_D(u) = \text{grado}(u) 
''')

st.markdown("""
**Centralidad de Intermediación:** La centralidad de intermediación mide cuántas veces un nodo actúa como un puente a lo largo del camino más corto entre dos otros nodos.
Estos nodos con alta centralidad, son los que sostienen la red unida, si eliminamos ese nodo, perdemos muchos caminos que unen otros nodos.
""")

st.latex(r'''
C_B(u) = \sum_{s \neq v \neq t} \frac{\sigma_{st}(u)}{\sigma_{st}}
''')

st.markdown("""
Donde $\sigma_{st}$ son todos los caminos que unen al nodo $s$ con el nodo $t$, y $\sigma_{st}(u)$ son todos los caminos que pasan por $u$
""")

st.markdown("""
**Centralidad de Cercanía:** La centralidad de cercanía mide cuán cerca está un nodo de todos los demás nodos en la red. 
Este nodo es capaz de llegar a todos los nodos en más rápido que cualquier otro nodo.
""")
st.latex(r'''
C_C(u) = \frac{1}{\sum_{v \in V} d(u, v)}
''')

st.markdown("""
Donde $d(u,v)$ es la distancia más corta entre los nodos $u$ y $v$, y $V$ es el conjunto de todos los nodos del grafo $G$.
""")

st.markdown("""
Ahora que ya sabemos que es cada centralidad y como calcular cada centralidad, usamos la libreria netwrokX que además de permitir
dibujar los grafo, ofrece las funciones para calcular las 3 centralidades.
            
Una vez que se calculan, se puede representar la centralidad del nodo a través del tamaño del nodo, donde el nodo mas grande es el nodo mas central,
tambien podemos identificar el valor de cada centralidad a través de colores, que es como se presenta en la siguiente figura.
""")


G = GrafoEjemplo()
fig, axs = plt.subplots(1, 3, figsize=(30, 10))
# Centralidad de grado
centrality = nx.degree_centrality(G)
PlotCentralidad(G, axs[0], centrality, 'Centralidad de Grado', 'Centralidad de Grado')

# Centralidad de intermediación
centrality = nx.betweenness_centrality(G)
PlotCentralidad(G, axs[1], centrality, 'Centralidad de Intermediación', 'Centralidad de Intermediación')

# Centralidad de cercanía
centrality = nx.closeness_centrality(G)
PlotCentralidad(G, axs[2], centrality, 'Centralidad de Cercanía', 'Centralidad de Cercanía')

# Ajustar los layouts para que no se sobrepongan
plt.tight_layout()
st.pyplot(fig)

st.markdown("""
El primer grafo de la imágen corresponde a la centralidad de grado, donde los nodos mas centrales fueron el nodo $14$ y el nodo $6$, estos son los nodos
con mayor aristas en la red.
            
En el segundo grafo, que corresponde a la centralidad de intermediacón, vemos que el nodo por donde pasan la mayor cantidad de caminos más cortos es el nodo $6$, 
que de acuerdo a la red, si queremos llegar de un nodo a otro, es muy probable que debamos pasar por el nodo $6$.
            
El último grafo, que corresponde a la centralidad de cercanía, vemos nuevamente al nodo $14$, lo que indica que este nodo $14$ tiene los caminos más cortos para llegar a cualquier otro nodo
del grafo, seguido del nodo $6$, que tambien es muy cercano a los otros nodos, pero en su caso, tendría que recorrer algunas aristas más.
""")

st.header("Grafo Dirigido")

st.markdown("""
¿Que pasa ahora si el grafo fuera digirido?, ¿Importa de donde que nodo sale una aristas?, ¿Importa a que nodo llega una arista?. Para responder estas preguntas,
exsite un algoritmo llamado **PageRank**.
            
PageRank es un algoritmo originalmente creado por Google para su motor de
búsqueda. Se basa en la idea de que el valor de una página web se puede medir en
función del número y calidad de los hipervínculos que apuntan hacia ella.
""")

G = GrafoDirigidoEjemplo()
fig, ax = plt.subplots()
pos = nx.nx_agraph.graphviz_layout(G, prog='dot')
# pos = nx.spring_layout(G)
nx.draw(G, pos= pos,  with_labels=True, node_color='lightblue', ax=ax)
ax.set_title('Grafo Dirigido de Ejemplo', fontsize=16)
st.pyplot(fig)

st.markdown("""
Viendo este grafo, ¿Que nodo sería considerado el más importante?, para esto aplicamos el algoritmo de PageRank, que por suerte, la librería Networkx, nos ofrece este algoritmo,        
""")
fig, ax = plt.subplots()
pagerank = nx.pagerank(G)
PlotPagerank(G,pagerank)

st.markdown("""
De acuerdo con el algoritmo de PageRank, el nodo mas "importante" de la red es el nodo $14$, el cual es el nodo que otros nodos "importantes" apuntan,
seguido del nodo $13$ y el nodo $9$""")

st.header("Entonces, de que va mi memoria de título")

st.markdown("""
Cuando teniamos todos los datos sobre autores y articulos científicos, los mismos que fueron mostrados en la parte 1, queriamos armar una red de coautoría, con 
los autores como **nodos** y la coautoría como **arista**, pero aplicar centralidad de grado o centralidad de cercanía era algo muy simple de hacer, considerando la cantidad de datos disponibles.
            
Entonces podiamos aplicar PageRank, pero tambien nos dejaba con gusto a poco, queriamos aprovechar que teniamos datos como el número de artículos, todas las coautorías de los artículos disponibles,
la cantidad de coautoía entre autores, etc.
            
Aquí es cuando aparece paper [Co-authorship networks in the digital library research community](https://www.sciencedirect.com/science/article/abs/pii/S0306457305000336)
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

st.header("Grafo de comunidades de autores de mayor productividad - Las primeras 200 comunidades")

# with open('GrafoComunidadAutores.html', 'r', encoding='utf-8') as f:
#     html_content = f.read()

# components.html(html_content, height=600)

st.header('Red de Comunidades de Grandes Productores')

st.markdown("""
La red de comunidades de grandes productores muestra la estructura de colaboración entre autores destacados:

- Cada comunidad está liderada por un gran productor.
- Se observa una diversidad en la conexión de las comunidades, destacándose la centralidad de algunos autores.
- La presencia de autores con afiliación internacional y su impacto en la red.

Este análisis permite visualizar la distribución y conexiones dentro de la red de coautoría, evidenciando la influencia y colaboración entre autores destacados tanto nacionales como internacionales.

Para este grafo se muestran las primeras 16 comunidades de grandes productores en Chile, donde el mínimo de artículos por autor para estar en el grafo es de 3 artículos
            """)

# with open('Grafo20Comunidad.html', 'r', encoding='utf-8') as f:
#     html_content = f.read()

# components.html(html_content, height=600)
