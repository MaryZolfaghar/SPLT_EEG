#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 09:08:45 2020

@author: Maryam
"""
import numpy as np
import argparse
import pickle

from sklearn.model_selection import StratifiedKFold, cross_val_score, StratifiedShuffleSplit, \
                                    RepeatedStratifiedKFold

from modules.read_prep_epochs import read_prep_epochs
from modules.apply_temp_gen import apply_temp_gen
from utils.generate_correlation_map import generate_correlation_map

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
parser.add_argument('--loop_null_iter', type=int, default=5,
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
"""
main function
"""
def main(args):
    [Grp1, Grp2, Grp3, Grp4, main_ptrn] = read_prep_epochs(args)

    map_G1 = generate_correlation_map(Grp1)
    map_G2 = generate_correlation_map(Grp2)
    map_G3 = generate_correlation_map(Grp3)
    map_G4 = generate_correlation_map(Grp4)


    fn_str_sbj='autocorr_%sBlocks_%sFilter_PrePost_decod%s_bsline%s_%sk_Subj_%s' \
            %(args.cond_block, args.cond_filter, \
            args.cond_decoding, args.applyBaseline_bool, \
            args.n_splits, args.subj_num)

    avg_map= np.zeros([4, map_G1.shape[0], map_G1.shape[1]])
    avg_map[0,:,:] = map_G1
    avg_map[1,:,:] = map_G2
    avg_map[2,:,:] = map_G3
    avg_map[3,:,:] = map_G4
    avg_map = np.mean(avg_map, axis=0)

    # ------ Pack all scores and save them
    fn_str = args.SAVE_RESULT_ROOT + 'avgP%s_' %(main_ptrn) + fn_str_sbj
    with open(fn_str, 'wb') as f:
	    pickle.dump(avg_map, f)

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
