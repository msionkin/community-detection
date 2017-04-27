import random

from slm.clustering import Clustering


class SmartLocalMoving(object):

    def __init__(self, network, resolution):
        self.network = network
        self.clustering = Clustering(network.n_nodes)
        self.clustering.init_singleton_clusters()
        self.resolution = resolution

    def calc_modularity(self):
        modularity = 0
        for i in range(self.network.n_nodes):
            j = self.clustering.clusters[i]
            for k in range(self.network.first_neighbor_index[i], self.network.first_neighbor_index[i + 1]):
                if self.clustering.clusters[self.network.neighbor[k]] == j:
                    modularity += self.network.edge_weight[k]
        modularity += self.network.total_edge_weight_self_links
        cluster_weight = [0] * self.clustering.n_clusters
        for i in range(self.network.n_nodes):
            cluster_weight[self.clustering.clusters[i]] += self.network.node_weight[i]
        for i in range(self.clustering.n_clusters):
            modularity -= cluster_weight[i] * cluster_weight[i] * self.resolution
        modularity /= 2.0 * self.network.get_total_edge_weight() + self.network.total_edge_weight_self_links
        return modularity

    def _run_local_moving_algorithm(self):
        if self.network.n_nodes == 1:
            return False
        update = False
        cluster_weight = [0] * self.network.n_nodes
        n_nodes_per_cluster = [0] * self.network.n_nodes
        for i in range(self.network.n_nodes):
            cluster_weight[self.clustering.clusters[i]] += self.network.node_weight[i]
            n_nodes_per_cluster[self.clustering.clusters[i]] += 1

        n_unused_clusters = 0
        unused_cluster = [0] * self.network.n_nodes
        for i in range(self.network.n_nodes):
            if n_nodes_per_cluster[i] == 0:
                unused_cluster[n_unused_clusters] = i
                n_unused_clusters += 1

        node_permutation = [x for x in range(self.network.n_nodes)]
        random.shuffle(node_permutation)

        edge_weight_per_cluster = [0] * self.network.n_nodes
        neighboring_cluster = [0] * (self.network.n_nodes - 1)
        n_stable_nodes = 0
        i = 0
        while n_stable_nodes < self.network.n_nodes:
            j = node_permutation[i]
            n_neighboring_clusters = 0
            for k in range(self.network.first_neighbor_index[j], self.network.first_neighbor_index[j + 1]):
                l = self.clustering.clusters[self.network.neighbor[k]]
                if edge_weight_per_cluster[l] == 0:
                    neighboring_cluster[n_neighboring_clusters] = l
                    n_neighboring_clusters += 1
                    edge_weight_per_cluster[l] += self.network.edge_weight[k]

            cluster_weight[self.clustering.clusters[j]] -= self.network.node_weight[j]
            n_nodes_per_cluster[self.clustering.clusters[j]] -= 1
            if n_nodes_per_cluster[self.clustering.clusters[j]] == 0:
                unused_cluster[n_unused_clusters] = self.clustering.clusters[j]
                n_unused_clusters += 1

            best_cluster = -1
            max_modularity = 0
            for k in range(n_neighboring_clusters):
                l = neighboring_cluster[k]
                modularity = edge_weight_per_cluster[l] - self.network.node_weight[j] * cluster_weight[l] * self.resolution
                if (modularity > max_modularity) or (modularity == max_modularity and l < best_cluster):
                    best_cluster = l
                    max_modularity = modularity
                edge_weight_per_cluster[l] = 0

            if max_modularity == 0:
                best_cluster = unused_cluster[n_unused_clusters - 1]
                n_unused_clusters -= 1

            cluster_weight[best_cluster] += self.network.node_weight[j]
            n_nodes_per_cluster[best_cluster] += 1
            if best_cluster == self.clustering.clusters[j]:
                n_stable_nodes += 1
            else:
                self.clustering.clusters[j] = best_cluster
                n_stable_nodes = 1
                update = True
            i = i + 1 if (i < self.network.n_nodes - 1) else 0

        new_cluster = [0] * self.network.n_nodes
        self.clustering.n_clusters = 0
        for i in range(self.network.n_nodes):
            if n_nodes_per_cluster[i] > 0:
                new_cluster[i] = self.clustering.n_clusters
                self.clustering.n_clusters += 1

        for i in range(self.network.n_nodes):
            self.clustering.clusters[i] = new_cluster[self.clustering.clusters[i]]

        return update

    def run_smart_local_moving(self):
        if self.network.n_nodes == 1:
            return False

        update = self._run_local_moving_algorithm()

        if self.clustering.n_clusters < self.network.n_nodes:
            subnetworks = self.network.create_subnetworks(self.clustering)

            node_per_cluster = self.clustering.get_nodes_per_cluster()

            self.clustering.n_clusters = 0
            n_nodes_per_cluster_reduced_network = [0] * len(subnetworks)
            for i in range(len(subnetworks)):
                smart_local_moving = SmartLocalMoving(subnetworks[i], self.resolution)

                smart_local_moving._run_local_moving_algorithm()

                for j in range(subnetworks[i].n_nodes):
                    self.clustering.clusters[node_per_cluster[i][j]] = self.clustering.n_clusters + smart_local_moving.clustering.clusters[j]
                self.clustering.n_clusters += smart_local_moving.clustering.n_clusters
                n_nodes_per_cluster_reduced_network[i] = smart_local_moving.clustering.n_clusters

            smart_local_moving = SmartLocalMoving(self.network.create_reduced_network(self.clustering), self.resolution)

            i = 0
            for j in range(len(n_nodes_per_cluster_reduced_network)):
                for k in range(n_nodes_per_cluster_reduced_network[j]):
                    smart_local_moving.clustering.clusters[i] = j
                    i += 1
            smart_local_moving.clustering.n_clusters = len(n_nodes_per_cluster_reduced_network)

            update |= smart_local_moving.run_smart_local_moving()

            self.clustering.merge_clusters(smart_local_moving.clustering)

        return update
