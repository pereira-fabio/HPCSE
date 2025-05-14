#!/bin/bash
#SBATCH --job-name="rfm_OSUBandwidthTest"
#SBATCH --ntasks=2
#SBATCH --ntasks-per-node=2
#SBATCH --cpus-per-task=1
#SBATCH --output=rfm_job.out
#SBATCH --error=rfm_job.err
srun --cpus-per-task=1 /opt/apps/easybuild/systems/aion/rhel810-20250405/2023b/epyc/software/OSU-Micro-Benchmarks/7.5-gompi-2023b/libexec/osu-micro-benchmarks/mpi/pt2pt/osu_bw
