#!/bin/bash
#SBATCH --time=120:00:00
#SBATCH -c 16
#SBATCH --qos=blanca-ccn
#SBATCH --mem=20G

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

# selected_subj=(70 71 72 73 74)

selected_subj=( 5 7 12 18 19 21 23 24 27\
                29 30 31 32 33 34 51  \
                55 56 73 74)



start time
date +"%H:%M:%S"

for i in "${selected_subj[@]}"
do
echo $i
sbj_num=$i

echo "Process subject $sbj_num starts"

#1. - no baseline - #
# - removed evoked - #
# - 3k - #
#done (running) sbatch scripts/eCortex/temp_gen/temp_gen_earlyPrePost_none_noBsline_rmvevoked.sh $sbj_num &
#done (running) sbatch scripts/eCortex/temp_gen/temp_gen_laterPrePost_none_noBsline_rmvevoked.sh $sbj_num &

# - no baseline - #
# - removed evoked - #
# - 100k - #
# running sbatch scripts/eCortex/temp_gen/temp_gen_earlyPrePost_none_noBsline_rmvevoked_100k.sh $sbj_num &
# running sbatch scripts/eCortex/temp_gen/temp_gen_laterPrePost_none_noBsline_rmvevoked_100k.sh $sbj_num &


#2. - no baseline - #
# - none - #
# - 3k - #
#done (finished) sbatch scripts/eCortex/temp_gen/temp_gen_earlyPrePost_none_noBsline.sh $sbj_num &
#done (finished) sbatch scripts/eCortex/temp_gen/temp_gen_laterPrePost_none_noBsline.sh $sbj_num &

# - no baseline - #
# - none - #
# - 100k - #
#done (running) sbatch scripts/eCortex/temp_gen/temp_gen_earlyPrePost_none_noBsline_100k.sh $sbj_num &
#done (running) sbatch scripts/eCortex/temp_gen/temp_gen_laterPrePost_none_noBsline_100k.sh $sbj_num &


#3. - with baseline - #
# - removed evoked - #
# - 3k - #
#done (finished) sbatch scripts/eCortex/temp_gen/temp_gen_earlyPrePost_none_rmvevoked.sh $sbj_num &
#done (finished) sbatch scripts/eCortex/temp_gen/temp_gen_laterPrePost_none_rmvevoked.sh $sbj_num &

# - with baseline - #
# - removed evoked - #
# - 100k - #
#not done sbatch scripts/eCortex/temp_gen/temp_gen_earlyPrePost_none_rmvevoked_100k.sh $sbj_num &
#not done sbatch scripts/eCortex/temp_gen/temp_gen_laterPrePost_none_rmvevoked_100k.sh $sbj_num &


#4. - with baseline - #
# - none - #
# - 3k - #
#done (finished) sbatch scripts/eCortex/temp_gen/temp_gen_earlyPrePost_none.sh $sbj_num &
#done (finished) sbatch scripts/eCortex/temp_gen/temp_gen_laterPrePost_none.sh $sbj_num &

# - with baseline - #
# - none - #
# - 100k - #
#not done sbatch scripts/eCortex/temp_gen/temp_gen_earlyPrePost_none_100k.sh $sbj_num &
#not done sbatch scripts/eCortex/temp_gen/temp_gen_laterPrePost_none_100k.sh $sbj_num &


#"""""""""""""""""""""""""
#"""""""""" Rand """""""""
#"""""""""""""""""""""""""
#1. - no baseline - #
# - removed evoked - #
# - 3k - #
# - 100 iterations - #
sbatch scripts/blanca/temp_gen/rand_temp_gen_earlyPrePost_none_noBsline_rmvevoked.sh $sbj_num &
sbatch scripts/blanca/temp_gen/rand_temp_gen_laterPrePost_none_noBsline_rmvevoked.sh $sbj_num &

# - no baseline - #
# - removed evoked - #
# - 100k - #
#sbatch scripts/eCortex/temp_gen/rand_temp_gen_earlyPrePost_none_noBsline_rmvevoked_100k.sh $sbj_num &
#sbatch scripts/eCortex/temp_gen/rand_temp_gen_laterPrePost_none_noBsline_rmvevoked_100k.sh $sbj_num &


#2. - no baseline - #
# - none - #
# - 3k - #
#sbatch scripts/eCortex/temp_gen/rand_temp_gen_earlyPrePost_none_noBsline.sh $sbj_num &
#sbatch scripts/eCortex/temp_gen/rand_temp_gen_laterPrePost_none_noBsline.sh $sbj_num &

# - no baseline - #
# - none - #
# - 100k - #
#sbatch scripts/eCortex/temp_gen/rand_temp_gen_earlyPrePost_none_noBsline_100k.sh $sbj_num &
#sbatch scripts/eCortex/temp_gen/rand_temp_gen_laterPrePost_none_noBsline_100k.sh $sbj_num &


#3. - with baseline - #
# - removed evoked - #
# - 3k - #
#sbatch scripts/eCortex/temp_gen/rand_temp_gen_earlyPrePost_none_rmvevoked.sh $sbj_num &
#sbatch scripts/eCortex/temp_gen/rand_temp_gen_laterPrePost_none_rmvevoked.sh $sbj_num &

# - with baseline - #
# - removed evoked - #
# - 100k - #
#sbatch scripts/eCortex/temp_gen/rand_temp_gen_earlyPrePost_none_rmvevoked_100k.sh $sbj_num &
#sbatch scripts/eCortex/temp_gen/rand_temp_gen_laterPrePost_none_rmvevoked_100k.sh $sbj_num &


#4. - with baseline - #
# - none - #
# - 3k - #
#sbatch scripts/eCortex/temp_gen/rand_temp_gen_earlyPrePost_none.sh $sbj_num &
#sbatch scripts/eCortex/temp_gen/rand_temp_gen_laterPrePost_none.sh $sbj_num &

# - with baseline - #
# - none - #
# - 100k - #
#sbatch scripts/eCortex/temp_gen/rand_temp_gen_earlyPrePost_none_100k.sh $sbj_num &
#sbatch scripts/eCortex/temp_gen/rand_temp_gen_laterPrePost_none_100k.sh $sbj_num &



done

wait
