import streamlit as st
import pandas as pd




st.title("Algoritmo de detección de comunidades basado en atractivo")


st.markdown("""

Ocupamos el algoritmo ABCD debido a su facilidad de implementación y su capacidad
para adaptarse dinámicamente al número de comunidades en un grafo
sin requerir una **cantidad predefinida de comunidades**.
            
La implementación del algoritmo ABCD se realiza en el lenguaje de programaci
ón Python, aprovechando la biblioteca NetworkX, que proporciona herramientas
para la creación y el análisis de grafos.
            
En este contexto, se utiliza el mismo grafo previamente generado para el
cálculo de AuthorRank. Además, se aprovecha el valor de AuthorRank asignado
a cada autor, que se obtiene desde un archivo Excel. En este archivo, cada valor
de AuthorRank está vinculado a la enumeración de nodos en el grafo.

Una característica clave de esta implementación es la utilización del orden
proporcionado por el grafo G. Dado que cada nodo está enumerado, podemos
asignar un peso específico a cada uno, en este caso, se utiliza una ponderación
común de 2000 para todos los nodos. Esto permite realizar ajustes y cálculos
en el algoritmo de manera eficiente.

Las aristas del grafo se obtienen considerando todos los pares de nodos en
G. Los pesos de estas aristas se asignan según el número de coautorías entre
los autores correspondientes. Esta estrategia facilita la identificación de nodos
y aristas específicos para realizar los cálculos necesarios en el algoritmo.

De esta forma, cada nodo y arista queda facilmente identificada para hacer
los calculos correspondiente en el codigo.

**Ejemplo de ponderar los resultados del Algoritmo AuthorRank
por 2000**
            
""")

data = {
    'Enumeracion': [3970, 133, 38, 1231, 2750],
    'Nombre': ['Ibanez, Agustin', 'Alfonso Urzúa M.', 'Adolfo M. Garcia', 'Felipe E. García', 'Mariane Krause'],
    'AuthorRank': [0.002354, 0.001600, 0.001439, 0.001405, 0.001369],
    'AR2000': [4.708, 3.200, 2.878, 2.810, 2.738]
}
df = pd.DataFrame(data)
st.dataframe(df)

st.markdown("""
Mientras avancemos con la definción de este algoritmo, explicaremos porque es necesario ponderar el resultado de AuthorRank por
algún escalar para obtener resultados coherente.        
    
Ahora necesitamos mostrar algunas definiciones de caracterizan este **Algoritmo ABCD**.

### Definición $1$: Densidad de cluster
""")

st.latex(r'''
W_i = \dfrac{\displaystyle \sum_{a=1}^{Q_i} W_a}{Q_i}
''')

st.markdown("""
Donde $W_a$ corresponde al peso individual de cada nodo de la comunidad, $Q_i$ es número de nodos del cluster.
¿y cual es el peso de los nodos?, el peso de cada nodo corresponde a su AuthorRank, que ya calculamos. Tambien
hay que saber que este es un algoritmo aglomerativo, por lo que el estado incial del proceso corresponde al
que todos los nodos individuales son una comunidad $W_i$, por lo que si pensamos que un nodo tiene peso $W_a = 10$, entonces $W_i$ es:
            
Si hay un solo nodo entonces $Q_i = 1$, luego el peso de la comunidad de un solo nodo es:
""")

st.latex(r'''
W_i = \dfrac{\displaystyle \sum_{a=1}^1 W_a}{1} = \dfrac{10}{1} = 10
''')

st.markdown("""                     
### Definición 2: Atractivo entre clusters    
El algoritmo ABCD comienza con comunidades de un solo nodo que se agrupan
en cada iteración hasta que ya no sea posible formar más comunidades. La
formación de comunidades se rige por la condición de atractivo, que se expresa
en la siguiente ecuación        
""")

st.latex(r'''
S_{ij} = \dfrac{\displaystyle \sum_{e=1}^q S_e}{Q_i \times Q_j}
''')

st.markdown("""
En esta fórmula, $S_{ij}$ representa el atractivo entre dos nodos o comunidad, $Q_i$
y $Q_j$ son el número de nodos en las comunidades respectivas, y $S_e$ es el peso de la arista entre nodos de distintas comunidades.
Cuando $S_{ij}$ supera la suma de los pesos individuales de las comunidades ($W_i$ y $W_j$), los nodos pueden
fusionarse en una comunidad.
            
Hay que saber que $Q_i \times Q_j$, es el total de aristas posibles entre las comunidades.
""")

st.markdown("""                     
### Definición 3: Clusters inter-interesados
Si los cluster $i$ y $j$ son inter-interesados, deben cumplir la siguiente condición: 
""")

st.latex(r'''
q \geq Q_i , q \geq Q_j
''')

