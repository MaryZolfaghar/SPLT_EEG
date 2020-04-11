#!/bin/bash
#SBATCH --time=72:00:00
#SBATCH -c 16
#SBATCH --qos=blanca-ccn

export HOME=`getent passwd $USER | cut -d':' -f6`
echo $HOME
export PYTHONUNBUFFERED=1

echo Running on $HOSTNAME

source /pl/active/ccnlab/conda/etc/profile.d/conda.sh
conda activate /pl/active/ccnlab/users/zolfaghar/conda/SPLTEEG


PYTHONPATH=/pl/active/ccnlab/users/zolfaghar/finalCodes_version5.2/github/SPLT_EEG/

selected_subj=( 1 2 3 4 5 7 8 9 10 12 15 16 17 18 19 20 21 22 23 24 25 26 27 28\
                29 30 31 32 33 34 35 36 37 38 39 42 43 44 45 46 47 48 51 52 53 \
                55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74)

start time
date +"%H:%M:%S"

for i in "${selected_subj[@]}"
do
echo $i
sbj_num=$i

echo "Process subject $sbj_num starts"

#1. - no baseline - #
# - removed evoked - #
# sbatch scripts/blanca/autocorr/autocorr_earlyPrePost_none_noBsline_rmvevoked.sh $sbj_num &
# sbatch scripts/blanca/autocorr/autocorr_laterPrePost_none_noBsline_rmvevoked.sh $sbj_num &

#2. - no baseline - #
# - none - #
sbatch scripts/blanca/autocorr/autocorr_earlyPrePost_none_noBsline.sh $sbj_num &
sbatch scripts/blanca/autocorr/autocorr_laterPrePost_none_noBsline.sh $sbj_num &

#3. - with baseline - #
# - removed evoked - #
sbatch scripts/blanca/autocorr/autocorr_earlyPrePost_none_rmvevoked.sh $sbj_num &
sbatch scripts/blanca/autocorr/autocorr_laterPrePost_none_rmvevoked.sh $sbj_num &

#4. - with baseline - #
# - none - #
sbatch scripts/blanca/autocorr/autocorr_earlyPrePost_none.sh $sbj_num &
sbatch scripts/blanca/autocorr/autocorr_laterPrePost_none.sh $sbj_num &

done

wait
