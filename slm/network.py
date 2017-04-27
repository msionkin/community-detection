
class Network(object):

    def __init__(self, n_nodes=0, node_weight=None, first_neighbor_index=None, neighbor=None, edge_weight=None):
        self.n_nodes = n_nodes
        self.n_edges = 0 if neighbor is None else len(neighbor)
        self.first_neighbor_index = first_neighbor_index
        self.neighbor = neighbor
        if edge_weight is not None:
            self.edge_weight = edge_weight
        else:
            self.edge_weight = [1] * self.n_edges
        self.total_edge_weight_self_links = 0
        if node_weight is not None:
            self.node_weight = node_weight
        else:
            self.node_weight = self.get_total_edge_weight_per_node()

    def get_n_edges(self):
        return self.n_edges / 2

    def get_total_edge_weight_per_node(self):
        total_edge_weight_per_node = [0] * self.n_nodes
        for i in range(self.n_nodes):
            total_edge_weight_per_node[i] = sum(
                self.edge_weight[self.first_neighbor_index[i]:self.first_neighbor_index[i + 1]])
        return total_edge_weight_per_node

    def get_n_edges_per_node(self):
        n_edges_per_node = [0] * self.n_nodes
        for i in range(self.n_nodes):
            n_edges_per_node[i] = self.first_neighbor_index[i + 1] - self.first_neighbor_index[i]
        return n_edges_per_node

    def get_total_edge_weight(self):
        return sum(self.edge_weight) / 2

    def create_subnetwork(self, clustering, cluster, node,
                          subnetwork_node, subnetwork_neighbor, subnetwork_edge_weight):
        subnetwork = Network()
        subnetwork.n_nodes = len(node)

        if subnetwork.n_nodes == 1:
            subnetwork.n_edges = 0
            subnetwork.node_weight = [self.node_weight[node[0]]]
            subnetwork.first_neighbor_index = []
            subnetwork.neighbor = []
            subnetwork.edge_weight = []
        else:
            for i in range(len(node)):
                subnetwork_node[node[i]] = i

            subnetwork.n_edges = 0
            subnetwork.node_weight = [0] * subnetwork.n_nodes
            subnetwork.first_neighbor_index = [0] * (subnetwork.n_nodes + 1)
            for i in range(subnetwork.n_nodes):
                j = node[i]
                subnetwork.node_weight[i] = self.node_weight[j]
                for k in range(self.first_neighbor_index[j], self.first_neighbor_index[j + 1]):
                    if clustering.clusters[self.neighbor[k]] == cluster:
                        subnetwork_neighbor[subnetwork.n_edges] = subnetwork_node[self.neighbor[k]]
                        subnetwork_edge_weight[subnetwork.n_edges] = self.edge_weight[k]
                        subnetwork.n_edges += 1
                subnetwork.first_neighbor_index[i + 1] = subnetwork.n_edges
            subnetwork.neighbor = subnetwork_neighbor[0:subnetwork.n_edges]
            subnetwork.edge_weight = subnetwork_edge_weight[0:subnetwork.n_edges]

        subnetwork.total_edge_weight_self_links = 0

        return subnetwork

    def create_subnetworks(self, clustering):
        subnetworks = [None] * clustering.n_clusters
        node_per_cluster = clustering.get_nodes_per_cluster()
        subnetwork_node = [0] * self.n_nodes
        subnetwork_neighbor = [0] * self.n_edges
        subnetwork_edge_weight = [0] * self.n_edges
        for i in range(clustering.n_clusters):
            subnetworks[i] = self.create_subnetwork(clustering, i, node_per_cluster[i],
                                                    subnetwork_node, subnetwork_neighbor, subnetwork_edge_weight)
        return subnetworks

    def create_reduced_network(self, clustering):

        reduced_network = Network()

        reduced_network.n_nodes = clustering.n_clusters

        reduced_network.n_edges = 0
        reduced_network.node_weight = [0] * clustering.n_clusters
        reduced_network.first_neighbor_index = [0] * (clustering.n_clusters + 1)
        reduced_network.total_edge_weight_self_links = self.total_edge_weight_self_links
        reduced_network_neighbor1 = [0] * self.n_edges
        reduced_network_edge_weight1 = [0] * self.n_edges
        reduced_network_neighbor2 = [0] * (clustering.n_clusters - 1)
        reduced_network_edge_weight2 = [0] * clustering.n_clusters
        node_per_cluster = clustering.get_nodes_per_cluster()
        for i in range(clustering.n_clusters):
            j = 0
            for k in range(len(node_per_cluster[i])):
                l = node_per_cluster[i][k]

                reduced_network.node_weight[i] += self.node_weight[l]

                for m in range(self.first_neighbor_index[l], self.first_neighbor_index[l + 1]):
                    n = clustering.clusters[self.neighbor[m]]
                    if n != i:
                        if reduced_network_edge_weight2[n] == 0:
                            reduced_network_neighbor2[j] = n
                            j += 1
                        reduced_network_edge_weight2[n] += self.edge_weight[m]
                    else:
                        reduced_network.total_edge_weight_self_links += self.edge_weight[m]

            for k in range(j):
                reduced_network_neighbor1[reduced_network.n_edges + k] = reduced_network_neighbor2[k]
                reduced_network_edge_weight1[reduced_network.n_edges + k] = reduced_network_edge_weight2[reduced_network_neighbor2[k]]
                reduced_network_edge_weight2[reduced_network_neighbor2[k]] = 0
            reduced_network.n_edges += j
            reduced_network.first_neighbor_index[i + 1] = reduced_network.n_edges
        reduced_network.neighbor = reduced_network_neighbor1[0:reduced_network.n_edges].copy()
        reduced_network.edge_weight = reduced_network_edge_weight1[0:reduced_network.n_edges].copy()

        return reduced_network
