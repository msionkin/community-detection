import louvain
import networkx as nx
from collections import defaultdict
import matplotlib.pyplot as plt
from graphIO import read_graph as rg


def main():
    graph = rg.read_from_file("./data/test.txt")
    print(graph.number_of_edges())
    print(graph.number_of_nodes())
    print(graph.number_of_selfloops())

    pa = louvain.best_partition(graph)

    communities = defaultdict(list)
    for elem, part in pa.items():
        communities[part].append(elem)

    for c, elems in communities.items():
        print (c, ": ", elems)

    color_map = {0: "red", 1: "green", 2: "blue", 3: "yellow"}
    count = 0
    pos = nx.spring_layout(graph)
    labels = {l: str(l) for l in graph.nodes()}
    for com in set(pa.values()):
        list_nodes = [nodes for nodes in pa.keys() if pa[nodes] == com]
        nx.draw_networkx_nodes(graph, pos, list_nodes, node_size=200, node_color=color_map[count])
        count += 1
    nx.draw_networkx_labels(graph, pos, labels, label_pos=0.3, font_size=16)
    nx.draw_networkx_edges(graph, pos, alpha=0.5)
    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    main()
