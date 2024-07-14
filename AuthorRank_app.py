import streamlit as st

st.title("Algoritmo de AuthorRank")

st.markdown("""
            Cuando hacemos **análisis de redes sociales**, muchas veces queremos identificar a las personas (nodos)
            que tienen mayor impacto o influencia en la red. Para esto, existen medidas como la centralidad de grado, intermediación
            y cercanía, las cuales son **fáciles de calcular**, ya que solo requieren conocer los nodos y el número de aristas.

            Para el caso de un análisis de redes sociales en una red de coautoría donde se tiene información de los autores como:
            
            - Número de artículos 
            - Número de coautores
            - Con quién trabajó
            - Dónde trabajó

            debemos hacer algo más para obtener mejores resultados. Para este caso, existe **AuthorRank**, detallado en el artículo
            [DOI: 10.1016/j.ipm.2005.03.012](https://www.sciencedirect.com/science/article/abs/pii/S0306457305000336), donde además de los nodos y cantidad de aristas, aprovechamos los pesos $w$ que podemos asignar a cada arista para cuantificar la influencia de cada autor
            en la red. Aquí mostraremos cómo se calculan estos pesos $w$ a partir de las coautorías.

            Se propone representar la red de coautoría como un grafo ponderado dirigido.
             Denominamos este grafo como $G = (V, E, W) $, donde $V$ es el conjunto de nodos, $E$ es el conjunto de aristas,
             y $W$ es el conjunto de pesos $ w_{ij} $ asociados a cada arista que conecta un par de nodos $(v_i, v_j)$.
            

            ### Cálculo de los pesos $w$

            Para calcular los pesos $w$, primero se calcula la exclusividad de cada artículo
            para cada par de autores de la siguiente manera:
            Se tienen dos autores, $(u_i, u_j)$, que colaboran en una colección de artículos
            $A = a1, a2, . . . , ak$. Luego, se calcula cuántos autores diferentes contribuyen a
            cada artículo en el conjunto $A$, donde el número de autores se denota como
            $f(a_k)$ para cada artículo $a_k$.
            Para calcular la exclusividad de un artículo, se utiliza la siguiente fórmula:

            $$ g_{i,j,k}  = \dfrac{1}{f(a_k) - 1}$$


            De esta manera, para cada par de autores $(u_i, u_j)$, se obtiene un conjunto
            de valores de exclusividad correspondientes a cada artículo en la colección:
            $g_{i,j,1}, g_{i,j,2}, ...., g_{i,j,k−1}, g_{i,j,k}$
            Esta metodología permite calcular la exclusividad de los artículos en función
            del número de autores involucrados en cada uno de ellos.

            ### Cálculo de la frecuencia de coautoría

            Para cada par de autores $(u_i, u_j)$, se suman todos sus valores de $g_{i,j,k}$, este valor de
            $C_{i,j}$ es más alto cuanto más exclusivos sean los artículos trabajados en conjunto.
            
            $$ C_{ij} = \displaystyle \sum_{k=1}^m g_{i,j,k}$$

            ### Pesos normalizados

            Para cada par de nodos $(u_i, u_j)$, sus pesos $w_{i,j}$ se calculan de acuerdo a la
            siguiente ecuación:

            $$ w_{ij} = \dfrac{C_{ij}}{\displaystyle \sum_{k=1}^n C_{ik}} $$


            de esta forma la suma de todos los pesos de las aristas de salida del nodo $u_i$
            suma 1. Como en el siguiente ejemplo:
""")

st.image("imagenes/ejemplo_grafo1.png", caption="Ejemplo de un grafo ponderado dirigido")

st.markdown("""
            El nodo $u_i$ comparte artículos con los nodos $u_1$, $u_2$ y $u_3$, los pesos de cada
            arista son $w_{i1}$, $w_{i2}$, $w_{i3}$ respectivamente y por último, la suma da 1. Así para
            todos los nodos del grafo.

            $$ w_{i1} + w_{i2} + w_{i3} = 1 $$

            ### Algoritmo de AuthorRank

            Una vez que se han calculado los pesos $w$ para cada nodo del grafo, se puede
            aplicar la ecuación de AuthorRank en cada iteración:

            $$ AR(i) = (1 - d) + d \displaystyle \sum_{j=0}^n AR(j) w_{ji}$$

            Es importante destacar que se debe inicializar el valor de AuthorRank para
            cada nodo. En este caso, se utiliza un valor inicial común de $1/n$, donde $n$
            representa el total de nodos en el grafo.

            ### Código en Python

            A continuación se muestra cómo se programó en Python, resumiendo qué hace cada función del código.
""")


# Código para crear el grafo
st.markdown("### Función para crear el grafo")
code_create_graph = '''
def create_graph(data, min_articulos_autor, min_articulos_coautor):
    G = nx.Graph()
    for autor_id, autor_datos in data.items():
        if autor_datos['n_articulos'] >= min_articulos_autor:
            G.add_node(autor_id)
            for coautor_id, n in autor_datos['coautores'].items():
                if n >= min_articulos_coautor:
                    G.add_edge(autor_id, coautor_id)
    return G
'''
st.code(code_create_graph, language='python')
st.write("Esta función crea un grafo `G` a partir de los datos de autores y coautores. Solo se incluyen los autores y coautores que tienen un número mínimo de artículos especificado.")