st.markdown("""                     
### Definición 4: Comunidad
Un cluster $i$ será comunidad cuando se cumpla que:
""")

st.latex(r'''
S_{ij} < W_i + W_j , \forall j        
         ''')


st.markdown("""
Inicialmente cada nodo es un cluster, ya que tratamos con un algoritmo aglomerativo.
Cuando queremos hacer la fusión del cluster $i$, hay que buscar entre todos los cluster inter-interesados, supongamos que sea el cluster $j$ que tenga el mayor atractivo,
debemos asegurarnos que se fusionaran, ya que su atractivo puede ser muy pequeño, necesitamos la siguiente condición:
""")
st.latex(r'''
S_{ij} \geq W_i + W_j    
''')

st.markdown("""
Cumpliendose esta condicón, ambos cluster se fusionan en un cluster.
            
Como ejemplo, consideremos a Agustin Ibañez, y Adolfo García, entre ellos hay un total de $38$ artículos, entonces $S_e = 38$, el peso de la arista entre estos autores.
Ahora como peso de cada nodo, ocupamos el valor de AuthorRank, escalado por $2000$, entonces tenemos que para Agustin Ibañez $W_i = 4.7$ y para Adolfo $W_j = 2.8$, y suponiendo que
$W_j$ es el inter-interesado cluster de mayor valor, debemos comprobar la condición de la **definición 4**, entonces:
""")

st.latex(r'''
\begin{align*}
S_{ij} &\geq W_i + W_j \\
38 &\geq 4.7 + 3.8 \\
38 &\geq 7.5
\end{align*}
''')

st.markdown("""
Por lo tanto, Agustín Ibáñez y Adolfo García cumplen con la condición de atractivo y pueden fusionarse en una comunidad.
La condición de atractivo permite que los nodos se agrupen en comunidades en función de su colaboración,
y el algoritmo ABCD utiliza esta condición para determinar las fusiones de comunidades de manera dinámica durante el proceso de ejecución.

Aquí se explica por qué es necesario escalar el valor de AuthorRank con un factor adecuado.
Es importante tener en cuenta que el número de artículos es un valor entero; 
no se puede tener 1.5 artículos, solo 1 o 2. Por lo tanto, si consideramos el
peso del nodo de Agustín Ibáñez como 
0.002354, al realizar los cálculos, estamos exigiendo a cualquier otro autor un mínimo de 
0.002354 artículos para la unión, lo que en realidad se traduce en un artículo completo.
Esto puede resultar en la formación de una gran comunidad donde todos los autores con al menos un artículo se agruparían,
lo cual no refleja la realidad.

Lo mismo ocurre si el factor de escalado es demasiado grande, por ejemplo,
si exige que un autor tenga al menos 30 artículos para considerar la unión con Agustín Ibáñez. Hasta ahora,
no he encontrado un caso que requiera tal cantidad.

Por eso, determiné que un factor de 2000 produce comunidades de tamaño que tienen sentido y son más representativas.
            
### A continuación se muestra cómo se programó en Python
""")

