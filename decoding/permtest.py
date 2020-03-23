#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 16:19:47 2020

@author: Maryam
"""
import argparse
import mne
import numpy as np
from sklearn.model_selection import StratifiedKFold#, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.pipeline import make_pipeline
from sklearn.svm import LinearSVC
from mne.decoding import LinearModel, SlidingEstimator


parser = argparse.ArgumentParser()

# Set Path
parser.add_argument("--SAVE_EPOCH_ROOT",
                    default='../../data/preprocessed/epochs/aft_ICA_rej/',
                    help='Filename for saved preprocessed epochs')

parser.add_argument("--SAVE_RESULT_ROOT",
                    default='../../results/decoding/permtest/',
                    help='Filename for saving the results')

# Conditions
parser.add_argument('--cond_filter', choices=['none','non_symm'],
                    default='none',
                    help='What type of filter should use')
parser.add_argument('--cond_block', choices=['early','later'],
                    default='early',
                    help='Earlier blocks vs later blocks')
parser.add_argument('--cond_time', choices=['prestim','poststim'],
                    default='prestim',
                    help='Period of analysis related to the onset(stim presentation)')
parser.add_argument('--cond_decoding', choices=['none','removeevoked','resampled'],
                    default='none',
                    help='Period of analysis related to the onset(stim presentation)')


# EEG
parser.add_argument('--subj_num', type=int, default=1,
                    help='subject number')
parser.add_argument('--applyBaseline_bool', action='store_true', 
                    default='True', help='apply baseline')
parser.add_argument('--pre_tmin', type=float, default=-0.4,
                    help='tmin crop for prestim period')
parser.add_argument('--pre_tmax', type=float, default=-0.05,
                    help='tmax crop for prestim period')
parser.add_argument('--post_tmin', type=float, default=0.05,
                    help='tmin crop for poststim period')
parser.add_argument('--post_tmax', type=float, default=-0.45,
                    help='tmax crop for poststim period')


parser.add_argument('--num_classes', type=int, default=2,
                    help='Number of classes to decode')
parser.add_argument('--normalization_type', choices=['normal','lstmPaper'],
                    default='normal',
                    help='Type of normalization')

# Permutation
parser.add_argument('--gen_rand_perm', action='store_true',
                    help='generate random permutation for each subject')
parser.add_argument('--null_max_iter', type=int, default=10,
                    help='max num of iterations in generating null distribution')

# Decoder
parser.add_argument('--n_splits', type=int, default=3,
                    help='How many folds to use for cross-validation')
parser.add_argument('--random_state', type=int, default=0,
                    help='random state in LinearSVC')
parser.add_argument('--max_iter', type=int, default=1000,
                    help='maximum num of iterations in LinearSVC')
parser.add_argument('--n_jobs', type=int, default=1,
                    help='Number of jobs to use for running the decoder')
parser.add_argument("--scoring",
                    default='roc_auc',
                    help='The scoring method using in decoder')




# """
# Set parameter
# """
# def set_params(args):
#     epchs = mne.read_epochs(args.SAVE_EPOCH_ROOT +
#     'epochs_sec_applyBaseline_subj1-afterRejICA-epo.fif',
#     proj=True, preload=True, verbose=None)
#     ##==========================================================================
#     epchs = epchs.pick_types(eeg=True)
#     set_param = epchs['pred']['non'].copy()
#     ##==========================================================================
#     if args.cond_block=='early': #block 3-6
#         set_param = set_param['Block<7'].copy()
#         set_param = set_param['Block>2'].copy()
#     elif args.cond_block=='later':#block 7-10
#         set_param = set_param['Block<11'].copy()
#         set_param = set_param['Block>6'].copy()
#     ##==========================================================================
#     if args.cond_time=='prestim':
#         set_param= set_param.crop(tmin=args.pre_tmin, tmax=args.pre_tmax)
#     elif args.cond_time=='poststim':
#         set_param= set_param.crop(tmin=args.post_tmin, tmax=args.post_tmax)
#     ##==========================================================================
#     n_chan  = set_param._data.shape[1]
#     n_times = set_param._data.shape[2]
#     ##========================================================================
#     return set_param, n_chan, n_times
"""
Apply a non-symmetric filter
"""
def apply_nonSymm_filter(epoch_data, frequencies):
    #filter epoch data
    flip_signal = np.flip(epoch_data._data.copy(), axis=-1)
    flip_signal_filt = mne.filter.filter_data(data=flip_signal,
                                              sfreq=epoch_data.info['sfreq'],
                                              l_freq=frequencies[0],
                                              h_freq=frequencies[-1],
                                              method='fir',
                                              fir_window='hamming',
                                              fir_design='firwin',
                                              phase='minimum',
                                              l_trans_bandwidth = 2,
                                              h_trans_bandwidth = 2,
                                              verbose=True)
    tfr = np.flip(flip_signal_filt.copy(), axis=-1)
    tfr_abs = np.abs(tfr)
    data_filt = tfr_abs ** 2  # power
    epoch_data._data = data_filt.copy()
    epoch_data_filt=epoch_data.copy()
    return epoch_data_filt
