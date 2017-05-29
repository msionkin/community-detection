import time

import networkx
from vk.exceptions import VkAPIError

from metrics.utils import comms_from_file
from vkData.vk_api import vkapi


def get_friends_ids(user_id):
    try:
        return vkapi.friends.get(user_id=int(user_id)).get('items')
    except VkAPIError as e:
        print(e)  # TODO: add logging
        return []


def get_friends_to_friends_map(user_id):
    """
    Returns dict in which keys are friends of the given user and
    values are list of friends of key-friend
    """
    map = {}
    user_friend_ids = get_friends_ids(user_id)
    count = 0
    for friend in user_friend_ids:
        print ('Processing id: ', friend)
        count += 1
        if count % 3 == 0:
            time.sleep(2)
        map[friend] = get_friends_ids(friend)
    return map


def get_friends_to_friends_links(f_to_f_map, with_self_loops=True):
    """
    Returns list of tuples with links between friends:
    [
    (friend1, friend2),
    (friend1, friend10),
     ...
    (friend10, friend4)
    ]
    """
    links = []
    for friend, its_friends in f_to_f_map.items():
        for fr in its_friends:
            if friend != fr and fr in f_to_f_map.keys():
                links.append((friend, fr))
        if with_self_loops:
            links.append((friend, friend))
    return links


def get_friends_to_friends_graph(user_id):
    """
    Returns networkx graph of friends of given user in which
    edge between two friends if and only if they are friends and
    if both are friends of a given user
    """
    g = networkx.Graph(directed=False)
    f_to_f_map = get_friends_to_friends_map(user_id)
    edges = get_friends_to_friends_links(f_to_f_map)
    for fr1, fr2 in edges:
        g.add_edge(fr1, fr2)
    return g


def get_friends_to_friends_file(user_id, file_path):
    """
    Returns file with links between friends of a given user in which
    link between two friends if and only if they are friends and
    if both are friends of a given user
    """
    f_to_f_map = get_friends_to_friends_map(user_id)
    edges = get_friends_to_friends_links(f_to_f_map)
    with open(file_path, 'w') as f:
        for fr1, fr2 in edges:
            f.write("{}\t{}\n".format(fr1, fr2))


def get_users_info(users_ids_list):
    users_ids = ",".join(users_ids_list)
    try:
        return vkapi.users.get(user_ids=users_ids)
    except VkAPIError as e:
        print(e)  # TODO: add logging
        return []


def get_users_names_map(vk_users_info):
    res = {}
    for user_info in vk_users_info:
        res[user_info.get('id')] = "{}_{}".format(user_info.get('last_name'), user_info.get('first_name'))
    return res


def write_users_names_to_file(users_names, output_file):
    with open(output_file, 'w') as f:
        for user_info in users_names:
            f.write("{}\t{}_{}\n".format(user_info.get('id'), user_info.get('last_name'), user_info.get('first_name')))
        f.flush()


def id_to_names(input_file, id_name_map):
    output_file = input_file.replace('.txt', '_names.txt')
    comms = comms_from_file(input_file)
    with open(output_file, 'w') as fw:
        for comm, nodes in comms.items():
            fw.write("{}\t{}\n".format(comm, ", ".join([id_name_map[n] for n in nodes])))
