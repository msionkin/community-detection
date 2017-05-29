import random

import colorsys
import matplotlib.pyplot as plt
import networkx as nx

from louvain import utils


def generate_color_map(partition):
    communities = utils.partition_to_comm_nodes_map(partition).keys()
    n = len(communities)

    hsv_tuples = [(x * 1.0 / n, 0.8, 0.7) for x in range(n)]
    rgb_tuples = map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples)

    return dict(zip(communities, rgb_tuples))


def show_graph_communities(graph, partition, color_map=None, with_labels=False):
    if color_map is None:
        color_map = generate_color_map(partition)
    pos = nx.spring_layout(graph,k=0.1,iterations=50)
    comm_nodes = utils.partition_to_comm_nodes_map(partition)
    for comm, nodes in comm_nodes.items():
        nx.draw_networkx_nodes(graph, pos, nodelist=nodes, node_size=400,
                               node_color=color_map.get(comm), label=comm, cmap=plt.cm.jet)
    if with_labels:
        nx.draw_networkx_labels(graph, pos, font_size=12)
    nx.draw_networkx_edges(graph, pos, alpha=0.3)
    plt.legend()
    plt.axis('off')
    plt.show()


def show_graph(graph, with_labels=False):
    pos = nx.spring_layout(graph)
    nx.draw_networkx_nodes(graph, pos, node_size=200, node_color='red')
    if with_labels:
        nx.draw_networkx_labels(graph, pos, font_size=12)
    nx.draw_networkx_edges(graph, pos, alpha=0.3)
    plt.axis('off')
    plt.show()


def draw_circular_graph(graph):
    graph = nx.cycle_graph(graph.number_of_nodes(), graph)
    nx.draw_circular(graph)
    plt.axis('off')
    plt.show()


def print_graph_communities(partition):
    comm_nodes = utils.partition_to_comm_nodes_map(partition)
    for comm, nodes in comm_nodes.items():
        print("{}: {}".format(comm, ",".join(list(map(str, sorted(nodes))))))


def write_graph_communities(partition, file_path):
    comm_nodes = utils.partition_to_comm_nodes_map(partition)
    with open(file_path, 'w') as f:
        for comm, nodes in comm_nodes.items():
            f.write("{}: {}\n".format(comm, ",".join(map(str, sorted(nodes, key=lambda x: int(x))))))
        f.flush()
