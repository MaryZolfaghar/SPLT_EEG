#!/bin/bash

source /Users/Maryam/anaconda3/etc/profile.d/conda.sh
conda activate DeepLearningEEG
cd ../../../decoding/

python permtest.py \
--SAVE_EPOCH_ROOT ../data/preprocessed/epochs/ \
--SAVE_RESULT_ROOT ../results/decoding/permtest/ \
--cond_filter none \
--cond_block later \
--cond_time prestim \ 
