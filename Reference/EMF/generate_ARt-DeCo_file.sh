#!/bin/bash
set -e

EMF=Compara.newick_trees.31.emf.gz
OUTPUT=Compara.transcript.sorted.tab
SCRIPT=../../Script/02-create_INPUT_files_for_AD.py
SPECIES=../../Configuration/selected_species.tab

rm -f *.tab

zcat $EMF | grep "^SEQ" \
    | cut -d" " -f 2-7 \
    | sort -k 1,1 -k 3,3 -k 6,6 -k4,4n \
    >$OUTPUT

$SCRIPT $OUTPUT $SPECIES
exit