"""
Reading and preparing epoch data to create each 4 grous and 2 pattern
"""
def read_prep_epochs(args):
    if args.applyBaseline_bool:
        filename_epoch = args.SAVE_EPOCH_ROOT + \
                         'epochs_sec_applyBaseline_subj%s-afterRejICA-epo.fif' \
                          %args.subj_num
    else:
        filename_epoch = args.SAVE_EPOCH_ROOT + \
                         'epochs_sec_subj%s-afterRejICA-epo.fif' \
                         %args.subj_num
    epochs_orig = mne.read_epochs(filename_epoch, proj=True, preload=True,
                                  verbose=None)
    epochs = epochs_orig.copy()
    subset = epochs['pred']['non'].copy()
    subset = subset.pick_types(eeg=True)
    if (args.cond_decoding=='removeevoked'):
        # REMOVE EVOKED RESP.
        subset.subtract_evoked()    # remove evoked response
    elif (args.cond_decoding=='resampled'):
        # RESAMPLE
        subset = subset.resample(args.n_resampling, npad='auto')
    else:
        pass
    ##==========================================================================
    if subset['Block==7'].metadata.Ptrn_Type.values.shape[0]>0:
       main_ptrn = subset['Block==7'].metadata.Ptrn_Type.values[0]
    else:
       main_ptrn = subset['Block==8'].metadata.Ptrn_Type.values[0]
    ##==========================================================================
    if args.cond_block=='early': #block 3-6
        subset = subset['Block<7'].copy()
        subset = subset['Block>2'].copy()
    elif args.cond_block=='later':#block 7-10
        subset = subset['Block<11'].copy()
        subset = subset['Block>6'].copy()
    ##==========================================================================
    if (args.cond_time=='prestim'):
        subset= subset.crop(tmin=-0.4, tmax=0.05)
    if (args.cond_time=='poststim'):
        subset= subset.crop(tmin=0.05, tmax=0.45)
    ##==========================================================================
    # Group data based on the previous trial
    Grp1 = subset['Trgt_Loc_prev==1'].copy()
    Grp2 = subset['Trgt_Loc_prev==2'].copy()
    Grp3 = subset['Trgt_Loc_prev==3'].copy()
    Grp4 = subset['Trgt_Loc_prev==4'].copy()
    if main_ptrn==1:
        Grp1 = Grp1['Trgt_Loc_main!=4'].copy()
        Grp2 = Grp2['Trgt_Loc_main!=1'].copy()
        Grp3 = Grp3['Trgt_Loc_main!=2'].copy()
        Grp4 = Grp4['Trgt_Loc_main!=3'].copy()
    ##==========================================================================
    frequencies = np.arange(3, 13, 2)
    if args.cond_decoding=='non_symm':
        Grp1 = apply_nonSymm_filter(Grp1, frequencies)
        Grp2 = apply_nonSymm_filter(Grp2, frequencies)
        Grp3 = apply_nonSymm_filter(Grp3, frequencies)
        Grp4 = apply_nonSymm_filter(Grp4, frequencies)
    ##==========================================================================
    print('the pattern for this subj is :=====================================')
    print(main_ptrn)
    print('          ')
    print('===================================================================')
    ##==========================================================================
    # Normalizing the data for each subject
    if args.normalization_type=='normal':
        Grp1._data = (Grp1._data - np.mean(Grp1._data)) / np.std(Grp1._data)
        Grp2._data = (Grp2._data - np.mean(Grp2._data)) / np.std(Grp2._data)
        Grp3._data = (Grp3._data - np.mean(Grp3._data)) / np.std(Grp3._data)
        Grp4._data = (Grp4._data - np.mean(Grp4._data)) / np.std(Grp4._data)
    elif args.normalization_type=='lstmPaper':
        Grp1._data = (2 * (Grp1._data - np.min(Grp1._data))) \
                        / (np.max(Grp1._data) - np.min(Grp1._data) - 1)
        Grp2._data = (2 * (Grp2._data - np.min(Grp2._data))) \
                        / (np.max(Grp2._data) - np.min(Grp2._data) - 1)
        Grp3._data = (2 * (Grp3._data - np.min(Grp3._data))) \
                        / (np.max(Grp3._data) - np.min(Grp3._data) - 1)
        Grp4._data = (2 * (Grp4._data - np.min(Grp4._data))) \
                        / (np.max(Grp4._data) - np.min(Grp4._data) - 1)
    ##==========================================================================
    return Grp1, Grp2, Grp3, Grp4, main_ptrn
