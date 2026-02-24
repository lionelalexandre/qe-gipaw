#!/bin/bash

# how to patch
# diff -u file file_corr >> file.patch
# patch [options] file_to_patch < file.patch
# [options] -b keep backtrack of original file
# [options] -R reverse patching

QEROOT=/Users/lioneltruflandier/q-e
QEGIPAWROOT=/Users/lioneltruflandier/q-e-gipaw
LD1ROOT=$QEROOT/atomic

#patch -b $LD1ROOT/src/ld1_readin.f90 < ld1_gipaw.patch 
#patch -b $QEGIPAWROOT/src/gipaw_routines.f90 < ms_gipaw_routines.patch
#patch -b $QEGIPAWROOT/src/suscept_crystal.f90< ms_.suscept_crystal.patch

