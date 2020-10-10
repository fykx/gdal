#!/bin/bash
#PBS -N test_1
#PBS -l nodes=5:ppn=16
#PBS -j n
#PBS -l walltime=4:00:00
cd $PBS_O_WORKDIR

NP=`cat $PBS_NODEFILE | wc -l`

mpiexec -n $NP python Interpolation.py -i /public/home/mfeng/work/test/forest/pangyong/phase2/ne/forest/file12/scene04/comp01/data -o /public/home/mfeng/jwang/forest/northeast/tcc -s comp01 -n $NP
