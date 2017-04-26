from graphIO import read_graph as rg
from graphIO import show_graph as sg
from graphIO import utils
import igraph as ig
import louvain
from vkData import vk_data as vk


def vk_test():
    user_id = 1
    #graph = vk.get_friends_to_friends_graph(user_id)
    #vk.get_friends_to_friends_file(user_id, file_path="./data/friends.txt")
    graph = rg.read_from_file("./data/friends.txt")
    print(graph.number_of_edges())
    print(graph.number_of_nodes())
    print(graph.number_of_selfloops())

    pa = louvain.best_partition(graph)

    sg.print_graph_communities(pa)
    sg.show_graph_communities(graph, pa)


def infomap_test(graph):
    cg = ig.Graph(utils.get_graph_edges(graph, True))
    communities = cg.community_infomap()
    modular = communities.modularity
    print('Infomap modularity: ', modular)
    print('Infomap: ', communities, '\n')


def walktrap_test(graph):
    cg = ig.Graph(utils.get_graph_edges(graph, True))
    communities = cg.community_walktrap()
    modular = communities.as_clustering(n=4).modularity
    print('Walktrap modularity: ', modular)
    print('Walktrap: ', communities, '\n')


def eigenvector_test(graph):
    cg = ig.Graph(utils.get_graph_edges(graph, True))
    communities = cg.community_leading_eigenvector()
    modular = communities.modularity
    print('Eigen vector modularity: ', modular)
    print('Eigen vector: ', communities, '\n')


def label_propagation_test(graph):
    cg = ig.Graph(utils.get_graph_edges(graph, True))
    communities = cg.community_label_propagation()
    modular = communities.modularity
    print('Label propagation modularity: ', modular)
    print('Label propagation: ', communities, '\n')


def fastgreedy_test(graph):
    cg = ig.Graph(utils.get_graph_edges(graph, True))
    communities = cg.community_fastgreedy()
    modular = communities.as_clustering(n=4).modularity
    print('Fastgreedy modularity: ', modular)
    print('Fastgreedy: ', communities, '\n')


def edge_betweenness_test(graph):
    cg = ig.Graph(utils.get_graph_edges(graph, True))
    communities = cg.community_edge_betweenness(directed=False)
    modular = communities.as_clustering(n=4).modularity
    print('Edge betweenness modularity: ', modular)
    print('Edge betweenness: ', communities, '\n')


def louvain_test(graph):
    pa = louvain.best_partition(graph)
    modular = louvain.modularity(pa, graph)
    print('Louvain modularity: ', modular)
    print('Louvain:')
    sg.print_graph_communities(pa)
    print('\n')


def run_all_tests(graph):
    walktrap_test(graph)
    infomap_test(graph)
    louvain_test(graph)
    eigenvector_test(graph)
    label_propagation_test(graph)
    fastgreedy_test(graph)
    edge_betweenness_test(graph)


def main():
    print("TWO CIRCLES:")
    graph = rg.read_from_file("./data/two_circles.txt")
    run_all_tests(graph)

    print("=" * 100)

    print("KARATE:")
    graph = rg.read_from_file("./data/karate.txt")
    run_all_tests(graph)


if __name__ == "__main__":
    main()
