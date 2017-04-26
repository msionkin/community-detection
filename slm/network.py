
class Network(object):

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
