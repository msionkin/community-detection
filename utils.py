from os import path


def translate_to_zero_start(inf, ouf):
    """
    Moves labels of nodes by 1 down

    :param inf: path to input file with 'a b' structure
    :param ouf: path to output file with 'a-1 b-1' structure
    :return: None
    """
    with open(inf, 'r') as f, open(ouf, 'w') as of:
        for line in f:
            nodes = list(map(int, line.split()))
            res = "\t".join(list(map(str, map(lambda x: x-1, nodes))))
            of.write(res + "\n")
        of.flush()


def remove_unused_nodes(all_comms_file, all_nodes_file):
    """
    Removes nodes from all_nodes_file that doesn't exist in all_comms_file  
    
    :param all_comms_file: path to file with nodes: a b \n c \n d e f 
    :param all_nodes_file: path to file with nodes: a c \n d e
    :return: None, creates new file with only nodes from all_nodes_file that all_comms_file contains  
    """
    output_f = "{}_reduced.txt".format(all_nodes_file.replace(".txt", ""))
    with open(all_comms_file, 'r') as comms_f, open(all_nodes_file) as nodes_f, open(output_f, 'w') as out_f:
        comms = set(comms_f.read().split())
        for line in nodes_f.readlines():
            if all(node in comms for node in line.split()):
                out_f.write(line)
        out_f.flush()


def translate_nodes(in_file_path):
    #in_file_path = "./data/friends_my_without_single.txt"
    basename = path.splitext(in_file_path)[0]
    ext = path.splitext(in_file_path)[1]

    nodes = set()
    with open(in_file_path, 'r') as f:
        for line in f:
            edge_parts = list(map(int, map(str.strip, line.split())))
            nodes.add(edge_parts[0])
            nodes.add(edge_parts[1])
    nodes = sorted(nodes)

    map_file_path = "{}_map{}".format(basename, ext)
    nodes_map = {}
    i = 0
    with open(map_file_path, 'w') as fm:
        for node in nodes:
            nodes_map[node] = i
            fm.write("{}\t{}\n".format(node, i))
            i += 1
        fm.flush()

    result_file = "{}_zero_start{}".format(basename, ext)
    result = []
    with open(result_file, 'w') as fw, open(in_file_path, 'r') as fr:
        for line in fr:
            edge_parts = list(map(int, map(str.strip, line.split())))
            result.append((nodes_map[edge_parts[0]], nodes_map[edge_parts[1]]))

        for e1, e2 in sorted(result, key=lambda tup: tup[0]):
            fw.write("{}\t{}\n".format(e1, e2))
        fw.flush()


def _get_nodes_map(map_file):
    # map_file = "./data/friends_my_without_single_map.txt"
    nodes_map = {}

    with open(map_file, 'r') as f:
        for line in f:
            edge_parts = list(map(int, map(str.strip, line.split())))
            nodes_map[edge_parts[1]] = edge_parts[0]
    return nodes_map


def translate_nodes_to_source(input_file, map_file, output_file):
    """
    Translates nodes to their source representation

    :param input_file: 12: 1,3,4 
    :param map_file: 3646 1\n677 3\n8787 4
    :param output_file: 12: 3646,677,8787
    :return: None
    """
    nm = _get_nodes_map(map_file)
    with open(input_file, 'r') as fr, open(output_file, 'w') as fw:
        for line in fr:
            comm, nodes = line.split(":")
            nodes_list = list(map(int, map(str.strip, nodes.split(","))))
            nodes_list = map(str, [nm[node] for node in nodes_list])
            fw.write("{}: {}\n".format(comm, ",".join(nodes_list)))
        fw.flush()


def remove_multiple_edges(inf, ouf):
    """
    Removes all edges from inf file that have multiple occurrence

    :param inf: path to file with edges: 'a b \n c d'
    :param ouf: path to output file
    :return: None
    """
    edges = set()
    with open(inf, 'r') as fr, open(ouf, 'w') as fw:
        for line in fr:
            edge_parts = list(map(int, map(str.strip, line.split())))
            if (edge_parts[1], edge_parts[0]) not in edges:
                edges.add((edge_parts[0], edge_parts[1]))

        for e1, e2 in sorted(edges, key=lambda tup: tup[0]):
            fw.write("{}\t{}\n".format(e1, e2))
        fw.flush()


def get_nodes_from_edges_file(file_path):
    nodes = set()
    with open(file_path, 'r') as f:
        for line in f:
            edge_parts = list(map(str.strip, line.split()))
            nodes.add(edge_parts[0])
            nodes.add(edge_parts[1])
    return list(nodes)
