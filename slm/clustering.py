
class Clustering:

    def __init__(self, n_nodes):
        self.n_nodes = n_nodes
        self.cluster = []
        self.n_clusters = 1

    def get_n_nodes_per_cluster(self):
        n_nodes_per_cluster = [0] * self.n_clusters
        for i in range(self.n_nodes):
            n_nodes_per_cluster[self.cluster[i]] += 1
        return n_nodes_per_cluster

    def get_nodes_per_cluster(self):
        node_per_cluster = [[] for _ in range(self.n_clusters)]
        for i in range(self.n_nodes):
            node_per_cluster[self.cluster[i]].append(i)
        return node_per_cluster

    def init_singleton_clusters(self):
        for i in range(self.n_nodes):
            self.cluster[i] = i
        self.n_clusters = self.n_nodes

    def sort_clusters_by_n_nodes(self):
        sorted(self.cluster, key=lambda nodes: len(nodes))

    def merge_clusters(self, clustering):
        for i in range(self.n_nodes):
            self.cluster[i] = clustering.cluster[self.cluster[i]]
        self.n_clusters = clustering.n_clusters
