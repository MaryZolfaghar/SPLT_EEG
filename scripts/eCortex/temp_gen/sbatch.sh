#!/usr/bin/env bash
#SBATCH -p localLimited
#SBATCH -A ecortex
#SBATCH --mem=1G

export HOME=`getent passwd $USER | cut -d':' -f6`
export PYTHONUNBUFFERED=1
echo Running on $HOSTNAME

source /usr/local/anaconda3/etc/profile.d/conda.sh
conda activate /home/mazlfghr/.conda/envs/DeepLearningEEG

# removed subjects : 17 22 37 27 17 25 27 70, issues are in the notes.txt
selected_subj=( 1 2 3 4 5 7 8 9 10 12 15 16 18 19 20 21 23 24 26 28\
                29 30 31 32 33 34 35 36 38 39 42 43 44 45 46 47 48 51 52 53 \
                55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 71 72 73 74)

for i in "${selected_subj[@]}"
do
echo $i
sbj_num=$i
# echo "Process $sbj_num starts"

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
sbatch scripts/eCortex/temp_gen/rand_temp_gen_earlyPrePost_none_noBsline_rmvevoked.sh $sbj_num &
sbatch scripts/eCortex/temp_gen/rand_temp_gen_laterPrePost_none_noBsline_rmvevoked.sh $sbj_num &

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