# Código para la clase AuthorRank
st.markdown("### Clase AuthorRank")
code_author_rank = '''
class AuthorRank:
    def __init__(self, data_autores, data_papers, min_articulos_autor, min_articulos_coautor):
        G = create_graph(data_autores, min_articulos_autor, min_articulos_coautor)
        self.lengthG = G.number_of_nodes()
        self.authorrank_dict = self.CalculateRank(G, data_papers)
        self.df = self.to_dataframe(data_autores)
'''
st.code(code_author_rank, language='python')
st.write("El constructor de la clase `AuthorRank` inicializa el grafo `G` utilizando la función `create_graph`, calcula el ranking de los autores y convierte los datos a un DataFrame ordenado por ranking.")

# Método GrandesProductores
st.markdown("### Método GrandesProductores")
code_grandes_productores = '''
    def GrandesProductores(self, G_autor, top_n=None):
        NodeArt = [(data_autores[node]['nombre_autor'], data_autores[node]['n_articulos']) for node in G_autor.nodes()]
        NodeArt_ordenada = sorted(NodeArt, key=lambda x: x[1], reverse=True)
        return NodeArt_ordenada[:top_n] if top_n else NodeArt_ordenada
'''
st.code(code_grandes_productores, language='python')
st.write("Este método devuelve una lista de los autores con más artículos en el grafo `G_autor`, ordenados de mayor a menor. Se puede especificar un número `top_n` para limitar la cantidad de resultados.")

# Método WeigthG
st.markdown("### Método WeigthG")
code_weight_g = '''
    def WeigthG(self, G, data_papers):
        lista_paper = set()
        for node, node_data in data_autores.items():
            lista_paper.update(node_data["articulos"])

        exclusividad = {}
        for paper in lista_paper:
            if len(data_papers[paper]) > 1:
                pares = [(str(a), str(b)) for a in data_papers[paper] for b in data_papers[paper] if a != b]
                pares_en_g = set(pares) & set(G.edges())
                exclusividad[paper] = {"pares": pares_en_g, "score": 1 / (len(data_papers[paper]) - 1)}

        deleted_paper = [paper for paper, data in exclusividad.items() if not data]
        for paper in deleted_paper:
            del exclusividad[paper]

        peso_c = {}
        for edge in G.edges():
            suma = sum(data["score"] for paper, data in exclusividad.items() if edge in data["pares"])
            peso_c[edge] = peso_c[(edge[1], edge[0])] = suma

        peso_w = {edge: peso_c[edge] / sum(peso_c[e] for e in G.edges(node)) for node in G for edge in G.edges(node)}

        return peso_w
'''
st.code(code_weight_g, language='python')
st.write("Este método calcula el peso de las aristas en el grafo `G` basado en la exclusividad de los artículos compartidos entre coautores. Asigna un score a cada arista basado en la cantidad de artículos compartidos.")

# Método CalculateRank
st.markdown("### Método CalculateRank")
code_calculate_rank = '''
    def CalculateRank(self, G, data_papers, damping=0.85, max_iter=1000):
        peso_w = self.WeigthG(G, data_papers)
        largo = G.number_of_nodes()
        authorrank = {node: (1 / largo) for node in G.nodes()}
        iterr = 0
        while iterr < max_iter:
            iterr += 1
            for node_i in G.nodes():
                suma = 0
                for nodo_j in G.edges(node_i):
                    suma += authorrank[nodo_j[1]] * peso_w[(nodo_j[1], node_i)]
                authorrank[node_i] = (1 - damping) / largo + damping * suma
        return authorrank
'''
st.code(code_calculate_rank, language='python')
st.write("Este método calcula el ranking de los autores en el grafo `G` utilizando un algoritmo similar al PageRank. Ajusta el ranking en cada iteración hasta un máximo de iteraciones o hasta que los valores converjan.")

# Método to_dataframe
st.markdown("### Método to_dataframe")
code_to_dataframe = '''
    def to_dataframe(self, data_autores):
        data = [{'Nodo': node, 'Nombre': data_autores[node]['nombre_autor'], 'Rank': rank} for node, rank in self.authorrank_dict.items()]
        df = pd.DataFrame(data)
        df = df.sort_values(by='Rank', ascending=False)
        return df
'''
st.code(code_to_dataframe, language='python')
st.write("Este método convierte los datos del ranking de autores a un DataFrame de Pandas, ordenado por el ranking de forma descendente.")

# Ejecución principal
st.markdown("### Ejecución principal")
code_main = '''
if __name__ == "__main__":
    # Cargar datos
    with open('data/data_autores_prueba.json', 'r', encoding='utf-8') as f:
        data_autores = json.load(f)

    with open('data/data_papers_prueba.json', 'r', encoding='utf-8') as f:
        data_papers = json.load(f)

    # Crear instancia de AuthorRank
    author_rank_instance = AuthorRank(data_autores, data_papers, 1, 1)

    # Obtener el DataFrame ordenado descendente
    df_result = author_rank_instance.df

    # Imprimir el DataFrame
    print(df_result)
'''
st.code(code_main, language='python')
st.write("""Este bloque de código se ejecuta solo si el script se ejecuta como un programa principal.
          Carga los datos de los autores y artículos, crea una instancia de la clase `AuthorRank`,
          y finalmente imprime el DataFrame con los resultados del ranking.""")

st.markdown("""
[Código final](https://github.com/Igrojas/Algoritmo-AuthorRank)
""")

