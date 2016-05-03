import networkx as nx


def read_from_file(filename):
    graph = nx.Graph()
    with open(filename, "r") as f:
        for line in f:
            if line[0] == '#':
                continue
            edge_parts = line.split()
            if len(edge_parts) == 3:
                w = edge_parts[2]
            else:
                w = 1
            graph.add_edge(edge_parts[0], edge_parts[1], weight=float(w))
    return graph