from collections import defaultdict
from itertools import chain


def comms_from_file(file_path):
    """
    transform "12: 1,3,4" to {12: 1,3,4}
    """
    result = {}
    with open(file_path, 'r') as f:
        for line in f.readlines():
            comm, nodes = line.split(":")
            result[int(comm)] = list(map(int, nodes.split(",")))
    return result


def ground_truth_comms_from_file(file_path):
    """
    transform "1    3   4" to {0: 1,3,4}
    """
    result = {}
    with open(file_path, 'r') as f:
        for comm, line in enumerate(f.readlines()):
            nodes = line.split()
            result[comm] = list(map(int, nodes))
    return result


def communities_to_array(comms_dict):
    """
    transform  {12: 1,3,4} to [-1, 12, -1, 12, 12]
    """
    chn = chain.from_iterable(comms_dict.values())
    result = [1] * (max(chn) + 1)
    for comm, nodes in comms_dict.items():
        for node in nodes:
            result[node] = comm
    return result


def communities_to_array_from_file(file_path):
    result = []
    with open(file_path, 'r') as f:
        for comm, line in enumerate(f.readlines()):
            result.append(int(line))
    return result


def comms_from_file_fast_greedy(file_path):
    result = {}
    cur_comm = -1
    cur_nodes = []
    with open(file_path, 'r') as f:
        for line in f.readlines():
            if 'GROUP' in line:
                result[cur_comm] = cur_nodes
                cur_nodes = []
                cur_comm += 1
            else:
                cur_nodes.append(int(line))
        result[cur_comm] = cur_nodes
    del result[-1]
    return result


def comms_array_to_dict(comms_array):
    res = defaultdict(list)
    for node, comm in enumerate(comms_array):
        res[comm].append(node)
    return res


def comms_dict_to_file(comms_dict, output_file):
    """
    writes {12: 1,3,4} to "12: 1,3,4" to file
    """
    with open(output_file, 'w') as f:
        for comm, nodes in comms_dict.items():
            f.write("{}:\t{}\n".format(comm, ",".join(map(str, nodes))))
        f.flush()