st.markdown("### Función algoritmo_comunidad")
code_algoritmo_comunidad = '''
def algoritmo_comunidad(data_autores, salida_authorrank):
    
    def create_graph(data, min_articulos_autor, min_articulos_coautor):
        """ Crea un grafo, donde se poda por número de artículos de autor principal
        y de artículos con el autor.
        Parameters:
            data: json de acuerdo a especificacion de component_def
            min_articulos: número de artículos que debe tener un autor para ingresar
            al grafo
            min_articulos_coautores: número de artículos mínimo que debe tener
            un coautor para ser considerado coautor relevante
        """
        G = nx.Graph()
        for autor_id, autor_datos in data.items():
            if autor_datos['n_articulos'] >= min_articulos_autor:
                G.add_node(autor_id)
                for  coautor_id, n in autor_datos['coautores'].items():
                    if n >= min_articulos_coautor:
                        G.add_edge(autor_id, coautor_id)
        return G

    G = create_graph(data_autores, 1, 1)
    nodos = defaultdict(lambda: 0)
    for nodo, valor in salida_authorrank[['ins', 'values']].itertuples(index=False):
        nodos[str(nodo)] = 2000 * valor

    aristas = defaultdict(lambda: 0)
    for edge in G.edges():
        aristas[edge] = data_autores[edge[0]]['coautores'][edge[1]]

    def get_peso_arista(S, key_1, key_2):
        return S.get((key_1, key_2), S.get((key_2, key_1), 0))

    def calcular_peso_promedio(el_1, el_2):
        return (len(el_1['nodos']) * el_1['peso'] + len(el_2['nodos']) * el_2['peso']) / (len(el_1['nodos']) + len(el_2['nodos']))

    def iterar_ct_S(ct, S):
        max_val = 0
        elegidos = None
        ct_keys = list(ct.keys())
        res = [peso for k, peso in S.items() if peso >= ct[k[0]]["peso"] + ct[k[1]]["peso"]]
        if res:
            max_value = max(res)
            max_keys = {key: peso for key, peso in S.items() if peso == max_value}
            for keys, peso_arista in max_keys.items():
                key_1, key_2 = keys
                peso_1 = ct[key_1]["peso"]
                peso_2 = ct[key_2]["peso"]
                if peso_arista > max_val and peso_arista >= (peso_1 + peso_2):
                    max_val = peso_arista
                    elegidos = (key_1, key_2)

        if elegidos:
            ct_new = ct.copy()
            S_new = S.copy()
            key_1, key_2 = elegidos
            new_key = f"{key_1}_{key_2}"
            el_1 = ct[key_1]
            el_2 = ct[key_2]
            peso_nuevo = calcular_peso_promedio(el_1, el_2)
            ct_new[new_key] = {"nodos": el_1['nodos'].union(el_2['nodos']), 'peso': peso_nuevo}
            del ct_new[key_1]
            del ct_new[key_2]
            # Creamos los S_new para los que corresponda
            for key_l in set(ct_keys) - {key_1, key_2}:
                q1 = len(ct[key_1]["nodos"])
                q2 = len(ct[key_2]["nodos"])
                q_dest = len(ct[key_l]["nodos"])
                s1 = get_peso_arista(S_new, key_1, key_l)
                s2 = get_peso_arista(S_new, key_2, key_l)
                s_new = (s1 * q1 * q_dest + s2 * q2 * q_dest) / ((q1 + q2) * q_dest)
                if s_new > 0:
                    S_new[(new_key, key_l)] = s_new
            for arista_n in list(S.keys()):
                if any([key_1 == x or key_2 == x for x in arista_n]):
                    del S_new[arista_n]
            return ct_new, S_new
        else:
            return ct, S

    listo = False
    ct = defaultdict(lambda: {"nodos": set(), "peso": 0})
    for x, peso in nodos.items():
        ct[x]["nodos"].add(x)
        ct[x]["peso"] = peso
    S = aristas.copy()
    iter = 1
    while not listo:
        ct_new, S_new = iterar_ct_S(ct, S)
        if len(ct_new) == 1 or len(ct_new) == len(ct):
            listo = True
        else:
            print("I", iter, ":", len(ct_new))
            ct = ct_new
            S = S_new
            iter += 1
    # print("Final 1:", S,"\n", ct)
    # print("\n")
    return ct
'''
st.code(code_algoritmo_comunidad, language='python')
st.write("""Esta función realiza el algoritmo de comunidad para identificar clústeres de autores en un grafo.
          Primero crea un grafo filtrado por el número de artículos de autores y coautores.
          Luego, itera para fusionar nodos en clústeres basados en un peso calculado para las aristas.""")

st.markdown("### Función sorted_cluster_by_autor")
code_sorted_cluster = '''
def sorted_cluster_by_autor(data_autores, cluster):
    # Crear el diccionario max_articulos_autor
    max_articulos_autor = {node: data['n_articulos'] for node, data in data_autores.items() if data['n_articulos'] > 0}
    max_articulos_autor = dict(sorted(max_articulos_autor.items(), key=lambda x: x[1], reverse=True))

    filter_cluster_max_autores = []
    for key in max_articulos_autor:
        for clr, data in cluster.items():
            if key in data['nodos'] and clr not in filter_cluster_max_autores:
                filter_cluster_max_autores.append(clr)

    return filter_cluster_max_autores
'''
st.code(code_sorted_cluster, language='python')
st.write("""Esta función filtra los clústeres de autores basándose en el número de artículos de los autores.
          Devuelve una lista de clústeres que contienen autores con un número significativo de artículos.""")

st.markdown("### Ejecución principal")
code_main = '''
if __name__ == "__main__":
    f = open('data/grafo_autores.json', encoding='utf-8') 
    data_autores = json.load(f)
    f.close()

    salida_authorrank = pd.read_excel("data/salida_AuthorRank.xlsx", index_col=0)

    cluster = algoritmo_comunidad(data_autores, salida_authorrank)

    filter_cluster_max_autores = sorted_cluster_by_autor(data_autores, cluster)

    print(filter_cluster_max_autores)
'''
st.code(code_main, language='python')
st.write("""Este bloque de código se ejecuta solo si el script se ejecuta como un programa principal.
          Carga los datos de los autores y el ranking de autores, ejecuta el algoritmo de comunidad para identificar clústeres,
          filtra los clústeres basándose en los autores con mayor número de artículos, y finalmente imprime los resultados.""")

