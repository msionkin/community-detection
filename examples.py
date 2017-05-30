
def array_result_to_dict_result():
    from metrics.utils import comms_array_to_dict
    from metrics.utils import communities_to_array_from_file
    from metrics.utils import comms_dict_to_file

    comms_array = communities_to_array_from_file("./results/vk_slm.txt")
    comms_dict = comms_array_to_dict(comms_array)
    comms_dict_to_file(comms_dict, "./results/vk_slm_res.txt")


def remove_unused_nodes():
    from utils import remove_unused_nodes
    remove_unused_nodes("./data/com_lj_all_cmty_zero_start.txt", "./data/com_lj_ungraph_zero_start.txt")


def transform_user_ids_to_numbers_from_zero():
    from utils import translate_nodes
    translate_nodes("./data/friends_my_without_single.txt")


def translate_user_ids_to_names():
    from vkData import vk_data as vk
    from utils import get_nodes_from_edges_file

    vk_users_info = vk.get_users_info(get_nodes_from_edges_file("./results/friends_my_without_single.txt"))
    id_name_map = vk.get_users_names_map(vk_users_info)
    vk.id_to_names("./results/vk_louvain_source.txt", id_name_map)


def translate_nodes_to_user_ids():
    from utils import translate_nodes_to_source

    translate_nodes_to_source("./results/vk_slm_res.txt",
                              "./results/friends_my_without_single_map.txt",
                              "./results/vk_slm_source.txt")
    # translate_nodes_to_source("./data/vk_edge_betweenness.txt",
    #                           "./data/friends_my_without_single_map.txt",
    #                           "./data/vk_edge_betweenness_source.txt")
    # translate_nodes_to_source("./data/vk_eigenvector.txt",
    #                           "./data/friends_my_without_single_map.txt",
    #                           "./data/vk_eigenvector_source.txt")


def calc_corr_matrix():
    from metrics.metrics import corr_matr
    df = corr_matr()