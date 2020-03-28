#!/bin/bash
#SBATCH --time=72:00:00
#SBATCH --mem=60G
#SBATCH -c 16
#SBATCH --qos=blanca-ccn

export HOME=`getent passwd $USER | cut -d':' -f6`
export PYTHONUNBUFFERED=1
echo Running on $HOSTNAME

source /pl/active/ccnlab/conda/etc/profile.d/conda.sh
conda activate /pl/active/ccnlab/users/zolfaghar/EEGexp

gpus=$(echo $CUDA_VISIBLE_DEVICES | tr "," "\n")
for gpu in $gpus
do
echo "Setting fan for" $gpu "to full"
nvidia_fancontrol full $gpu
done

#cd ../../../tempGen/

#=============================================================================#

selected_subj=( 1 2 3 4 5 7 8 9 10 12 15 16 17 18 19 20 21 22 23 24 25 26 27 28\
                29 30 31 32 33 34 35 36 37 38 39 42 43 44 45 46 47 48 51 52 53 \
                55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74)


#selected_subj=( 1 2 3 4 5 7 8 9 10 12 15 16 17 18 19 20 21 )

#selected_subj=(1)

start time
#sleep 1h
date +"%H:%M:%S"


for i in "${selected_subj[@]}"
do
echo $i
sbj_num=$i

dcd_fn="avgP1_scores_timeGen_earlyBlock_noneFilter_Subj_$sbj_num.npy"
#full_dcd_fn=../../results/tempGen/
#=============================================================================#

#if [ ! -f $full_dcd_fn ]
#then
echo "Process $dcd_fn starts"

python temp_gen.py \
--SAVE_EPOCH_ROOT ../../../../../../data/SPLT5.2/epochs/ \
--SAVE_RESULT_ROOT ../results/temp_gen/ \
--subj_num $sbj_num \
--applyBaseline_bool \
--cond_filter none \
--cond_block later \
--cond_time prestim
#else
#     echo "File $dcd_fn already exists."
#fi
done

for gpu in $gpus
do
echo "Setting fan for " $gpu "back to auto"
nvidia_fancontrol auto $gpu
done

#wait
