#!/usr/bin/env bash
#SBATCH -p localLimited
#SBATCH -A ecortex
#SBATCH --mem=10G

export HOME=`getent passwd $USER | cut -d':' -f6`
export PYTHONUNBUFFERED=1
echo Running on $HOSTNAME

source /usr/local/anaconda3/etc/profile.d/conda.sh
conda activate /home/mazlfghr/.conda/envs/DeepLearningEEG

# removed subjects : 17 22 37 27 17 25 27 70, issues are in the notes.txt
selected_subj=( 1 2 3 4 5 7 8 9 10 12 15 16 18 19 20 21 23 24 26 28\
                29 30 31 32 33 34 35 36 38 39 42 43 44 45 46 47 48 51 52 53 \
                55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 71 72 73 74)

# selected_subj=(1)
for i in "${selected_subj[@]}"
do
echo $i
sbj_num=$i

# ----------------------- upcoming trial ------------------#
#1. - no baseline - #
# - removed evoked - #
# sbatch scripts/eCortex/ERPs/ERP_earlyPrePost_none_noBsline_rmvevoked.sh $sbj_num &
# sbatch scripts/eCortex/ERPs/ERP_laterPrePost_none_noBsline_rmvevoked.sh $sbj_num &

#2. - no baseline - #
# - removed evoked - #
# only occipital channels
# sbatch scripts/eCortex/ERPs/ERP_earlyPrePost_none_noBsline_rmvevoked_occ.sh $sbj_num &
# sbatch scripts/eCortex/ERPs/ERP_laterPrePost_none_noBsline_rmvevoked_occ.sh $sbj_num &

#3. - no baseline - #
# - none - #
# only occipital channels
# sbatch scripts/eCortex/ERPs/ERP_earlyPrePost_none_noBsline_occ.sh $sbj_num &
# sbatch scripts/eCortex/ERPs/ERP_laterPrePost_none_noBsline_occ.sh $sbj_num &

#4. - WITH baseline - #
# - removed evoked  - #
# only occipital channels
# sbatch scripts/eCortex/ERPs/ERP_earlyPrePost_none_rmvevoked_occ.sh $sbj_num &
# sbatch scripts/eCortex/ERPs/ERP_laterPrePost_none_rmvevoked_occ.sh $sbj_num &

#5. - WITH baseline - #
# - none - #
# only occipital channels
# sbatch scripts/eCortex/ERPs/ERP_earlyPrePost_none_occ.sh $sbj_num &
# sbatch scripts/eCortex/ERPs/ERP_laterPrePost_none_occ.sh $sbj_num &

# # ----------------------- previous trial ------------------#
#1. - no baseline - #
# - removed evoked - #
# only occipital channels
# prev trials
sbatch scripts/eCortex/ERPs/ERP_randPrePost_none_noBsline_rmvevoked_occ_mainLoc.sh $sbj_num &
# sbatch scripts/eCortex/ERPs/ERP_earlyPrePost_none_noBsline_rmvevoked_occ_prevLoc.sh $sbj_num &
# sbatch scripts/eCortex/ERPs/ERP_laterPrePost_none_noBsline_rmvevoked_occ_prevLoc.sh $sbj_num &

#2. - no baseline - #
# - none - #
# only occipital channels
# prev trials
# sbatch scripts/eCortex/ERPs/ERP_earlyPrePost_none_noBsline_occ_prevLoc.sh $sbj_num &
# sbatch scripts/eCortex/ERPs/ERP_laterPrePost_none_noBsline_occ_prevLoc.sh $sbj_num &
# #
# #3. - WITH baseline - #
# # - removed evoked  - #
# # only occipital channels
# # prev trials
# sbatch scripts/eCortex/ERPs/ERP_earlyPrePost_none_rmvevoked_occ_prevLoc.sh $sbj_num &
# sbatch scripts/eCortex/ERPs/ERP_laterPrePost_none_rmvevoked_occ_prevLoc.sh $sbj_num &
#
# #- WITH baseline - #
# # - none  - #
# # only occipital channels
# # prev trials
# sbatch scripts/eCortex/ERPs/ERP_earlyPrePost_none_occ_prevLoc.sh $sbj_num &
# sbatch scripts/eCortex/ERPs/ERP_laterPrePost_none_occ_prevLoc.sh $sbj_num &

done

wait
