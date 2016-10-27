from graphIO import read_graph as rg
from graphIO import show_graph as sg
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


def main():
    vk_test()


if __name__ == "__main__":
    main()
