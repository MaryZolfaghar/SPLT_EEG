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
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
#plt.switch_backend('Agg')

from os import scandir

server_bool=0;

#======================================================================================================================== 
def set_params(cond_block, cond_time, SAVE_EPOCH_ROOT):

    n_chan=129
    n_times=113
    
    set_param = mne.read_epochs(SAVE_EPOCH_ROOT + 'epochs_sec_applyBaseline_subj1-afterRejICA-epo.fif', proj=True, preload=True, verbose=None)
    
    ##==============================================================================
    set_param = set_param['pred']['non'].copy()
    
    ##==============================================================================
    if cond_block=='early': #block 3-6
        set_param = set_param['Block<7'].copy()
        set_param = set_param['Block>2'].copy()
    elif cond_block=='later':#block 7-10
        set_param = set_param['Block<11'].copy()
        set_param = set_param['Block>6'].copy()
    ##==============================================================================
    if cond_time=='prestim':
        set_param= set_param.crop(tmin=-0.4, tmax=0.05)
    elif cond_time=='poststim':
        set_param= set_param.crop(tmin=0.05, tmax=0.45)
    
    ##==============================================================================        
    set_param = set_param.pick_types(eeg=True)    

    n_chan  = set_param._data.shape[1]
    n_times = set_param._data.shape[2]
    
    return set_param, n_chan, n_times

#========================================================================================================================    
def set_fonts():
    from matplotlib.font_manager import FontProperties

    font = FontProperties()
    font.set_family('serif')
    font.set_name('Calibri')
#    font.set_style('italic')
    return font

#======================================================================================================================== 
def plot_scores_dcding(avg_X, times, fn_str):
    plt.close('all')

    font=set_fonts();
    
    plt.close('all')
    plt.subplot(111)
    plt.tight_layout()
    plt.plot(times, avg_X, label='score')
    plt.axhline(.5, color='k', linestyle='--', label='chance')
    plt.ylim([0.43,0.56])
    plt.axvline(.0, color='k', linestyle='-')

    plt.tight_layout()

    plt.xlabel('Times', fontproperties=font, fontsize=12, fontweight='bold')
    plt.ylabel('AUC', fontproperties=font,  labelpad=16, fontsize=12, fontweight='bold')
    plt.title('P%s scores' %(cond_time[1:]), fontproperties=font, fontweight='bold', fontsize=16, loc='left')
    plt.legend(fontsize=11)    
    plt.tight_layout()

    plt.savefig(fn_str)
    

#========================================================================================================================    
def do_plot_permttest_dcding(X, avg_X, times, fn_str):
    t_obs, clusters, clusters_pv, H0 = mne.stats.spatio_temporal_cluster_1samp_test(X, tail=0, threshold=50)
#    good_cluster_inds = np.where(clusters_pv < p_accept)[0]
    font=set_fonts();
    
    plt.close('all')
    plt.subplot(111)
    plt.tight_layout()
    plt.plot(times, avg_X, label='score')
    plt.axhline(.5, color='k', linestyle='--', label='chance')
    plt.ylim([0.43,0.56])
    plt.axvline(.0, color='k', linestyle='-')

    plt.tight_layout()
        
    for i_clu, clu_idx in enumerate(clusters):
        clu_idx=clu_idx[0]
        print(clu_idx)
        # unpack cluster information, get unique indices
        if clusters_pv[i_clu] <= 0.05:
            h = plt.axvspan(times[clu_idx[0]], times[clu_idx[-1] - 1],
                            color='r', alpha=0.3)
            plt.legend((h, ), ('cluster p-value < 0.05', ))
        else:
            plt.axvspan(times[clu_idx[0]], times[clu_idx[-1] - 1], color=(0.3, 0.3, 0.3),
                        alpha=0.3)
    plt.tight_layout()
    plt.xlabel('Times', fontproperties=font, fontsize=12, fontweight='bold')
    plt.ylabel('AUC', fontproperties=font,  labelpad=16, fontsize=12, fontweight='bold')
#    plt.title('Decoding Scores \n \n %s' %(cond_time), fontproperties=font, fontweight='bold', fontsize=16)
    plt.title('P%s scores - perm ttest' %(cond_time[1:]), fontproperties=font, fontweight='bold', fontsize=16, loc='left')
    plt.legend(fontsize=11)
    
    plt.tight_layout()
    
    plt.savefig(fn_str)
    