"""
Generate random data to create a null distribution
"""
def generate_rand(args, X, Y):
    null_scores=[]
    true_Y=Y.copy();
    for nitr in range(args.null_max_iter):
        # Y=true_Y.copy()
        cv = StratifiedKFold(n_splits=args.n_splits, shuffle=True)
        le = LabelEncoder()
        clf_SVC = make_pipeline(StandardScaler(),
                                LinearModel(LinearSVC(args.random_state,
                                                      args.max_iter)))
        indx=np.random.permutation(true_Y.shape[0]);
        shuffled_Y = true_Y.copy()[indx];
        shuffled_Y = le.fit_transform(shuffled_Y.copy());
        time_decod_clf = SlidingEstimator(clf_SVC, n_jobs=args.n_jobs,
                                          scoring=args.scoring)
        scores_clf = mne.decoding.cross_val_multiscore(time_decod_clf,
                                                       X, shuffled_Y,
                                                       cv=cv, n_jobs=args.n_jobs)
        scores_clf = np.mean(scores_clf, axis=0) # Mean scores across cv splits
        null_scores.append(scores_clf)
    return null_scores
"""
Apply decoder and generting null distribution as well
"""
def apply_decoder(args, Grp_data, fn_str):
    cv = StratifiedKFold(n_splits=args.n_splits, shuffle=True)
    le = LabelEncoder()
    clf_SVC  = make_pipeline(StandardScaler(),
                             LinearModel(LinearSVC(args.random_state,
                                                   args.max_iter)))
    X = Grp_data.copy()._data
    y = le.fit_transform(Grp_data.copy().metadata.Trgt_Loc_main)
    if args.gen_rand_perm:
        str_clf='clf_SVC'
        null_scores = generate_rand(args.null_max_iter, X, y)
        np.save(args.SAVE_RESULT_ROOT +'/null_scores_Grp1_ptrn1_%s_subj_%s.npy'
                %(str_clf, args.subj_num), null_scores, allow_pickle=True);
    else:
        time_decod_clf = SlidingEstimator(clf_SVC, n_jobs=1, scoring='roc_auc')
        scores_clf = mne.decoding.cross_val_multiscore(time_decod_clf, X, y,
                                                       cv=cv, n_jobs=args.n_jobs)
        scores_clf = np.mean(scores_clf, axis=0)# Mean scores across cv splits
        np.save(fn_str, scores_clf, allow_pickle=True);
    return scores_clf
"""
main function
"""
def main(args):
    [Grp1, Grp2, Grp3, Grp4, main_ptrn]=read_prep_epochs(args)


if __name__ == '__main__':
    args=parser.parse_args()
    print(args)
    print('--------------------------')
    main(args)
