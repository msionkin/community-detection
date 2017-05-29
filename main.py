import time

from graphIO import read_graph as rg
from graphIO import show_graph as sg
from graphIO import utils
import igraph as ig
import louvain
from slm.modularity_optimizer import ModularityOptimizer
from vkData import vk_data as vk


def vk_test():
    user_id = 1
    #graph = vk.get_friends_to_friends_graph(user_id)
    #vk.get_friends_to_friends_file(user_id, file_path="./data/friends_my.txt")
    graph = rg.read_from_file("./data/friends_my_without_single.txt")
    print(graph.number_of_edges())
    print(graph.number_of_nodes())
    print(graph.number_of_selfloops())

    pa = louvain.best_partition(graph)

    sg.print_graph_communities(pa)
    sg.show_graph_communities(graph, pa)


def infomap_test(graph):
    '''
    :param graph: igraph.Graph 
    :return: None
    '''
    print("Infomap has been started")
    start_time = time.time()
    communities = graph.community_infomap()
    print("time : ", time.time() - start_time)
    modular = communities.modularity
    print('Infomap modularity: ', modular)
    # print('Infomap: ', communities, '\n')
    sg.write_graph_communities(communities.membership, "./data/vk_infomap.txt")


def walktrap_test(graph):
    '''
    :param graph: igraph.Graph 
    :return: None
    '''
    print("Walktrap has been started")
    start_time = time.time()
    communities = graph.community_walktrap()
    print("time : ", time.time() - start_time)
    modular = communities.as_clustering().modularity
    print('Walktrap modularity: ', modular)
    sg.write_graph_communities(communities.as_clustering().membership, "./data/vk_walktrap.txt")
    # print('Walktrap: ', communities, '\n')


def eigenvector_test(graph):
    '''
    :param graph: igraph.Graph 
    :return: None
    '''
    print("Eigen vector has been started")
    start_time = time.time()
    communities = graph.community_leading_eigenvector(weights=None, arpack_options=None)
    print("time : ", time.time() - start_time)
    modular = communities.modularity
    print('Eigen vector modularity: ', modular)
    sg.write_graph_communities(communities.membership, "./data/lj_eigenvector.txt")
    # print('Eigen vector: ', communities, '\n')


def label_propagation_test(graph):
    '''
    :param graph: igraph.Graph 
    :return: None
    '''
    print("Label propagation has been started")
    start_time = time.time()
    communities = graph.community_label_propagation()
    print("time : ", time.time() - start_time)
    modular = communities.modularity
    print('Label propagation modularity: ', modular)
    sg.write_graph_communities(communities.membership, "./data/vk_label_propagation.txt")
    # print('Label propagation: ', communities, '\n')


def fastgreedy_test(graph):
    '''
    :param graph: igraph.Graph 
    :return: None
    '''
    print("Fastgreedy has been started")
    start_time = time.time()
    communities = graph.community_fastgreedy()
    print("time : ", time.time() - start_time)
    modular = communities.as_clustering().modularity
    print('Fastgreedy modularity: ', modular)
    sg.write_graph_communities(communities.as_clustering().membership, "./data/vk_fastgreedy.txt")
    # print('Fastgreedy: ', communities, '\n')


def edge_betweenness_test(graph):
    '''
    :param graph: igraph.Graph 
    :return: None
    '''
    print("Edge betweenness has been started")
    start_time = time.time()
    communities = graph.community_edge_betweenness(directed=False)
    print("time : ", time.time() - start_time)
    modular = communities.as_clustering().modularity
    sg.write_graph_communities(communities.as_clustering().membership, "./data/vk_edge_betweenness.txt")
    print('Edge betweenness modularity: ', modular)
    # print('Edge betweenness: ', communities, '\n')


def louvain_test(graph):
    '''
    :param graph: networkx.Graph
    :return: None
    '''
    print("Louvain has been started started")
    start_time = time.time()
    pa = louvain.best_partition(graph)
    print("time : ", time.time() - start_time)
    modular = louvain.modularity(pa, graph)
    print('Louvain modularity: ', modular)
    # sg.print_graph_communities(pa)
    sg.write_graph_communities(pa, "./data/vk_louvain_source.txt")
    print('\n')


def run_all_tests(graph):
    walktrap_test(graph)
    infomap_test(graph)
    #louvain_test(graph)
    eigenvector_test(graph)
    label_propagation_test(graph)
    fastgreedy_test(graph)
    edge_betweenness_test(graph)


def main():
    nx_graph = rg.read_from_file("./data/karate.txt")
    igraph_graph = ig.Graph.Read_Ncol("./data/karate.txt", directed=False)
    igraph_graph = igraph_graph.simplify(multiple=True, loops=False)

    run_all_tests(igraph_graph)
    louvain_test(nx_graph)

    # ModularityOptimizer.run("./data/friends_my_without_single_zero_start_for_slm.txt", "./data/vk_slm.txt", print_output=True)

    # from utils import remove_unused_nodes
    # remove_unused_nodes("./data/com_lj_all_cmty_zero_start.txt", "./data/com_lj_ungraph_zero_start.txt")

    # vk_test()

    # from utils import translate_nodes
    # translate_nodes()

    # from utils import translate_nodes_to_source
    # translate_nodes_to_source("./data/vk_edge_betweenness.txt", "./data/friends_my_without_single_map.txt", "./data/vk_edge_betweenness_source.txt")
    # translate_nodes_to_source("./data/vk_eigenvector.txt", "./data/friends_my_without_single_map.txt", "./data/vk_eigenvector_source.txt")

    # df = corr_matr()

    # from vkData.vk_data import get_users_info
    # from utils import get_nodes_from_edges_file
    # from vkData.vk_data import get_users_names_map
    # from vkData.vk_data import id_to_names
    # vk_users_info = get_users_info(get_nodes_from_edges_file("./data/friends_my_without_single.txt"))
    # id_name_map = get_users_names_map(vk_users_info)
    # id_to_names("./results/vk_louvain_source.txt", id_name_map)


if __name__ == "__main__":
    main()
