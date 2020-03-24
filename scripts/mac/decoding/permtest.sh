#!/bin/bash

source /Users/Maryam/anaconda3/etc/profile.d/conda.sh
conda activate DeepLearningEEG
#cd /../../../decoding/


python permtest.py \
--cond_filter none \
--cond_block later \
--cond_time prestim \
--applyBaseline_bool \
--gen_rand_perm \
--gen_decoder_scores \
