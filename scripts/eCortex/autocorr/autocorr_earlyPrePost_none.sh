#!/usr/bin/env bash
#SBATCH -p localLimited
#SBATCH -A ecortex
#SBATCH --mem=10G

export HOME=`getent passwd $USER | cut -d':' -f6`
export PYTHONUNBUFFERED=1
echo Running on $HOSTNAME

source /usr/local/anaconda3/etc/profile.d/conda.sh
conda activate /home/mazlfghr/.conda/envs/DeepLearningEEG

echo "Process $1 starts"


python autocorr.py \
--SAVE_EPOCH_ROOT ../data/version5.2/preprocessed/epochs/aft_ICA_rej/ \
--SAVE_RESULT_ROOT ../results/autocorr/eCortex/ \
--subj_num $1 \
--cond_filter none \
--cond_block early \
--applyBaseline_bool \
--mtdt_feat Trgt_Loc_main \ 