#======================================================================================================================== 

if server_bool == 0:
    sys.path.insert(0, "/Users/Maryam/Documents/MATLAB/PsychoExp/FinalExp/Analysis/pkg")
    SAVE_EPOCH_ROOT = '/Users/Maryam/Documents/MATLAB/PsychoExp/FinalExp/Analysis/data/version5_2/epochs/aft_ICA_rej/'
#    SAVE_datasets_ROOT='/Users/Maryam/Documents/MATLAB/PsychoExp/FinalExp/Analysis/data/version5_2/deepLearning/EEGNet/datasets/results_filter_400postStim/'
    SAVE_RESULT_ROOT = '/Users/Maryam/Documents/MATLAB/PsychoExp/FinalExp/Analysis/data/version5_2/decoding/decoding_designedFilter/results/'
    SAVE_FIG_ROOT ='/Users/Maryam/Documents/MATLAB/PsychoExp/FinalExp/Analysis/data/version5_2/decoding/decoding_designedFilter/figs/'
else:
    sys.path.insert(0, "/pl/active/ccnlab/users/zolfaghar/my_pkg")
    sys.path.insert(0, "/pl/active/ccnlab/users/zolfaghar/EEGexp/lib/python2.7/site-packages/my_pkg")
    SAVE_EPOCH_ROOT = '/pl/active/ccnlab/users/zolfaghar/data/SPLT5.2/epochs/'
    MAIN_ROOT = '/pl/active/ccnlab/users/zolfaghar/finalCodes_version5.2/deepLearning/EEGNet/'
#    SAVE_datasets_ROOT = MAIN_ROOT+'datasets/results_filter_400postStim/'
    SAVE_RESULT_ROOT = '/pl/active/ccnlab/users/zolfaghar/finalCodes_version5.2/decoding/decoding_designedFilter/results/'

    subj_num      = sys.argv[1]
    cond_filter = sys.argv[2]
    cond_time     = sys.argv[3]

#========================================================================================================================



def main_read_gen_stat(path, cond_block, cond_time, cond_filter, times):
    
    dir_entries = scandir(path)
    
    Grp1_ptrn1_score=[]
    Grp2_ptrn1_score=[]
    Grp3_ptrn1_score=[]
    Grp4_ptrn1_score=[]
    Grp1_ptrn2_score=[]
    Grp2_ptrn2_score=[]
    Grp3_ptrn2_score=[]
    Grp4_ptrn2_score=[]
    
    Grp1_ptrn1_subj=[]
    Grp2_ptrn1_subj=[]
    Grp3_ptrn1_subj=[]
    Grp4_ptrn1_subj=[]
    Grp1_ptrn2_subj=[]
    Grp2_ptrn2_subj=[]
    Grp3_ptrn2_subj=[]
    Grp4_ptrn2_subj=[]

    G1P1=0; G2P1=0; G3P1=0; G4P1=0;
    G1P2=0; G2P2=0; G3P2=0; G4P2=0;

    for f in dir_entries:
