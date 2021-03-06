#!/usr/bin/env bash
#SBATCH -p localLimited
#SBATCH -A ecortex
#SBATCH --mem=10G

export HOME=`getent passwd $USER | cut -d':' -f6`
export PYTHONUNBUFFERED=1
echo Running on $HOSTNAME

source /usr/local/anaconda3/etc/profile.d/conda.sh
conda activate /home/mazlfghr/.conda/envs/DeepLearningEEG

# selected_subj_P1=( 1 2 3 4 5 7 8 9 10 12 15 16 42 43 44 45 46 47 48 51 52 53 \
#                    55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 71 72 73 74)
#done subjects =(2 3 4 15 42 43 48 51 58 59 60 63 64 66 67 69)
selected_subj_P1=( 1 5 7 8 9 10 12 16 44 45 46 47 52 53 \
                   55 56 57 61 62 65 68 71 72 73 74)
echo "Random - pattern 1 - Later Blocks"

for i in "${selected_subj_P1[@]}"
do
echo $i
sbj_num=$i
fn_str="rand_avgP1_scores_timeGen_laterBlocks_noneFilter_PrePost_decodremoveevoked_bslineFalse_3k_Trgt_Loc_prev_$sbj_num"
full_fn=/home/mazlfghr/projects/SPLT/results/temp_gen/eCortex/$fn_str

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
     sbatch scripts/eCortex/temp_gen/rand_temp_gen_laterPrePost_none_noBsline_rmvevoked.sh $sbj_num --job-name=subj$sbj_num &
else
     echo "File $sbj_num already exists."
fi


done

wait
