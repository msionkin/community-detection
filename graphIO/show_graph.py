import random

import matplotlib.pyplot as plt
import networkx as nx

from louvain import utils


def generate_color_map(partition):
    communities = utils.partition_to_comm_nodes_map(partition).keys()
    color_map = {}
    r = lambda: random.randint(0, 255)
    for comm in communities:
        color_map[comm] = '#%02X%02X%02X' % (r(), r(), r())
    return color_map


def show_graph_communities(graph, partition, color_map=None, with_labels=False):
    if color_map is None:
        color_map = generate_color_map(partition)
    pos = nx.spring_layout(graph)
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


def print_graph_communities(partition):
    comm_nodes = utils.partition_to_comm_nodes_map(partition)
    for comm, nodes in comm_nodes.items():
        print ("{}: {}".format(comm, nodes))