#        print(f.name)
        fname=str(f.name)
        group_name=fname.split("_")[1]+'_'+fname.split("_")[2]
        subj_num=fname.split("_")[-1][0:-4]
    #    print(group_name)
        scores=np.load(f)
        
        if group_name=='Grp1_ptrn1':
            Grp1_ptrn1_score.append(scores)
            Grp1_ptrn1_subj.append(subj_num)
            G1P1+=1
            
        if group_name=='Grp2_ptrn1':
            Grp2_ptrn1_score.append(scores)
            Grp2_ptrn1_subj.append(subj_num)
            G2P1+=1
            
        if group_name=='Grp3_ptrn1':
            Grp3_ptrn1_score.append(scores)
            Grp3_ptrn1_subj.append(subj_num)
            G3P1+=1
            
        if group_name=='Grp4_ptrn1':
            Grp4_ptrn1_score.append(scores)
            Grp4_ptrn1_subj.append(subj_num)
            G4P1+=1
            
        if group_name=='Grp1_ptrn2':
            Grp1_ptrn2_score.append(scores)
            Grp1_ptrn2_subj.append(subj_num)
            G1P2+=1
            
        if group_name=='Grp2_ptrn2':
            Grp2_ptrn2_score.append(scores)
            Grp2_ptrn2_subj.append(subj_num)
            G2P2+=1
            
        if group_name=='Grp3_ptrn2':
            Grp3_ptrn2_score.append(scores)
            Grp3_ptrn2_subj.append(subj_num)
            G3P2+=1
            
        if group_name=='Grp4_ptrn2':
            Grp4_ptrn2_score.append(scores)
            Grp4_ptrn2_subj.append(subj_num)
            G4P2+=1
    
    Grp1_ptrn1_score=np.asarray(Grp1_ptrn1_score)
    Grp2_ptrn1_score=np.asarray(Grp2_ptrn1_score)
    Grp3_ptrn1_score=np.asarray(Grp3_ptrn1_score)
    Grp4_ptrn1_score=np.asarray(Grp4_ptrn1_score)
    
    Grp1_ptrn2_score=np.asarray(Grp1_ptrn2_score)
    Grp2_ptrn2_score=np.asarray(Grp2_ptrn2_score)
    Grp3_ptrn2_score=np.asarray(Grp3_ptrn2_score)
    Grp4_ptrn2_score=np.asarray(Grp4_ptrn2_score)
    
    avg_Grp1_ptrn1_score=np.mean(Grp1_ptrn1_score, axis=0)
    avg_Grp2_ptrn1_score=np.mean(Grp2_ptrn1_score, axis=0)
    avg_Grp3_ptrn1_score=np.mean(Grp3_ptrn1_score, axis=0)
    avg_Grp4_ptrn1_score=np.mean(Grp4_ptrn1_score, axis=0)
    
    avg_Grp1_ptrn2_score=np.mean(Grp1_ptrn2_score, axis=0)
    avg_Grp2_ptrn2_score=np.mean(Grp2_ptrn2_score, axis=0)
    avg_Grp3_ptrn2_score=np.mean(Grp3_ptrn2_score, axis=0)
    avg_Grp4_ptrn2_score=np.mean(Grp4_ptrn2_score, axis=0)
    
    print('In pattern 1, 4 groups:')
    print([G1P1, G2P1, G3P1, G4P1])
    print('In pattern 2, 4 groups:')
    print([G1P2, G2P2, G3P2, G4P2])
    
    
    
    
    
     #---------------------- ---------------------- ---------------------- ---------
    # PLOT ---------------------- ---------------------- --------
    #------------
    # Each group separately
    #------------
    # pattern 1
    #------------
    scores=avg_Grp1_ptrn1_score
    fn_str=SAVE_FIG_ROOT + 'G1P1_dcding_%s_%s_%s.pdf' %(cond_block, cond_time, cond_filter)
    plot_scores_dcding(scores, times, fn_str)
    
    scores=avg_Grp2_ptrn1_score
    fn_str=SAVE_FIG_ROOT + 'G2P1_dcding_%s_%s_%s.pdf' %(cond_block, cond_time, cond_filter)
    plot_scores_dcding(scores, times, fn_str)
    
    scores=avg_Grp3_ptrn1_score
    fn_str=SAVE_FIG_ROOT + 'G3P1_dcding_%s_%s_%s.pdf' %(cond_block, cond_time, cond_filter)
    plot_scores_dcding(scores, times, fn_str)
    
    scores=avg_Grp4_ptrn1_score
    fn_str=SAVE_FIG_ROOT + 'G4P1_dcding_%s_%s_%s.pdf' %(cond_block, cond_time, cond_filter)
    plot_scores_dcding(scores, times, fn_str)

    #------------    
    # pattern 2
    #------------
    scores=avg_Grp1_ptrn2_score
    fn_str=SAVE_FIG_ROOT + 'G1P2_dcding_%s_%s_%s.pdf' %(cond_block, cond_time, cond_filter)
    plot_scores_dcding(scores, times, fn_str)
    
    scores=avg_Grp2_ptrn2_score
    fn_str=SAVE_FIG_ROOT + 'G2P2_dcding_%s_%s_%s.pdf' %(cond_block, cond_time, cond_filter)
    plot_scores_dcding(scores, times, fn_str)
    
    scores=avg_Grp3_ptrn2_score
    fn_str=SAVE_FIG_ROOT + 'G3P2_dcding_%s_%s_%s.pdf' %(cond_block, cond_time, cond_filter)
    plot_scores_dcding(scores, times, fn_str)
    
    scores=avg_Grp4_ptrn2_score
    fn_str=SAVE_FIG_ROOT + 'G4P2_dcding_%s_%s_%s.pdf' %(cond_block, cond_time, cond_filter)
    plot_scores_dcding(scores, times, fn_str)
    
    
    #---------------------- ---------------------- ---------------------- ---------
    # average over all groups---------------------- ---------------------- --------
    #------------
    # pattern 1
    #------------
    d=(Grp4_ptrn1_score).shape;
    print(d)
    P1Scrs=np.zeros([4,d[0],d[1]])
    
    P1Scrs[0,:,:]=np.asarray(Grp1_ptrn1_score[0:-1]) # Grp4 has one row feawer than others, so have to do [0:-1] to be consistent for all of them 
    P1Scrs[1,:,:]=np.asarray(Grp2_ptrn1_score[0:-1])
    P1Scrs[2,:,:]=np.asarray(Grp3_ptrn1_score[0:-1])
    P1Scrs[3,:,:]=np.asarray(Grp4_ptrn1_score)
    avgP1Scrs_stat=np.mean(P1Scrs, axis=0)
    avgP1Scrs=avgP1Scrs_stat.mean(axis=0)
    # PLOT -------------------------
    # average over pattern 1
    scores=avgP1Scrs
    fn_str=SAVE_FIG_ROOT + 'avgP1_dcding_%s_%s_%s.pdf' %(cond_block, cond_time, cond_filter)
    plot_scores_dcding(scores, times, fn_str)
    
    
    #------------
    # pattern 2
    #------------
    d=(Grp4_ptrn2_score).shape;
    print(d)
    P2Scrs=np.zeros([4,d[0],d[1]])
    
    P2Scrs[0,:,:]=np.asarray(Grp1_ptrn2_score) 
    P2Scrs[1,:,:]=np.asarray(Grp2_ptrn2_score)
    P2Scrs[2,:,:]=np.asarray(Grp3_ptrn2_score)
    P2Scrs[3,:,:]=np.asarray(Grp4_ptrn2_score)
    avgP2Scrs_stat=np.mean(P2Scrs, axis=0)
    avgP2Scrs=avgP2Scrs_stat.mean(axis=0)
    # PLOT -------------------------
    # average over pattern 2
    scores=avgP2Scrs
    fn_str=SAVE_FIG_ROOT + 'avgP2_dcding_%s_%s_%s.pdf' %(cond_block, cond_time, cond_filter)
    plot_scores_dcding(scores, times, fn_str)
    
    
    
    # STAT ---------------------- ---------------------- ----------------------
    # set cluster threshold
    #threshold = 50.0  # very high, but the test is quite sensitive on this data
    # set family-wise p-value
    #p_accept = 0.01
    #t_obs1, clusters1, clusters_pv1, H01 = mne.stats.permutation_cluster_1samp_test(X, tail=0) Check both functions the result was almost same for everything, the H0 was only different
    
    #------------
    # pattern 1
    #------------

    fn_str=SAVE_FIG_ROOT + 'G1P1_stat_dcding_%s_%s_%s.pdf' %(cond_block, cond_time, cond_filter)
    X=Grp1_ptrn1_score
    X=X[:,:,np.newaxis]
    avg_X=np.mean(X, axis=0)
    do_plot_permttest_dcding(X, avg_X, times, fn_str)
    
    fn_str=SAVE_FIG_ROOT + 'G2P1_stat_dcding_%s_%s_%s.pdf' %(cond_block, cond_time, cond_filter)
    X=Grp2_ptrn1_score
    X=X[:,:,np.newaxis]
    avg_X=np.mean(X, axis=0)
    do_plot_permttest_dcding(X, avg_X, times, fn_str)
   
    fn_str=SAVE_FIG_ROOT + 'G3P1_stat_dcding_%s_%s_%s.pdf' %(cond_block, cond_time, cond_filter)
    X=Grp3_ptrn1_score
    X=X[:,:,np.newaxis]
    avg_X=np.mean(X, axis=0)
    do_plot_permttest_dcding(X, avg_X, times, fn_str)
   
    
    fn_str=SAVE_FIG_ROOT + 'G4P1_stat_dcding_%s_%s_%s.pdf' %(cond_block, cond_time, cond_filter)
    X=Grp4_ptrn1_score
    X=X[:,:,np.newaxis]
    avg_X=np.mean(X, axis=0)
    do_plot_permttest_dcding(X, avg_X, times, fn_str)
    
    
    
    # -- Do stat over average of all four groups    
    fn_str=SAVE_FIG_ROOT + 'avgP1_stat_dcding_%s_%s_%s.pdf' %(cond_block, cond_time, cond_filter)
    X=avgP1Scrs_stat
    X=X[:,:,np.newaxis]
    avg_X=np.mean(avgP1Scrs_stat, axis=0)
    do_plot_permttest_dcding(X, avg_X, times, fn_str)
    
 
    
    #------------
    # pattern 2
    #------------

    fn_str=SAVE_FIG_ROOT + 'G1P2_stat_dcding_%s_%s_%s.pdf' %(cond_block, cond_time, cond_filter)
    X=Grp1_ptrn2_score
    X=X[:,:,np.newaxis]
    avg_X=np.mean(X, axis=0)
    do_plot_permttest_dcding(X, avg_X, times, fn_str)
    
    fn_str=SAVE_FIG_ROOT + 'G2P2_stat_dcding_%s_%s_%s.pdf' %(cond_block, cond_time, cond_filter)
    X=Grp2_ptrn2_score
    X=X[:,:,np.newaxis]
    avg_X=np.mean(X, axis=0)
    do_plot_permttest_dcding(X, avg_X, times, fn_str)
   
    fn_str=SAVE_FIG_ROOT + 'G3P2_stat_dcding_%s_%s_%s.pdf' %(cond_block, cond_time, cond_filter)
    X=Grp3_ptrn2_score
    X=X[:,:,np.newaxis]
    avg_X=np.mean(X, axis=0)
    do_plot_permttest_dcding(X, avg_X, times, fn_str)
   
    
    fn_str=SAVE_FIG_ROOT + 'G4P2_stat_dcding_%s_%s_%s.pdf' %(cond_block, cond_time, cond_filter)
    X=Grp4_ptrn2_score
    X=X[:,:,np.newaxis]
    avg_X=np.mean(X, axis=0)
    do_plot_permttest_dcding(X, avg_X, times, fn_str)
    
    
    
    # -- Do stat over average of all four groups
    fn_str=SAVE_FIG_ROOT + 'avgP2_stat_dcding_%s_%s_%s.pdf' %(cond_block, cond_time, cond_filter)
    X=avgP2Scrs_stat
    X=X[:,:,np.newaxis]
    avg_X=np.mean(avgP2Scrs_stat, axis=0)
    do_plot_permttest_dcding(X, avg_X, times, fn_str)

    

    return avgP1Scrs, avgP1Scrs_stat



