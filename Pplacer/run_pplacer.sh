#/bin/bash
# set -e

NEWICK_DIR=../TreeConversion/PrunedNewick
ALIGN_DIR=../TreeConversion/PrunedAlignment
FORTYTWO_DIR=../FortyTwo/Result

PHYLIP_DIR=Phylip
FASTA_DIR=Fasta
OUT_DIR=Result

i=0

echo "Starting $0" >nohup.out
echo $(date)
test -d $PHYLIP_DIR && rm -rf $PHYLIP_DIR
test -d $FASTA_DIR && rm -rf $FASTA_DIR
test -d $OUT_DIR && rm -rf $OUT_DIR

mkdir $PHYLIP_DIR $FASTA_DIR $OUT_DIR

for f in $FORTYTWO_DIR/*.fasta
do
    ((i=i+1))
    base=$(basename $f)
    tree_id=$(basename $f .msa.42.fasta)

    echo
    echo "### sequence $i: $base"

    rm -f RAxML_*
    rm -rf *.pkg

    # Convert alignment to PHYLIP format
    fasta2phylip.sh $ALIGN_DIR/$tree_id.msa.fasta >$PHYLIP_DIR/$tree_id.phy

    # Creating RAxML info file from tree and alignment
    raxmlHPC -f e \
        -m PROTGAMMAJTT \
        -t $NEWICK_DIR/$tree_id.nwk \
        -s $PHYLIP_DIR/$tree_id.phy \
        -n $tree_id || continue

    echo "RAxML exit code: $?"

    # Create package (*.pkg) containing tree and ref alignment
    taxit create \
        -l $tree_id \
        -P $tree_id.pkg \
        --aln-fasta $PHYLIP_DIR/$tree_id.phy \
        --tree-file $NEWICK_DIR/$tree_id.nwk \
        --tree-stats RAxML_info.$tree_id || continue

    echo "taxit exit code: $?"

    # Rename definition line of Forty-Two fasta MSA
    #  >ID
    perl -pe 's/^>\w+\@(\w+).*$/>$1/' $f >$FASTA_DIR/$tree_id.fasta

    # Place query sequence on tree
    pplacer \
        -c $tree_id.pkg \
        --out-dir $OUT_DIR \
        $FASTA_DIR/$tree_id.fasta || continue

    echo "pplacer exit code: $?"

    # Makes one tree for each query sequence
    guppy sing \
        --out-dir $OUT_DIR \
        -o $tree_id.pplacer.nwk \
        $OUT_DIR/$tree_id.jplace || continue

    echo "guppy exit code: $?"

    # Clean
    rm -f RAxML_*
    rm -rf *.pkg
done

echo
echo "End of $0"
echo $(date)
