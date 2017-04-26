
class ModularityOptimizer(object):

    def read_input_file(self, file_path):
        with open(file_path, 'r') as f:
            content = f.readlines()
        n_lines = len(content)
        node1 = [0] * n_lines
        node2 = [0] * n_lines
        edge_weight1 = [0] * n_lines
        i = -1
        for j in range(n_lines):
            edge_parts = content[j].split()
            node1[j] = int(edge_parts[0])
            if node1[j] > i:
                i = node1[j]
            node2[j] = int(edge_parts[1])
            if node2[j] > i:
                i = node2[j]
            edge_weight1[j] = float(edge_parts[2]) if len(edge_parts)> 2 else 1
        n_nodes = i + 1

        n_neighbors = [0] * n_nodes
        for i in range(n_lines):
            if node1[i] < node2[i]:
                n_neighbors[node1[i]] += 1
                n_neighbors[node2[i]] += 1

        first_neighbor_index = [0] * (n_nodes + 1)
        n_edges = 0
        for i in range(n_nodes):
            first_neighbor_index[i] = n_edges
            n_edges += n_neighbors[i]
        first_neighbor_index[n_nodes] = n_edges

        neighbor = [0] * n_edges
        edge_weight2 = [0] * n_edges
        n_neighbors = [0] * n_nodes
        for i in range(n_lines):
            if node1[i] < node2[i]:
                j = first_neighbor_index[node1[i]] + n_neighbors[node1[i]]
                neighbor[j] = node2[i]
                edge_weight2[j] = edge_weight1[i]
                n_neighbors[node1[i]] += 1

                j = first_neighbor_index[node2[i]] + n_neighbors[node2[i]]
                neighbor[j] = node1[i]
                edge_weight2[j] = edge_weight1[i]
                n_neighbors[node2[i]] += 1
        return Network(n_nodes, first_neighbor_index, neighbor, edge_weight2)

    def write_output_file(self, file_path, clustering):
        n_nodes = clustering.n_nodes
        clustering.sort_clusters_by_n_nodes()

        with open(file_path, 'w') as f:
            for i in range(n_nodes):
                f.write(str(clustering.get_cluster(i)) + "\n")
            f.flush()
