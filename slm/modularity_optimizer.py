import time

from slm.slm import SmartLocalMoving


class ModularityOptimizer(object):
    def run(self, input_file_path="", output_file_path="",
            resolution=1.0, n_iterations=10, n_random_starts=10, print_output=False):

        if print_output:
            print("Reading input file...")
        network = self.read_input_file(input_file_path)

        if print_output:
            print("Number of nodes: {}".format(network.n_nodes))
            print("Number of edges: {}".format(network.get_n_edges()))
            print("Running smart local moving algorithm...")

        resolution2 = resolution / (2 * network.get_total_edge_weight() + network.total_edge_weight_self_links)

        start_time = time.time()
        clustering = None
        max_modularity = float('-inf')
        for i in range(n_random_starts):
            if print_output and n_random_starts > 1:
                print("Random start: {}".format(i + 1))

            smart_local_moving = SmartLocalMoving(network, resolution2)

            j = 0
            while j < n_iterations:
                if print_output and n_iterations > 1:
                    print("Iteration: {}".format(j + 1))
                smart_local_moving.run_slm()
                j += 1

                modularity = smart_local_moving.calc_modularity()
                if print_output and n_iterations > 1:
                    print("Modularity: {}".format(modularity))

            if modularity > max_modularity:
                clustering = smart_local_moving.clustering
                max_modularity = modularity

            if print_output and n_random_starts > 1:
                if n_iterations == 1:
                    print("Modularity: {}".format(modularity))

        end_time = time.time()

        if print_output:
            if n_random_starts == 1:
                if n_iterations > 1:
                    print("\n")
                print("Modularity: {}".format(max_modularity))
            else:
                print("Maximum modularity in {} random starts: {}".format(n_random_starts, max_modularity))
            print("Number of communities: {}".format(clustering.n_cluster))
            print("Elapsed time: {} seconds".format((end_time - start_time) / 1000.0))
            print("\n")
            print("Writing output file...")

        self.write_output_file(output_file_path, clustering)

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
            edge_weight1[j] = float(edge_parts[2]) if len(edge_parts) > 2 else 1
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
