#!/bin/bash

QEROOT=/Users/lioneltruflandier/q-e
LD1ROOT=$QEROOT/atomic

patch $LD1ROOT/src/ld1_readin.f90 < ld1_gipaw.patch 
