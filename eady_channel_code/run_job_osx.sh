#!/bin/bash
CESM_ROOT="/PATH/TO/WHERE/YOU/INSTALLED/cesm2_3_alpha12b+mom6_marbl"
mpirun -n 16 $CESM_ROOT/components/mom/standalone/build/gnu/MOM6/MOM6
