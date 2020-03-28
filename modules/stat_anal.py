"""
Statistical analysis of results
"""
import mne
from utils.do_time_bin import do_time_bin

def stat_anal(scores_pck):
    indx=[26,51,76,101,126,151,176,201]

    score, score_diag = scores_pck
    score_subtract = score_diag - 0.5

    binned_score = do_time_bin(score, indx, 2)
    binned_score_diag = do_time_bin(score_diag, indx, 0)
    binned_score_subtract = do_time_bin(score_subtract, indx, 0)
    score_subtract=binned_score_subtract[:, np.newaxis, np.newaxis] # [:,:, np.newaxis] when added more subjects

    t_obs, clusters, clusters_pv, H0 = mne.stats.spatio_temporal_cluster_1samp_test(score_subtract, tail=0)
    clust_pck = [t_obs, clusters, clusters_pv, H0]

    return binned_score_diag, clust_pck
