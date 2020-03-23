#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 16 00:56:08 2019

@author: Maryam
"""

server_bool = 1;
first_time_run = 0

import sys
import time
import datetime
from numpy.random import randn
import scipy.io
import numpy as np
from scipy import stats

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import (StandardScaler, LabelEncoder)
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

import mne
from mne.decoding import (SlidingEstimator, GeneralizingEstimator, Scaler,
                          cross_val_multiscore, LinearModel, get_coef,
                          Vectorizer, CSP)

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.switch_backend('Agg')

#===============================================================================
def apply_nonSymm_filter(epoch_data, frequencies):
    #filter epoch data
    flip_signal = np.flip(epoch_data._data.copy(), axis=-1)
    flip_signal_filt = mne.filter.filter_data(
                            data=flip_signal,
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

#========================================================================================================================
if server_bool == 0:
sys.path.insert(0, "/Users/Maryam/Documents/MATLAB/PsychoExp/FinalExp/Analysis/pkg")
SAVE_EPOCH_ROOT = '/Users/Maryam/Documents/MATLAB/PsychoExp/FinalExp/Analysis/data/version5_2/epochs/'
SAVE_datasets_ROOT='/Users/Maryam/Documents/MATLAB/PsychoExp/FinalExp/Analysis/data/version5_2/deepLearning/EEGNet/datasets/results_filter_400postStim/'
else:
sys.path.insert(0, "/pl/active/ccnlab/users/zolfaghar/my_pkg")
sys.path.insert(0, "/pl/active/ccnlab/users/zolfaghar/EEGexp/lib/python2.7/site-packages/my_pkg")
SAVE_EPOCH_ROOT = '/pl/active/ccnlab/users/zolfaghar/data/SPLT5.2/epochs/aft_ICA_rej/'
MAIN_ROOT = '/pl/active/ccnlab/users/zolfaghar/finalCodes_version5.2/deepLearning/EEGNet/'
#    SAVE_datasets_ROOT = MAIN_ROOT+'datasets/results_filter_400postStim/'
SAVE_RESULT_ROOT = '/pl/active/ccnlab/users/zolfaghar/finalCodes_version5.2/decoding/decoding_designedFilter/datasets/'

subj_num      = sys.argv[1]
cond_decoding = sys.argv[2]
cond_time     = sys.argv[3]
rand_perm     = sys.argv[4]
cond_block    = sys.argv[5]

#========================================================================================================================
rand_perm=0;

SAVE_RESULT_ROOT=SAVE_RESULT_ROOT + '/' + cond_block + '/' + cond_decoding + '/'
#========================================================================================================================
#========================================================================================================================
def generate_rand(n_iterations, X, Y):
    null_scores=[]
    for nitr in range(n_iterations):
        true_Y=Y.copy();
        indx=np.random.permutation(true_Y.shape[0]);
        shuffled_Y = true_Y.copy()[indx];
        shuffled_Y = le.fit_transform(shuffled_Y.copy());

        time_decod_clf = SlidingEstimator(selected_clf, n_jobs=1, scoring='roc_auc')
        scores_clf = mne.decoding.cross_val_multiscore(time_decod_clf, X_clf, y_clf, cv=5, n_jobs=1)
        scores_clf = np.mean(scores_clf, axis=0) # Mean scores across cross-validation splits
        null_scores.append(scores_clf)

    return null_scores

#========================================================================================================================

"""
 ==============================================================================
 ==============================================================================