#========================================================================================================================


#========================================================================================================================
#[epochs_smpl, n_chan, n_times]=set_params(cond_block, SAVE_EPOCH_ROOT)
#extent_time=epochs_smpl.times[[0, -1, 0, -1]]


##========================================================================================================================

####=========
cond_filter='none'
cond_block='early'
cond_time='prestim'
path=SAVE_RESULT_ROOT+ 'results_filter_400%s' %(cond_time)+ '/' + '%s' %(cond_filter) + '/'
[epochs_smpl, n_chan, n_times]=set_params(cond_block, cond_time, SAVE_EPOCH_ROOT)
extent_time=epochs_smpl.times[[0, -1, 0, -1]]
times=epochs_smpl.times
[avgP1Scrs_ENpr, avgP1Scrs_stat_ENpr]=main_read_gen_stat(path, cond_block, cond_time, cond_filter, times)

#
cond_filter='none'
cond_block='early'
cond_time='poststim'
path=SAVE_RESULT_ROOT+ 'results_filter_400%s' %(cond_time)+ '/' + '%s' %(cond_filter) + '/'
[epochs_smpl, n_chan, n_times]=set_params(cond_block, cond_time, SAVE_EPOCH_ROOT)
extent_time=epochs_smpl.times[[0, -1, 0, -1]]
times=epochs_smpl.times
[avgP1Scrs_ENpo, avgP1Scrs_stat_ENpo]=main_read_gen_stat(path, cond_block, cond_time, cond_filter, times)

