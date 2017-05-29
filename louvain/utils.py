from collections import defaultdict


def partition_to_comm_nodes_map(partition):
    '''
    Transforms partition dict with {node: community} structure or
    partition list with comm1 \n comm2 \n comm1 structure
    to dict with {community: [list of its nodes]} structure
    '''
    comm_nodes = defaultdict(list)
    if type(partition) is dict:
        for node, comm in partition.items():
            comm_nodes[comm].append(node)
    elif type(partition) is list:
        for node, comm in enumerate(partition):
            comm_nodes[comm].append(node)
    return comm_nodes
