from slm.clustering import Clustering


class SmartLocalMoving(object):

    def __init__(self, network, resolution):
        self.network = network
        self.clustering = Clustering(network.n_nodes)
        self.clustering.init_singleton_clusters()
        self.resolution = resolution

    def run_slm(self):
        pass

    def calc_modularity(self):
        pass
