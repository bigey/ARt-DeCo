#!/usr/bin/env python

import sys
import os.path
import re
from Bio import Phylo

newickDir = 'Newick/'
alignDir  = 'Alignment/'

if len(sys.argv) == 1:
    sys.exit(1)

# Create output Newick tree directory
if not os.path.isdir(newickDir):
    os.mkdir(newickDir)

# Create output Alignment directory
if not os.path.isdir(alignDir):
    os.mkdir(alignDir)


file = sys.argv[1]
base = os.path.basename(file)
searchObj = re.search(r'^(.*)\.(.*)\.xml', base)
treeId = searchObj.group(1)

# Output newick tree
newickFile = newickDir + treeId + '.nwk'
tree = Phylo.read(file, "phyloxml")
Phylo.write(tree, newickFile, 'newick')

# Output multi sequence alignment (MSA)
alignOutput = open(alignDir + treeId + '.msa.fasta', 'w')

for clade in tree.get_terminals():
    [cladeId, properties, sequence, ensembl, alignment, species, taxon] = \
        [x for x in clade.find_elements()]
    geneId = cladeId.name
    transcriptID = ensembl.value
    alignOutput.write(">{0}| {1}, {2}".format(transcriptID, \
        species.scientific_name, taxon.value)+"\n")
    alignOutput.write(str(alignment)+"\n")

alignOutput.close()
exit()
