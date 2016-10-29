
def get_graph_edges(graph, for_igraph=False):
    if not for_igraph:
        return graph.edges
    edges = []
    for e in graph.edges():
        edges.append((int(e[0]), int(e[1])))
    return edges