##=========
cond_filter='none'
cond_block='later'
cond_time='prestim'
path=SAVE_RESULT_ROOT+ 'results_filter_400%s' %(cond_time)+ '/' + '%s' %(cond_filter) + '/'
[epochs_smpl, n_chan, n_times]=set_params(cond_block, cond_time, SAVE_EPOCH_ROOT)
extent_time=epochs_smpl.times[[0, -1, 0, -1]]
times=epochs_smpl.times
[avgP1Scrs_LNpr, avgP1Scrs_stat_LNpr]=main_read_gen_stat(path, cond_block, cond_time, cond_filter, times)


cond_filter='none'
cond_block='later'
cond_time='poststim'
path=SAVE_RESULT_ROOT+ 'results_filter_400%s' %(cond_time)+ '/' + '%s' %(cond_filter) + '/'
[epochs_smpl, n_chan, n_times]=set_params(cond_block, cond_time, SAVE_EPOCH_ROOT)
extent_time=epochs_smpl.times[[0, -1, 0, -1]]
times=epochs_smpl.times
[avgP1Scrs_LNpo, avgP1Scrs_stat_LNpo]=main_read_gen_stat(path, cond_block, cond_time, cond_filter, times)



##=========
cond_filter='non_symm'
cond_block='early'
cond_time='prestim'
path=SAVE_RESULT_ROOT+ 'results_filter_400%s' %(cond_time)+ '/' + '%s' %(cond_filter) + '/'
[epochs_smpl, n_chan, n_times]=set_params(cond_block, cond_time, SAVE_EPOCH_ROOT)
extent_time=epochs_smpl.times[[0, -1, 0, -1]]
times=epochs_smpl.times
[avgP1Scrs_LNpo, avgP1Scrs_stat_LNpo]=main_read_gen_stat(path, cond_block, cond_time, cond_filter, times)


