import networkx as nx
import numpy as np

def find_cluster(g):
    adj_matrix = g.values
    G = nx.from_numpy_array(adj_matrix)
    cliques = list(nx.find_cliques(G))
    unique_cliques = set(frozenset(c) for c in cliques)
    max_cliques = []
    for c in unique_cliques:
        if not any(set(c).issubset(set(m)) for m in max_cliques):
            max_cliques.append(list(c))
    cluster = []
    for i, c in enumerate(max_cliques):
        clusters = np.zeros_like(adj_matrix)
        clusters[np.ix_(c, c)] = adj_matrix[np.ix_(c, c)]
        cluster.append(clusters)

    return cluster