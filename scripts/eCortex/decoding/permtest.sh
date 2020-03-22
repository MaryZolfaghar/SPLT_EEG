#!/usr/bin/env bash
#SBATCH -p local
#SBATCH -A ecortex
#SBATCH --mem=32G
#SBATCH --time=6:00:00
#SBATCH --gres=gpu:1
#SBATCH -c 4

#export HOME=`getent passwd $USER | cut -d':' -f6`
#export PYTHONUNBUFFERED=1
#echo Running on $HOSTNAME


source /usr/local/anaconda3/etc/profile.d/conda.sh
conda activate /home/mazlfghr/.conda/envs/DeepLearningEEG

cd ../../decoding/

python permtest.py \
--SAVE_EPOCH_ROOT ../data/preprocessed/epochs/ \
--SAVE_RESULT_ROOT ../results/decoding/permtest/ \
--cond_filter none \
--cond_block later \
--cond_time prestim \ 
