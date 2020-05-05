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

# gpus=$(echo $CUDA_VISIBLE_DEVICES | tr "," "\n")
# for gpu in $gpus
# do
# echo "Setting fan for" $gpu "to full"
# nvidia_fancontrol full $gpu
# done

PYTHONPATH=/pl/active/ccnlab/users/zolfaghar/finalCodes_version5.2/github/SPLT_EEG/


echo Running on $HOSTNAME
for i in "${selected_subj_P1[@]}"
do
echo $i
sbj_num=$i
fn_str="rand_avgP1_scores_timeGen_earlyBlocks_noneFilter_PrePost_decodremoveevoked_bslineFalse_3k_Trgt_Loc_prev_$sbj_num"
echo $fn_str
full_fn=/home/mazlfghr/projects/SPLT/results/temp_gen/eCortex/$fn_str
echo $full_fn

if [ ! -f $full_fn ]
then
     echo "Process $sbj_num starts"
     #"""""""""""""""""""""""""
     #"""""""""" Rand """""""""
     #"""""""""""""""""""""""""
     #1. - no baseline - #
     # - removed evoked - #
     # - 3k - #
     # - 100 iterations - #
     sbatch scripts/blanca/temp_gen/temp_gen_earlyPrePost_none_noBsline_rmvevoked.sh &
     sbatch scripts/blanca/temp_gen/temp_gen_laterPrePost_none_noBsline_rmvevoked.sh &
else
     echo "----------------------------"
     echo "File $sbj_num already exists."
     echo "----------------------------"
fi


done

wait
