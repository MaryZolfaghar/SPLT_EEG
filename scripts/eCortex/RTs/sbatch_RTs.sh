#!/usr/bin/env bash
#SBATCH -p localLimited
#SBATCH -A ecortex
#SBATCH --mem=10G

export HOME=`getent passwd $USER | cut -d':' -f6`
export PYTHONUNBUFFERED=1
echo Running on $HOSTNAME

source /usr/local/anaconda3/etc/profile.d/conda.sh
conda activate /home/mazlfghr/.conda/envs/DeepLearningEEG

sbatch scripts/eCortex/temp_gen/sbatch_randP1_early.sh &
sbatch scripts/eCortex/temp_gen/sbatch_randP1_later.sh &
sbatch scripts/eCortex/temp_gen/sbatch_randP2_early.sh &
sbatch scripts/eCortex/temp_gen/sbatch_randP2_later.sh &

wait
