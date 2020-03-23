#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 16:19:47 2020

@author: Maryam
"""
import argparse
import mne

parser = argparse.ArgumentParser()

# Set Path
parser.add_argument("--SAVE_EPOCH_ROOT", default='../data/preprocessed/epochs/',
                    help='Filename for saved preprocessed epochs')

parser.add_argument("--SAVE_RESULT_ROOT", default='../results/permtest/',
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
                    help='Period of analysis related to the onset (stimulus presentation)')



"""
Set parameter
"""
def set_params(cond_block, cond_time, SAVE_EPOCH_ROOT):
    pass
def main_read_gen_stat():
    pass

####=========
def main(args):
    path=args.SAVE_RESULT_ROOT+ 'results_filter_400%s' %(args.cond_time)+ '/' + '%s' %(args.cond_filter) + '/'

if __name__ == '__main__':
    args=parser.parse_args()
    print(args.cond_filter)
    print('--------------------------')
    main(args)
#[epochs_smpl, n_chan, n_times]=set_params(cond_block, cond_time, SAVE_EPOCH_ROOT)
#extent_time=epochs_smpl.times[[0, -1, 0, -1]]
#times=epochs_smpl.times
#[avgP1Scrs_ENpr, avgP1Scrs_stat_ENpr]=main_read_gen_stat(path, cond_block, cond_time, cond_filter, times)