"""
selected_subj = [ 1,  2,  3,  4,  5,  7,  8,  9, 10, 12, 15, 16, 17, 18, 19, 20, 21,
       22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38,
       39, 42, 43, 44, 45, 46, 47, 48, 51, 52, 53, 55, 56, 57, 58, 59,
       60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74]
#remove subj #49 ,error:   tag.data = _read_matrix(fid, tag, shape, rlims, matrix_coding)
#===============================================================================
def load_prepare_epochs(filename_epoch, cond_decoding, cond_block):


    normalize_bool_type1=True #normal normalization
    normalize_bool_type2=False #normalization based on the LSTM paper


    ##==========================================================================
    print('strat of epoch reading=========================================')
    print(filename_epoch)
    print(datetime.datetime.now().time())

    ##==========================================================================
    epochs_orig = mne.read_epochs(filename_epoch, proj=True, preload=True,
                                  verbose=None)
    epochs = epochs_orig.copy()
    subset = epochs['pred']['non'].copy()
    subset = subset.pick_types(eeg=True)


    if (cond_decoding=='removeevoked'):
        # REMOVE EVOKED RESP.
        subset.subtract_evoked()    # remove evoked response
    elif (cond_decoding=='resampled'):
        # RESAMPLE
        subset = subset.resample(50, npad='auto')
    else:
        subset = subset.copy()
    ##==============================================================================
    if subset['Block==7'].metadata.Ptrn_Type.values.shape[0]>0:
       main_ptrn = subset['Block==7'].metadata.Ptrn_Type.values[0]
    else:
       main_ptrn = subset['Block==8'].metadata.Ptrn_Type.values[0]
    ##==============================================================================
    if cond_block=='early': #block 3-6
        subset = subset['Block<7'].copy()
        subset = subset['Block>2'].copy()
    elif cond_block=='later':#block 7-10
        subset = subset['Block<11'].copy()
        subset = subset['Block>6'].copy()

    ##==============================================================================
    if (cond_time=='prestim'):
        subset= subset.crop(tmin=-0.4, tmax=0.05)
    if (cond_time=='poststim'):
        subset= subset.crop(tmin=0.05, tmax=0.45)

    ##==============================================================================
    # Group data based on the previous truil
    Grp1 = subset['Trgt_Loc_prev==1'].copy()
    Grp2 = subset['Trgt_Loc_prev==2'].copy()
    Grp3 = subset['Trgt_Loc_prev==3'].copy()
    Grp4 = subset['Trgt_Loc_prev==4'].copy()

    if main_ptrn==1:
        Grp1 = Grp1['Trgt_Loc_main!=4'].copy()
        Grp2 = Grp2['Trgt_Loc_main!=1'].copy()
        Grp3 = Grp3['Trgt_Loc_main!=2'].copy()
        Grp4 = Grp4['Trgt_Loc_main!=3'].copy()



    ##==============================================================================
    frequencies = np.arange(3, 13, 2)

    if cond_decoding=='non_symm':
        Grp1 = apply_nonSymm_filter(Grp1, frequencies)
        Grp2 = apply_nonSymm_filter(Grp2, frequencies)
        Grp3 = apply_nonSymm_filter(Grp3, frequencies)
        Grp4 = apply_nonSymm_filter(Grp4, frequencies)


    ##==============================================================================
    print('the pattern for this subj is :=============================================================================')
    print(main_ptrn)
    print('          ')
    print('=============================================================================')

    ##==============================================================================
    # Normalizing the data for each subject
    if normalize_bool_type1:
        Grp1._data = (Grp1._data - np.mean(Grp1._data)) / np.std(Grp1._data)
        Grp2._data = (Grp2._data - np.mean(Grp2._data)) / np.std(Grp2._data)
        Grp3._data = (Grp3._data - np.mean(Grp3._data)) / np.std(Grp3._data)
        Grp4._data = (Grp4._data - np.mean(Grp4._data)) / np.std(Grp4._data)

    elif normalize_bool_type2:
        Grp1._data = (2 * (Grp1._data - np.min(Grp1._data))) / (np.max(Grp1._data) - np.min(Grp1._data) - 1)
        Grp2._data = (2 * (Grp2._data - np.min(Grp2._data))) / (np.max(Grp2._data) - np.min(Grp2._data) - 1)
        Grp3._data = (2 * (Grp3._data - np.min(Grp3._data))) / (np.max(Grp3._data) - np.min(Grp3._data) - 1)
        Grp4._data = (2 * (Grp4._data - np.min(Grp4._data))) / (np.max(Grp4._data) - np.min(Grp4._data) - 1)


    return Grp1, Grp2, Grp3, Grp4, main_ptrn

##==============================================================================
def apply_decoder(Grp_data, fn_str):

    rand_perm=0;

    n_splits = 3  # how many folds to use for cross-validation
    cv = StratifiedKFold(n_splits=n_splits, shuffle=True)
    le = LabelEncoder()

    clf_SVC  = make_pipeline(
                            StandardScaler(),
                            LinearModel(LinearSVC(random_state=0, max_iter=10000)))

    X=Grp_data.copy()._data
    y=le.fit_transform(Grp_data.copy().metadata.Trgt_Loc_main)

    if rand_perm:
        n_iterations=1000;
        str_clf='clf_SVC'
        null_scores = generate_rand(n_iterations, X, y)
        np.save(SAVE_RESULT_ROOT+'/null_scores_Grp1_ptrn1_%s_subj_%s.npy' %(str_clf, subj_num), null_scores, allow_pickle=True);
    else:
        time_decod_clf = SlidingEstimator(clf_SVC, n_jobs=1, scoring='roc_auc')
        scores_clf = mne.decoding.cross_val_multiscore(time_decod_clf, X, y, cv=cv, n_jobs=1)
        scores_clf = np.mean(scores_clf, axis=0)# Mean scores across cross-validation splits
        np.save(fn_str, scores_clf, allow_pickle=True);

    return scores_clf

#========================================================================================================================
#==========
#Read some params
#==========
#==========
SAVE_RESULT_ROOT=SAVE_RESULT_ROOT + '/' + cond_block + '/' + cond_decoding + '/'
#==========
#Set some params
#==========
num_classes = 2
applyBaseline_bool=1;


#========================================================================================================================
#[epochs_smpl, n_chan, n_times]=set_params(cond_block, cond_time, SAVE_EPOCH_ROOT)
#========================================================================================================================
if (applyBaseline_bool == 0):
     filename_epoch = SAVE_EPOCH_ROOT + 'epochs_sec_subj%s-afterRejICA-epo.fif' %subj_num
else:
     filename_epoch = SAVE_EPOCH_ROOT + 'epochs_sec_applyBaseline_subj%s-afterRejICA-epo.fif' %subj_num

#subj_num=1

#========================================================================================================================
# READ epochs for the subject and PREPARE it for the next step
#========================================================================================================================
[Grp1, Grp2, Grp3, Grp4, main_ptrn]=load_prepare_epochs(filename_epoch, cond_block)

scores_G1=apply_decoder(Grp1)
scores_G2=apply_decoder(Grp2)
scores_G3=apply_decoder(Grp3)
scores_G4=apply_decoder(Grp4)

#========================================================================================================================
# SAVE
#========================================================================================================================
fn_str_sbj='scores_dcding_%sBlocks_%sFilter_Subj_%s' %(cond_block, cond_decoding, subj_num)

np.save(SAVE_RESULT_ROOT + 'G1P%s_' %(main_ptrn) + fn_str_sbj + '.npy', scores_G1, allow_pickle=True)
np.save(SAVE_RESULT_ROOT + 'G2P%s_' %(main_ptrn) + fn_str_sbj + '.npy', scores_G2, allow_pickle=True)
np.save(SAVE_RESULT_ROOT + 'G3P%s_' %(main_ptrn) + fn_str_sbj + '.npy', scores_G3, allow_pickle=True)
np.save(SAVE_RESULT_ROOT + 'G4P%s_' %(main_ptrn) + fn_str_sbj + '.npy', scores_G4, allow_pickle=True)

avg_all_scores= np.zeros([4, scores_G1.shape[0], scores_G1.shape[1]])
avg_all_scores[0,:,:]=scores_G1
avg_all_scores[1,:,:]=scores_G2
avg_all_scores[2,:,:]=scores_G3
avg_all_scores[3,:,:]=scores_G4

avg_all_scores=np.mean(avg_all_scores,axis=0)
np.save(SAVE_RESULT_ROOT + 'avgP%s_' %(main_ptrn) + fn_str_sbj + '.npy', avg_all_scores, allow_pickle=True)



print("#Done==============================================================================#")

print(datetime.datetime.now().time())
