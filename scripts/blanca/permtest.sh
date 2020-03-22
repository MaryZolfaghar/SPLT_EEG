#!/bin/bash
#SBATCH --time=72:00:00
#SBATCH --mem=60G
#SBATCH -c 16
#SBATCH --qos=blanca-ccn

source  /pl/active/ccnlab/users/zolfaghar/EEGexp
conda activate EEGexp

cd ../../decoding/

python permtest.py \
--SAVE_EPOCH_ROOT ../data/preprocessed/epochs/ \
--SAVE_RESULT_ROOT ../results/decoding/permtest/ \
--cond_filter none \
--cond_block later \
--cond_time prestim \ 
