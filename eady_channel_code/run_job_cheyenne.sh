#!/bin/bash
### Job Name
#PBS -A PROJECT_CODE
#PBS -N Eady_channel
#PBS -l walltime=01:00:00
#PBS -q regular
#PBS -l select=6:ncpus=36:mpiprocs=36
### Send email on abort, begin and end
#PBS -m abe
#PBS -M YOUR@EMAIL.ADDRESS
### Merge output and error files
#PBS -j oe
##PBS -k eod

### Run the executable
CESM_ROOT="/PATH/TO/WHERE/YOU/INSTALLED/cesm2_3_alpha12b+mom6_marbl"
mpiexec_mpt -np 216 $CESM_ROOT/components/mom/standalone/build/intel/MOM6/MOM6
