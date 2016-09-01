#! /usr/bin/env python
# -*- coding: utf-8 -*-

#####################################################################################
#####################################################################################
###                                                                               ###
###     Goal:                                                                     ###
###         Create Gene and Adjacency files for ARt-DeCo from EMF file            ###
###                                                                               ###
###     INPUT:                                                                    ###
###         EMF input file with gene position for all species
###         Selected species file                                                 ###
###
###     OUTPUT:
###         3 files for ARt-DeCo (Gene & Adjacency & Species files):
###
###             - species_gene.tab,
###             - adjacencies.tab,
###             - species.tab
###                                                                               ###
###   Name: 02-create_INPUT_files_for_AD.py       Author: Yoann Anselmetti        ###
###   Creation date: 2015/09/22                   Last modification: 2016/05/11   ###
###                                               Modified by: Fred Bigey         ###
###                                               Last modification: 2016/06/24   ###
###                                                                               ###
#####################################################################################
#####################################################################################

from sys import argv, stdout
from datetime import datetime
from re import search
from os import close, path, makedirs


################
### FUNCTION ###
################
def mkdir_p(dir_path):
   try:
      makedirs(dir_path)
   except OSError as exc: # Python >2.5
      if exc.errno == errno.EEXIST and path.isdir(dir_path):
         pass
      else: raise


############
### MAIN ###
############
if __name__ == '__main__':

    start_time = datetime.now()
    speciesToKeep = {}

    # Recovery of input parameters
    INPUT_file=argv[1]
    INPUT_species=argv[2]

    # Store species names
    with open(INPUT_species, 'r') as f:
        for line in f:
            # speciesToKeep.append(line.split("\t")[1])
            name    = line.split("\t")[0]
            genus   = name.split(" ")[0]
            species = name.split(" ")[1]

            id = line.split("\t")[1]
            speciesToKeep[id] = genus + "_" + species

    f.close()

    print "Species to keep:"
    print speciesToKeep
    print

    # Creating file handles
    gene_file=open(INPUT_file,'r')
    output_gene=open("species_gene.tab",'w')
    output_adj=open("adjacencies.tab",'w')
    output_species = open("species.tab", 'w')

    species=""
    contig=""
    gene_store=""
    old_strand = ""
    nb_contig = 0

    # Main loop
    for gene in gene_file:

        # Regex search for species, transcript, contig and strand
        r = search('^([^\s]+)\s([^\s]+)\s([^\s]+)\s([^\s]+)\s([^\s]+)\s([^\s]+)\n$', gene)

        if r:
            name_species = r.group(1)
            gene_ID = r.group(2)
            contig_ID = r.group(3)
            strand = r.group(6)

            if name_species not in speciesToKeep:
                continue

            output_gene.write(speciesToKeep[name_species] + "\t" + gene_ID + "\n")

            if name_species == species and contig_ID == contig and strand == old_strand:
                output_adj.write(gene_store + "\t" + gene_ID + "\n")
                gene_store = gene_ID
            else:
                if species == "" or (name_species == species and contig_ID != contig):
                    nb_contig += 1
                elif name_species != species:
                    output_species.write(speciesToKeep[species] + '\t' \
                        + str(nb_contig) + '\n')
                    nb_contig = 1

                species = name_species
                contig = contig_ID
                gene_store = gene_ID
                old_strand = strand
        else:
            exit("ERROR at line: " + line)

    # print speciesToKeep[name_species], nb_contig

    gene_file.close()
    output_gene.close()
    output_adj.close()
    output_species.close()

    end_time = datetime.now()
    print('\nDuration: {}'.format(end_time - start_time))

exit(0)
