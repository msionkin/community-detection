from graphIO import read_graph as rg
from graphIO import show_graph as sg
import louvain
from vkData import vk_data as vk


def main():
    #graph = rg.read_from_file("./data/test.txt")
    graph = rg.read_from_file("./data/several_circles1.txt")
    #sg.show_graph(graph, with_labels=True)
    '''
    user_id = 1
    graph = vk.get_friends_to_friends_graph(user_id)
    vk.get_friends_to_friends_file(user_id, file_path="./data/friends.txt")
    #graph = rg.read_from_file("./data/friends.txt")
    '''

    print(graph.number_of_edges())
    print(graph.number_of_nodes())
    print(graph.number_of_selfloops())

    pa = louvain.best_partition(graph)

    sg.print_graph_communities(pa)
    sg.show_graph_communities(graph, pa)

if __name__ == "__main__":
    main()
