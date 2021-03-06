"""
Combine all RTs for each subjects and each block and each group
"""
import numpy as np
import argparse
import pickle
import datetime

from modules.read_prep_epochs import read_prep_epochs
from utils.calc_block_RTs import calc_block_RTs

def combine_subj_RTs(args, subj_ids):

    tot_num_blocks = 8
    mean_RTs_Subjs = np.zeros([len(subj_ids), 4, tot_num_blocks])
    sem_RTs_Subjs = np.zeros([len(subj_ids), 4, tot_num_blocks])

    for subj_id in range(len(subj_ids)):
        print('**************************************************************')
        print('Subject %s starts --------------------------------' %(subj_id))
        print(str(datetime.datetime.now()))

        args.cond_block = 'early'
        [Grp1e, Grp2e, Grp3e, Grp4e, Grps_dt, Grps_avg, smooth_evk, main_ptrn] = \
        read_prep_epochs(args)

        args.cond_block = 'later'
        [Grp1l, Grp2l, Grp3l, Grp4l, Grps_dt, Grps_avg, smooth_evk, main_ptrn] = \
        read_prep_epochs(args)

        mean_RTs_Subjs[subj_id, 0, :],  sem_RTs_Subjs[subj_id, 0, :], _ = \
         calc_block_RTs(Grp1e, Grp1l)
        mean_RTs_Subjs[subj_id, 1, :],  sem_RTs_Subjs[subj_id, 1, :], _ = \
         calc_block_RTs(Grp2e, Grp2l)
        mean_RTs_Subjs[subj_id, 2, :],  sem_RTs_Subjs[subj_id, 2, :], _ = \
         calc_block_RTs(Grp3e, Grp3l)
        mean_RTs_Subjs[subj_id, 3, :],  sem_RTs_Subjs[subj_id, 3, :], _ = \
         calc_block_RTs(Grp4e, Grp4l)
        print('**************************************************************')
        print('Subject %s Ends ----------------------------------' %(subj_id))
        print(str(datetime.datetime.now()))

    return mean_RTs_Subjs, sem_RTs_Subjs
