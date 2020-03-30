#!/usr/bin/env bash
#SBATCH -p localLimited
#SBATCH -A ecortex
#SBATCH --mem=16G

export HOME=`getent passwd $USER | cut -d':' -f6`
export PYTHONUNBUFFERED=1
echo Running on $HOSTNAME

source /usr/local/anaconda3/etc/profile.d/conda.sh
conda activate /home/mazlfghr/.conda/envs/DeepLearningEEG

selected_subj=( 1 2 3 4 5 7 8 9 10 12 15 16 17 18 19 20 21 22 23 24 25 26 27 28\
                29 30 31 32 33 34 35 36 37 38 39 42 43 44 45 46 47 48 51 52 53 \
                55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74)

for i in "${selected_subj[@]}"
do
echo $i
sbj_num=$i
echo "Process $sbj_num starts"

sbatch temp_gen_earlyPrePost_none_noBsline_rmvevoked.sh $sbj_num &
sbatch temp_gen_earlyPrePost_none_noBsline.sh $sbj_num &
sbatch temp_gen_earlyPrePost_none.sh $sbj_num &
sbatch temp_gen_laterPrePost_none_noBsline_rmvevoked.sh $sbj_num &
sbatch temp_gen_laterPrePost_none_noBsline.sh $sbj_num &
sbatch temp_gen_laterPrePost_none.sh $sbj_num &
sbatch rand_temp_gen_earlyPrePost_none_noBsline_rmvevoked.sh $sbj_num &
sbatch rand_temp_gen_earlyPrePost_none_noBsline.sh $sbj_num &
sbatch rand_temp_gen_earlyPrePost_none.sh $sbj_num &
sbatch rand_temp_gen_laterPrePost_none_noBsline_rmvevoked.sh $sbj_num &
sbatch rand_temp_gen_laterPrePost_none_noBsline.sh $sbj_num &
sbatch rand_temp_gen_laterPrePost_none.sh $sbj_num &

done

wait
