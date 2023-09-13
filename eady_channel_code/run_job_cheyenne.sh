#!/bin/bash
### Job Name
#PBS -A P93300612
#PBS -N Eady_channel
#PBS -l walltime=01:00:00
#PBS -q regular
#PBS -l select=6:ncpus=36:mpiprocs=36
### Send email on abort, begin and end
#PBS -m abe
#PBS -M dafydd@ucar.edu
### Merge output and error files
#PBS -j oe
##PBS -k eod

### Run the executable
CESM_ROOT="/glade/scratch/dafydd/MOM6/cesm2_3_alpha12b+mom6_marbl"
mpiexec_mpt -np 216 $CESM_ROOT/components/mom/standalone/build/intel/MOM6/MOM6