cond_filter='non_symm'
cond_block='early'
cond_time='poststim'
path=SAVE_RESULT_ROOT+ 'results_filter_400%s' %(cond_time)+ '/' + '%s' %(cond_filter) + '/'
[epochs_smpl, n_chan, n_times]=set_params(cond_block, cond_time, SAVE_EPOCH_ROOT)
extent_time=epochs_smpl.times[[0, -1, 0, -1]]
times=epochs_smpl.times
[avgP1Scrs_LNpo, avgP1Scrs_stat_LNpo]=main_read_gen_stat(path, cond_block, cond_time, cond_filter, times)

##=========
cond_filter='non_symm'
cond_block='later'
cond_time='prestim'
path=SAVE_RESULT_ROOT+ 'results_filter_400%s' %(cond_time)+ '/' + '%s' %(cond_filter) + '/'
[epochs_smpl, n_chan, n_times]=set_params(cond_block, cond_time, SAVE_EPOCH_ROOT)
extent_time=epochs_smpl.times[[0, -1, 0, -1]]
times=epochs_smpl.times
[avgP1Scrs_LNpo, avgP1Scrs_stat_LNpo]=main_read_gen_stat(path, cond_block, cond_time, cond_filter, times)


cond_filter='non_symm'
cond_block='later'
cond_time='poststim'
path=SAVE_RESULT_ROOT+ 'results_filter_400%s' %(cond_time)+ '/' + '%s' %(cond_filter) + '/'
[epochs_smpl, n_chan, n_times]=set_params(cond_block, cond_time, SAVE_EPOCH_ROOT)
extent_time=epochs_smpl.times[[0, -1, 0, -1]]
times=epochs_smpl.times
[avgP1Scrs_LNpo, avgP1Scrs_stat_LNpo]=main_read_gen_stat(path, cond_block, cond_time, cond_filter, times)



                                                 
    
    