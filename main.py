from graphIO import read_graph as rg
from graphIO import show_graph as sg
import louvain


def main():
    #graph = rg.read_from_file("./data/test.txt")
    graph = rg.read_from_file("./data/karate.txt")

    print(graph.number_of_edges())
    print(graph.number_of_nodes())
    print(graph.number_of_selfloops())

    pa = louvain.best_partition(graph)

    sg.print_graph_communities(pa)
    sg.show_graph_communities(graph, pa)

if __name__ == "__main__":
    main()
