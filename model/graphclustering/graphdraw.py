import re
import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from graphclustering.clustering import find_cluster
import time

def make_G(read):
    data = read
    # data
    df = pd.DataFrame(data=None, columns=['from', 'to'])
    # df
    # Take all drugs listed in Antecedents and Consequences
    compound_from = []
    compound_to = []
    for i in range(data.iloc[:, 0].size - 1):
        row = data.values[i]
        pa = row[0]
        pb = row[1]
        # Continuous Chinese matching
        # com_obj = re.compile(r'[\u4e00-\u9fa5]+')

        com_obj = re.compile(r'\b[a-zA-Z ]+\b(?=,|$)')
        word_result_from = np.array(com_obj.findall(pa))
        word_result_to = np.array(com_obj.findall(pb))
        temp_1 = np.array(compound_from)
        temp_2 = np.array(compound_to)
        if (i != 0):
            compound_from = np.union1d(temp_1, word_result_from)
            compound_to = np.union1d(temp_2, word_result_to)
        else:
            compound_from = temp_1.tolist()
            compound_to = temp_2.tolist()

        if word_result_from.size > 1 and word_result_to.size > 1:
            if word_result_from.size >= word_result_to.size:
                for j in range(word_result_from.size):
                    for l in range(word_result_to.size):
                        df = df.append(
                            {
                                'from': word_result_from[j],
                                'to': word_result_to[l]
                            },
                            ignore_index=True)
                    for k in range(1, word_result_from.size - j):
                        df = df.append(
                            {
                                'from': word_result_from[j],
                                'to': word_result_from[j + k]
                            },
                            ignore_index=True)
            else:
                for j in range(word_result_to.size):
                    for l in range(word_result_from.size):
                        df = df.append(
                            {
                                'from': word_result_from[l],
                                'to': word_result_to[j]
                            },
                            ignore_index=True)
                    for k in range(1, word_result_to.size - j):
                        df = df.append(
                            {
                                'from': word_result_to[j],
                                'to': word_result_to[j + k]
                            },
                            ignore_index=True)
        elif word_result_from.size > 1 and word_result_to.size == 1:
            for j in range(word_result_from.size):
                df = df.append(
                    {
                        'from': word_result_from[j],
                        'to': word_result_to[0]
                    },
                    ignore_index=True)
                for k in range(1, word_result_from.size - j):
                    df = df.append(
                        {
                            'from': word_result_from[j],
                            'to': word_result_from[j + k]
                        },
                        ignore_index=True)
        elif word_result_from.size == 1 and word_result_to.size > 1:
            for j in range(word_result_from.size):
                df = df.append(
                    {
                        'from': word_result_from[0],
                        'to': word_result_to[j]
                    },
                    ignore_index=True)
                for k in range(1, word_result_from.size - j):
                    df = df.append(
                        {
                            'from': word_result_to[j],
                            'to': word_result_to[j + k]
                        },
                        ignore_index=True)
        else:
            df = df.append({
                'from': word_result_from[0],
                'to': word_result_to[0]
            },
                ignore_index=True)
    # print(compound_from)
    # print(compound_to)
    # df
    df_tab = pd.crosstab(df['from'], df['to'])
    # df_tab
    df_mtx = (df_tab + df_tab.T).fillna(df_tab).fillna(df_tab.T)
    df_mtx = df_mtx.fillna(0)
    # df_mtx
    G = df_mtx.values
    return df_mtx

def make_graph(df_mtx):
    subgraphs = find_cluster(df_mtx)
    subarr = np.array(subgraphs)
    inx = np.array(df_mtx.index)
    G_total = nx.Graph()

    for node in inx:
        G_total.add_node(node)

    for i, row in df_mtx.iterrows():
        for j, weight in row.iteritems():
            if weight > 0:
                G_total.add_edge(i, j, weight=weight)

    pos = nx.spring_layout(G_total)
    plt.figure(figsize=(16, 9))
    nx.draw_networkx_nodes(G_total, pos, node_size=500, node_color="yellow")
    nx.draw_networkx_labels(G_total, pos, font_size=10, font_family="sans-serif")
    nx.draw_networkx_edges(G_total, pos, width=1, edge_color="black")
    edge_labels = nx.get_edge_attributes(G_total, "weight")
    nx.draw_networkx_edge_labels(G_total, pos, edge_labels=edge_labels)

    plt.tight_layout()
    plt.title("Non-directional fully connected network graph")
    output_path = 'graph/non-directional_fully_connected_network_graph.png'
    plt.savefig(output_path, dpi=600, bbox_inches='tight')
    plt.show()
    print(output_path)
    time.sleep(5)

    k = 0
    # Subgraph number
    for adj_matrix in subarr:
        m = len(adj_matrix)
        G = nx.Graph()
        # Create an undirected graph

        if sum(1 for row in adj_matrix for element in row if element > 0) > 2:
            for i in range(m):
                for j in range((i + 1), m):
                    weight = adj_matrix[i][j]  # Get the weight of adjacency matrix
                    if weight != 0:  # If the weight is not 0, add edges

                        G.add_edge(inx[i], inx[j], weight=weight)
            k = k + 1

            pos = nx.spring_layout(G)
            plt.figure(figsize=(16, 9))
            nx.draw_networkx_nodes(G, pos, node_size=500, node_color="yellow")
            nx.draw_networkx_labels(G, pos, font_size=10, font_family="sans-serif")
            nx.draw_networkx_edges(G, pos, width=1, edge_color="black")
            edge_labels = nx.get_edge_attributes(G, "weight")
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
            plt.tight_layout()
            plt.title(f"Subgraph {k}")
            output_path = f"graph/subgraph_{k}.png"
            plt.savefig(output_path, dpi=600, bbox_inches='tight')
            plt.show()
            print(output_path)
            time.sleep(5)
