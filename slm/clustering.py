
class Clustering:

    def __init__(self, n_nodes):
        self.n_nodes = n_nodes
        self.clusters = []
        self.n_clusters = 1

    def get_n_nodes_per_cluster(self):
        n_nodes_per_cluster = [0] * self.n_clusters
        for i in range(self.n_nodes):
            n_nodes_per_cluster[self.clusters[i]] += 1
        return n_nodes_per_cluster

    def get_nodes_per_cluster(self):
        node_per_cluster = [[] for _ in range(self.n_clusters)]
        for i in range(self.n_nodes):
            node_per_cluster[self.clusters[i]].append(i)
        return node_per_cluster

    def get_cluster(self, node):
        return self.clusters[node]

    def init_singleton_clusters(self):
        self.clusters = [i for i in range(self.n_nodes)]
        self.n_clusters = self.n_nodes

    def merge_clusters(self, clustering):
        for i in range(self.n_nodes):
            self.clusters[i] = clustering.clusters[self.clusters[i]]
        self.n_clusters = clustering.n_clusters
