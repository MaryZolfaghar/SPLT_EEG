#!/bin/bash
#SBATCH --time=120:00:00
#SBATCH -c 16
#SBATCH --qos=blanca-ccn
#SBATCH --mem=10G

export HOME=`getent passwd $USER | cut -d':' -f6`
echo $HOME
export PYTHONUNBUFFERED=1

echo Running on $HOSTNAME

source /pl/active/ccnlab/conda/etc/profile.d/conda.sh
conda activate /pl/active/ccnlab/users/zolfaghar/conda/SPLTEEG
PYTHONPATH=/pl/active/ccnlab/users/zolfaghar/finalCodes_version5.2/github/SPLT_EEG/

start time
date +"%H:%M:%S"

echo "Process $1 starts"

python autocorr.py \
--SAVE_EPOCH_ROOT ../../../data/SPLT5.2/epochs/aft_ICA_rej/ \
--SAVE_RESULT_ROOT ../results/autocorr/blanca/ \
--subj_num $1 \
--cond_filter none \
--cond_block later \
--cond_decoding removeevoked \
