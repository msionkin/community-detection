import matplotlib.pyplot as plt
import networkx as nx

from louvain import utils


def show_graph_communities(graph, partition, color_map=None):
    if color_map is None:
        color_map = {0: "red", 1: "green", 2: "blue", 3: "yellow"}
    count = 0
    pos = nx.spring_layout(graph)
    labels = {l: str(l) for l in graph.nodes()}
    comm_nodes = utils.partition_to_comm_nodes_map(partition)
    for comm, nodes in comm_nodes.items():
        nx.draw_networkx_nodes(graph, pos, nodes, node_size=200, node_color=color_map[count])
        count += 1
    nx.draw_networkx_labels(graph, pos, labels, label_pos=0.3, font_size=16)
    nx.draw_networkx_edges(graph, pos, alpha=0.5)
    plt.axis('off')
    plt.show()


def print_graph_communities(partition):
    comm_nodes = utils.partition_to_comm_nodes_map(partition)
    for comm, nodes in comm_nodes.items():
        print ("{}: {}".format(comm, nodes))