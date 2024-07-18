import matplotlib.pyplot as plt
import networkx as nx
import streamlit as st

def EjemploDeGrafos():
    G1 = nx.Graph()
    G1.add_edges_from([(1, 2), (1, 3), (2, 3), (3, 4)])

    G2 = nx.DiGraph()
    G2.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 1)])

    G3 = nx.Graph()
    G3.add_edge(1, 2, weight=4.2)
    G3.add_edge(2, 3, weight=2.1)
    G3.add_edge(3, 4, weight=1.8)
    G3.add_edge(4, 1, weight=3.5)

    G4 = nx.Graph()
    G4.add_nodes_from([1, 2, 3], bipartite=0)
    G4.add_nodes_from([4, 5, 6], bipartite=1)
    G4.add_edges_from([(1, 4), (2, 5), (3, 6), (1, 5), (2, 6)])
    l, r = nx.bipartite.sets(G4)
    pos1 = {}

    pos1.update((node, (1, index)) for index, node in enumerate(l))
    pos1.update((node, (2, index)) for index, node in enumerate(r))


    fig, axs = plt.subplots(2, 2, figsize=(10, 10))

    nx.draw(G1, ax=axs[0, 0], with_labels=True, node_color='lightblue', font_weight='bold')
    axs[0, 0].set_title('Grafo No Dirigido')

    nx.draw(G2, ax=axs[0, 1], with_labels=True, node_color='lightgreen', font_weight='bold', arrows=True)
    axs[0, 1].set_title('Grafo Dirigido')

    pos = nx.spring_layout(G3)
    nx.draw(G3, pos, ax=axs[1, 0], with_labels=True, node_color='lightcoral', font_weight='bold')
    edge_labels = nx.get_edge_attributes(G3, 'weight')
    nx.draw_networkx_edge_labels(G3, pos, edge_labels=edge_labels, ax=axs[1, 0])
    axs[1, 0].set_title('Grafo Ponderado')


    nx.draw(G4, pos=pos1, ax=axs[1, 1], with_labels=True, node_color='lightyellow', font_weight='bold')

    axs[1, 1].set_title('Grafo Bipartito')

    plt.tight_layout()
    st.pyplot(plt)

    return

def GrafoCentralidad():
    
    G = nx.Graph()

    G.add_edges_from([(1,2),(1,3),(1,4),(3,4),(2,4)])
    G.add_edges_from([(5,7), (5,6), (7,8), (6,8), (6,9), (8,9)])
    G.add_edges_from([(10,11), (10,12), (10,14), (11,12), (11,14), (11,13), (12,13)])

    G.add_edges_from([(3,10),(4,14),(2,14),(5,14),(7,14),(7,11),
                    (6,7),(2,6),(6,13)])

    fig, ax = plt.subplots()
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G,pos=pos, with_labels=True, node_color='lightblue', ax=ax)
    ax.set_title('Grafo de Ejemplo', fontsize=16)

    st.pyplot(fig)
    return 

def GrafoEjemplo():
    G = nx.Graph()

    G.add_edges_from([(1,2),(1,3),(1,4),(3,4),(2,4)])
    G.add_edges_from([(5,7), (5,6), (7,8), (6,8), (6,9), (8,9)])
    G.add_edges_from([(10,11), (10,12), (10,14), (11,12), (11,14), (11,13), (12,13)])

    G.add_edges_from([(3,10),(4,14),(2,14),(5,14),(7,14),(7,11),
                    (6,7),(2,6),(6,13)])
    return G


fig, axs = plt.subplots(1, 3, figsize=(30, 10))
def PlotCentralidad(G, ax, centrality, title, label):

    centrality_values = list(centrality.values())
    max_centrality = max(centrality_values)
    min_centrality = min(centrality_values)
    normalized_centrality = {node: (value - min_centrality) / (max_centrality - min_centrality) for node, value in centrality.items()}

    colors = [normalized_centrality[node] for node in G.nodes()]

    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos=pos, with_labels=True, node_color=colors, cmap=plt.cm.inferno, ax=ax)

    sm = plt.cm.ScalarMappable(cmap=plt.cm.inferno, norm=plt.Normalize(vmin=min_centrality, vmax=max_centrality))
    sm.set_array([])
    fig.colorbar(sm, ax=ax, orientation='vertical', label=label)
    ax.set_title(title, fontsize=16)


def GrafoDirigidoEjemplo():
    G = nx.DiGraph()

    # Agregar aristas al grafo dirigido
    G.add_edges_from([(1,2),(1,3),(1,4),(3,4),(2,4)])
    G.add_edges_from([(5,7), (5,6), (7,8), (6,8), (6,9), (8,9)])
    G.add_edges_from([(10,11), (10,12), (10,14), (11,12), (11,14), (11,13), (12,13)])

    # Agregar aristas adicionales
    G.add_edges_from([(3,10),(4,14),(2,14),(5,14),(7,14),(7,11),
                    (6,7),(2,6),(6,13)])
    
    return G


def PlotPagerank(G, centrality):
    fig, ax = plt.subplots()
    centrality_values = list(centrality.values())
    max_centrality = max(centrality_values)
    min_centrality = min(centrality_values)
    normalized_centrality = {node: (value - min_centrality) / (max_centrality - min_centrality) for node, value in centrality.items()}

    colors = [normalized_centrality[node] for node in G.nodes()]

    pos = nx.nx_agraph.graphviz_layout(G, prog='dot')
    # pos = nx.spring_layout(G)
    nx.draw(G, pos=pos, with_labels=True, node_color=colors, cmap=plt.cm.inferno, ax=ax)

    sm = plt.cm.ScalarMappable(cmap=plt.cm.inferno, norm=plt.Normalize(vmin=min_centrality, vmax=max_centrality))
    sm.set_array([])
    fig.colorbar(sm, orientation='vertical', ax=ax)
    ax.set_title("PageRank", fontsize=16)
    st.pyplot(fig)