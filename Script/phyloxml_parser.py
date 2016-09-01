#!/usr/bin/env python

import sys
import re
import os.path
from ete3 import Phyloxml

usage = \
"""

    USAGE: Phyloxml_parser.pl <tree> [<species_table>]
"""

newickDir = 'Newick/'
newickPrunedDir = 'PrunedNewick/'
alignDir  = 'Alignment/'
prunedAlignDir = 'PrunedAlignment/'

# Command line arguments test
if len(sys.argv) == 3:
    prune = True
    # Create pruned Newick tree directory
    if not os.path.isdir(newickPrunedDir):
        os.mkdir(newickPrunedDir)
    if not os.path.isdir(prunedAlignDir):
        os.mkdir(prunedAlignDir)
elif len(sys.argv) == 2:
    prune = False
else:
    print "ERROR: wrong number of arguments!", usage
    sys.exit(1)

# Create Newick tree directory
if not os.path.isdir(newickDir):
    os.mkdir(newickDir)

# Create Alignment directory
if not os.path.isdir(alignDir):
    os.mkdir(alignDir)

# Create Phyloxml projet and import tree file
project = Phyloxml()
project.build_from_file(sys.argv[1])
tree = project.get_phylogeny()[0]
print "Initial tree:"
print tree
print

# Extract tree id
file = sys.argv[1]
base = os.path.basename(file)
searchObj = re.search(r'^(.*)\.(.*)\.xml', base)
treeId = searchObj.group(1)

# Output multi sequence alignment (MSA)
alignOutput = open(alignDir + treeId + '.msa.fasta', 'w')

# Parse the PhyloXML tree
print "Tree leaves:"
print

speciesInTree = []
genesInTree = {}
i = 1
for node in tree.get_leaves():

    print "Leave #", i
    i += 1

    # Features are stored in the 'phyloxml_clade' attribute

    for taxo in node.phyloxml_clade.get_taxonomy():
        scientificName = taxo.scientific_name
        taxonId = taxo.id.get_valueOf_()
        print "Scientific name:", scientificName
        print "Taxon id:", taxonId

    print "Gene id:", node.name

    for prop in node.phyloxml_clade.get_property():
        strainId = prop.get_valueOf_()
        speciesInTree.append(strainId)
        print "Property:", strainId

    print "Sequence:"
    for seq in node.phyloxml_clade.get_sequence():
        transcriptID = seq.accession.get_valueOf_()
        location = seq.location
        sequence = seq.mol_seq.get_valueOf_()
        print "   name:", transcriptID
        print "   location:", location
        # print "   mol_seq:\n", sequence

    # Change node.name from GeneID -> transcriptID
    node.name = transcriptID

    alignOutput.write(">{0}| {1}, {2}".format(transcriptID, \
        scientificName, taxonId)+"\n")
    alignOutput.write(str(sequence)+"\n")

    genesInTree[strainId] = node.name
    print

# Close alignment file
alignOutput.close()

# Output initial tree in Newick format
newickFile = newickDir + treeId + '.nwk'
tree.write(outfile=newickFile, format=1)
print "Initial tree, changed node name:"
print tree
print

# All species present in tree
print "Species in tree:"
print speciesInTree
print

# If pruning, read file containing species to keep
if prune == True:

    speciesToKeep = []

    with open(sys.argv[2], 'r') as f:
        for line in f:
            speciesToKeep.append(line.split("\t")[1])

    f.close()

    print "Species to keep:"
    print speciesToKeep
    print

    # Species to output are in the intersection of both lists
    speciesToOutput = list( set(speciesToKeep).intersection(set(speciesInTree)) )
    print "Output species:"
    print speciesToOutput
    print

    # If no more sequence in tree
    if len(speciesToOutput) == 0:
        print "No sequence to output... skeep!"
        print
        exit(0)

    # Get transcriptID from the hash {species => transcriptID}
    genesToOutput = [genesInTree[x] for x in speciesToOutput]
    print "Gene to output:"
    print genesToOutput
    print

    # Prune tree: keep only species present in "speciesToOutput" list
    tree.prune(genesToOutput, preserve_branch_length=True)
    print "Pruned tree:"
    print tree
    print
    newickPrunedFile = newickPrunedDir + treeId + '.nwk'
    tree.write(outfile=newickPrunedFile, format=1)

    # Export pruned alignment
    prunedAlign = open(prunedAlignDir + treeId + '.msa.fasta', 'w')

    for node in tree.get_leaves():

        # Features are stored in the 'phyloxml_clade' attribute

        for taxo in node.phyloxml_clade.get_taxonomy():
            scientificName = taxo.scientific_name
            taxonId = taxo.id.get_valueOf_()

        for seq in node.phyloxml_clade.get_sequence():
            transcriptID = seq.accession.get_valueOf_()
            sequence = seq.mol_seq.get_valueOf_()

        prunedAlign.write(">{0}| {1}, {2}".format(transcriptID, \
            scientificName, taxonId)+"\n")
        prunedAlign.write(str(sequence)+"\n")

    # Close alignment file
    prunedAlign.close()


exit()
