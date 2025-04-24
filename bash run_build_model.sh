#!/bin/bash
mkdir -p Build_model
cp complex_Repair.pdb individual_list.txt Build_model/
cd Build_model
FoldX --command=BuildModel --pdb=complex_Repair.pdb --mutant-file=individual_list.txt --numberOfRuns=3
