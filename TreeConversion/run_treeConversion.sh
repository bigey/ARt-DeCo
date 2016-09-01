#/bin/bash
set -e

PHYLO_DIR=../EnsemblFungi/Compara.phyloxml_aa_trees.31
STRAIN_FILE=../Configuration/selected_species.tab
SCRIPT=../Script/phyloxml_parser.py
size=123205
i=0

rm -rf Newick/ PrunedNewick/ Alignment/ PrunedAlignment/

for xml in $PHYLO_DIR/*/*.xml
do
    ((i=$i+1))
    echo "[$i/$size]: $xml"
    $SCRIPT $xml $STRAIN_FILE
done
