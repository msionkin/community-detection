import itertools

import pandas as pd
from sklearn.metrics import adjusted_mutual_info_score
from sklearn.metrics import jaccard_similarity_score
from sklearn.metrics import mutual_info_score
from sklearn.metrics import normalized_mutual_info_score
from sklearn.metrics import precision_recall_fscore_support as score

from metrics.utils import comms_from_file
from metrics.utils import comms_from_file_fast_greedy
from metrics.utils import communities_to_array
from metrics.utils import communities_to_array_from_file
from metrics.utils import ground_truth_comms_from_file


def prepare_gr_truth(gr_truth_file_path):
    ground_truth_comms = ground_truth_comms_from_file(gr_truth_file_path)
    gr_truth = communities_to_array(ground_truth_comms)
    return gr_truth


def prepare_comms(predicted_file_path):
    comms_predicted = comms_from_file(predicted_file_path)
    predicted = communities_to_array(comms_predicted)
    return predicted


def calc(gr_truth, predicted):
    # precision, recall, fscore, _ = score(gr_truth, predicted, average='micro')
    # print('precision: {}'.format(precision))
    # print('recall: {}'.format(recall))
    # print('fscore: {}'.format(fscore))
    # print('jaccard: {}'.format(jaccard_similarity_score(gr_truth, predicted, normalize=True)))
    # print('mutual: {}'.format(mutual_info_score(gr_truth, predicted)))
    # print('mutual adj: {}'.format(adjusted_mutual_info_score(gr_truth, predicted)))
    # print('mutual norm: {}'.format(normalized_mutual_info_score(gr_truth, predicted)))
    return normalized_mutual_info_score(gr_truth, predicted)


def calc_metrics():
    gr_truth = prepare_gr_truth("./data/com_lj_all_cmty_zero_start.txt")

    predicted = prepare_comms("./results/lj_label_propagation_reduced.txt")
    calc(gr_truth, predicted)
    print("-" * 50)

    predicted = communities_to_array_from_file("./results/lj_label_propagation_reduced.txt")
    calc(gr_truth, predicted)
    print("-" * 50)

    comms = comms_from_file_fast_greedy("./results/com_amazon_ungraph_zero_start_reduced-fc_a.groups")
    predicted = communities_to_array(comms)
    calc(gr_truth, predicted)


def corr_matr():
    louv = communities_to_array_from_file("./results/you_lovain.txt")
    slm = communities_to_array_from_file("./results/you_slm.txt")
    walk = prepare_comms("./results/you_walktrap.txt")
    label = prepare_comms("./results/you_label_propagation_reduced.txt")
    info = prepare_comms("./results/you_infomap.txt")
    fast = comms_from_file_fast_greedy("./results/com_youtube_ungraph_zero_start_reduced-fc_a.groups")
    fast = communities_to_array(fast)

    data = {'louv': louv, 'slm': slm, 'walk': walk, 'label': label, 'info': info, 'fast': fast}
    #data = {'louv': louv, 'slm': slm, 'walk': walk}
    columns = data.keys()
    df = pd.DataFrame(columns=columns, index=columns)
    for col_a, col_b in itertools.combinations_with_replacement(columns, 2):
        print(col_a, col_b)
        df[col_a][col_b] = calc(data[col_a], data[col_b])
    print(df)
    return df
