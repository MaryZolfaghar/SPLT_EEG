#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 09:08:45 2020

@author: Maryam
"""
import numpy as np
import argparse
import pickle

from modules.read_prep_epochs import read_prep_epochs
from modules.combine_subj_RTs import combine_subj_RTs

parser = argparse.ArgumentParser()

# Set Path
parser.add_argument("--SAVE_EPOCH_ROOT",
                    default='../data/preprocessed/epochs/aft_ICA_rej/',
                    help='Filename for saved preprocessed epochs')

parser.add_argument("--SAVE_RESULT_ROOT",
                    default='../results/temp_gen/',
                    help='Filename for saving the results')

# Conditions
parser.add_argument('--cond_filter', choices=['none','non_symm'],
                    default='none',
                    help='What type of filter should use')
parser.add_argument('--cond_block', choices=['early','later','diff'],
                    default='early',
                    help='Earlier blocks vs later blocks')
parser.add_argument('--cond_time', choices=['prestim','poststim'],
                    default='prestim',
                    help='Period of analysis related to the onset(stim presentation)')
parser.add_argument('--cond_decoding',
                    choices=['none','removeevoked','resampled'],
                    default='none',
                    help='Period of analysis related to the onset(stim presentation)')
parser.add_argument('--mtdt_feat',
                    choices=['Trgt_Loc_main','Trgt_Loc_prev'],
                    default='Trgt_Loc_main',
                    help='Metadata feature for group data according to)')

# EEG
parser.add_argument('--subj_num', type=int, default=1,
                    help='subject number')
parser.add_argument('--applyBaseline_bool', action='store_true',
                    help='apply baseline')
parser.add_argument('--pre_tmin', type=float, default=-0.4,
                    help='tmin crop for prestim period')
parser.add_argument('--pre_tmax', type=float, default=-0.05,
                    help='tmax crop for prestim period')
parser.add_argument('--post_tmin', type=float, default=0.05,
                    help='tmin crop for poststim period')
parser.add_argument('--post_tmax', type=float, default=0.45,
                    help='tmax crop for poststim period')
parser.add_argument('--occ_channels', action='store_true',
                    help='only choose channels in occipital areas')

parser.add_argument('--num_classes', type=int, default=2,
                    help='Number of classes to decode')
parser.add_argument('--normalization_type', choices=['normal','lstmPaper'],
                    default='normal',
                    help='Type of normalization')

# Permutation
parser.add_argument('--gen_rand_perm', action='store_true',
                    help='generate random permutation for each subject')
parser.add_argument('--null_max_iter', type=int, default=10000,
                    help='max num of iterations in generating null distribution')
parser.add_argument('--loop_null_iter', type=int, default=100,
                    help='max num of iterations in outer loop to go through sim')



# Decoder
parser.add_argument('--gen_decoder_scores', action='store_true',
                    help='generate decoder scores for each subject')
parser.add_argument('--n_splits', type=int, default=3,
                    help='How many folds to use for cross-validation')
parser.add_argument('--random_state', type=int, default=42,
                    help='random state in LinearSVC')
parser.add_argument('--max_iter', type=int, default=10000,
                    help='maximum num of iterations in LinearSVC')
parser.add_argument('--n_jobs', type=int, default=1,
                    help='Number of jobs to use for running the decoder')
parser.add_argument("--scoring",
                    default='roc_auc',
                    help='The scoring method using in decoder')

# Plot
parser.add_argument('--smooth_lvl', type=int, default=55,
                    help='smoothing level for savgol_filter')

"""
main function
"""
def main(args):
    # removed subjects : 17 22 37 27 17 25 27 70, issues are in the notes.txt
    # subj_indx = [ 1,  2,  3,  4,  5,  7,  8,  9, 10, 12, 15, 16, 18, 19, 20, 21,\
    #           23, 24, 26, 28, 29, 30, 31, 32, 33, 34, 35, 36, 38,\
    #           39, 42, 43, 44, 45, 46, 47, 48, 51, 52, 53, 55, 56, 57, 58, 59,\
    #           60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 71, 72, 73, 74]
    subj_indx = [ 1,  2,  3,  4,  5,  7,  8,  9, 10, 12, 15, 16, 18, 19, 20, 21,\
                  23, 24, 26, 28, 29, 30, 31, 32, 33, 34, 35, 36, 38,\
                  39, 43, 44, 45, 47, 48, 51, 52, 56, 57, 58, 59,\
                  60, 61, 63, 64, 66, 67, 68, 69, 71, 72, 73]

    RTs_Subjs = combine_subj_RTs(args, subj_indx)

    print('Combination of all subjects RTs has a shape of:', RTs_Subjs.shape)
    # ------ Pack all scores and save them
    fn_str = args.SAVE_RESULT_ROOT + 'RTs_all_subjs_SxGxB_%s.npy' %(args.mtdt_feat)
    with open(fn_str, 'wb') as f:
	    pickle.dump(RTs_Subjs, f)

    print('-------------------------------------------------------------------')
    print('Done saving')
"""
==============================================================================
Main
==============================================================================
"""
if __name__ == '__main__':
    args=parser.parse_args()
    print('-------Arguments:---------')
    print(args)
    print('--------------------------')
    main(args)
