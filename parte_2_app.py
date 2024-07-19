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
# fig, ax = plt.subplots()
pagerank = nx.pagerank(G)
PlotPagerank(G,pagerank)

st.markdown("""
De acuerdo con el algoritmo de PageRank, el nodo mas "importante" de la red es el nodo $14$, el cual es el nodo que otros nodos "importantes" apuntan,
seguido del nodo $13$ y el nodo $9$""")

st.header("Entonces, de que va mi memoria de título")

st.markdown("""
**Red de Coautoría y Medidas de Centralidad**

Con todos los datos sobre autores y artículos científicos presentados en la parte 1, queríamos construir una red de coautoría donde los autores son **nodos** y las coautorías son
 **aristas**. Aplicar centralidad de grado o cercanía resultaba muy básico debido a la cantidad de datos disponibles.

Exploramos el uso de PageRank, pero necesitábamos algo más robusto. Aprovechando datos como el número de artículos, coautorías,
y la intensidad de colaboración entre autores, implementamos el algoritmo **AuthorRank**, descrito en el artículo
[Co-authorship networks in the digital library research community](https://www.sciencedirect.com/science/article/abs/pii/S0306457305000336).

### AuthorRank
            
[**AuthorRank**](https://an-lisis-bibliom-trico-q347mhuyf9j4wxsl9kdf2c.streamlit.app/) clasifica a los autores según la calidad e impacto de sus publicaciones y colaboraciones,
evaluando su influencia dentro de la red de coautores. Este algoritmo, implementado en Python, permitió utilizar información detallada sobre artículos y coautorías,
y sus resultados se aplicaron en el **algoritmo de comunidades ABCD** para un análisis más profundo.

Necesitamos un grafo dirigido con pesos para aplicar el algoritmo de AuthorRank, entonces definimos un grafo $G = (V,E,W)$, donde $V$ es el conjunto de nodos, $E$ el conjunto de aristas
y $W$ el conjunto de pesos $w$, estos pesos $w$ se asignan a cada arista que une un par de nodos $(v_i,v_j)$. Hay que definir que valor va tomar cada peso $w$ de la red, como se 
van a calcular, y que significado tiene en la red.
            
#### Peso de las Aristas en la Red de Coautoría

¿En qué casos el valor de $w$ será alto o bajo? Esto debe definirse. ¿Podemos asignar un valor alto de $w$ entre dos autores que publican frecuentemente juntos? Sí.
¿Podemos asignar un valor bajo a la arista entre dos autores que comparten un artículo con muchos coautores? Sí.
Esto no implica que publicar solo sea menos importante, ni que publicar con muchos autores sea peor.

[**El algoritmo de AuthorRank fue implementado en python, todas las definiciones y fórmulas matemáticas que definen cada aspecto de este algoritmo estan en este link**](https://an-lisis-bibliom-trico-q347mhuyf9j4wxsl9kdf2c.streamlit.app/)


A continuación, se presentan los resultados que dió el algoritmo de **AuthorRank**, además,
aprovechamos de contrastar resultados con las otras medidas de centralidad descritas anteriormente: **Intermediación**, **Cercanía**, **PageRank**.      

Todas estas medidas de centralidad se aplicaron a la totalidad de autores estudiados, es decir que es un grafo de $9393$ nodos, pero la representación del grafo solo muestra
a los autores con más de 10 artículos, para facilitar la visualización y no alterar los resultados de calcular las centralidades. 
""")



# Título de la aplicación
st.header("Visualización de Grafos de Coautoría de autores con más de 10 artículos")

# Opciones de selección
options = {
    "AuthorRank": "GrafoCoautoria.html",
    "PageRank": "GrafoCoautoria_pr.html",
    "Intermediación": "GrafoCoautoria_btw.html",
    "Cercanía": "GrafoCoautoria_close.html"
}

# Desplegable para elegir el grafo
selection = st.selectbox("Selecciona el grafo a visualizar", list(options.keys()))

# Cargar y mostrar el HTML seleccionado
html_file = options[selection]
with open(html_file, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Mostrar el contenido HTML en Streamlit
components.html(html_content, height=600)

mostrar_tabla()


st.markdown("""

Este grafo de coautoría está construido a partir de autores en psicología con al menos una afiliación chilena entre 2015 y 2020.
Los nodos representan a los autores y las aristas indican coautorías, es decir, si trabajaron juntos en un artículo. Las particularidades del grafo son las siguientes:

- El tamaño del nodo corresponde al número de artículos de cada autor; más artículos, nodo más grande.
- El grosor de la arista representa el total de artículos en conjunto; más artículos en común, arista más anchas.
- El tamaño del nombre también es proporcional a la cantidad de artículos de cada autor.
- El gradiente de colores muestra en un color más claro el valor más alto de centralidad calculada.
 
En los resultados de AuthorRank, Agustín Ibáñez ocupa el primer lugar, seguido de Alfonso Urzúa, Adolfo García, Felipe García y Marianne Krause,
quienes tienen un AuthorRank similar.

El PageRank muestra resultados similares, liderado por Agustín Ibáñez, seguido de cerca por Alfonso Urzúa, Marianne Krause, Felipe García y Adolfo García.

Tanto en AuthorRank como en PageRank, los autores con los mejores resultados coinciden con los mayores productores en psicología chilena.

Los tres principales conectores de la red son Xavier Orial, Alfonso Urzúa y Marianne Krause.

Los autores más cercanos a otros nodos son Anna Wlodarczyk, Agustín Espinosa, Alfonso Urzúa y Roberto González.

Si tuviéramos que elegir un autor "importante" que produzca muchos artículos, colabore ampliamente, tenga una gran intermediación en la red y sea cercano a otros autores,
sería Alfonso Urzúa, Profesor Titular Chileno de la Universidad Católica del Norte en Antofagasta, Chile.
            


""")
