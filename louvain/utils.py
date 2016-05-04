from collections import defaultdict


def partition_to_comm_nodes_map(partition):
    '''
    Transforms partition dict with {node: community} structure
    to dict with {community: [list of its nodes]} structure
    '''
    comm_nodes = defaultdict(list)
    for node, comm in partition.items():
        comm_nodes[comm].append(node)
    return comm_nodes
