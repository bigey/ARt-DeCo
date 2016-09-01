#/bin/bash
set -e

ALIGN_DIR=../TreeConversion/PrunedAlignment
RENAME_ALIGN_DIR=FormatedAlignment
OUT_DIR=Result
CONFIG=42.config.yaml
SCRIPT=forty-two.pl
size=123205
i=0

echo "Starting FORTY-TWO" >nohup.out
test -d $RENAME_ALIGN_DIR && rm -rf $RENAME_ALIGN_DIR
test -d $OUT_DIR && rm -rf $OUT_DIR

mkdir $RENAME_ALIGN_DIR $OUT_DIR

for f in $ALIGN_DIR/*.msa.fasta
do
    ((i=i+1))
    out=$(basename $f)
    prefix=$(basename $f .fasta)

    echo
    echo "### [$i/$size]: $out"

    # Reformat fasta definition line:
    #  >Saccharomyces_cerevisiae@YOR203
    perl -pe 's/^>(\w+)\| (\w+) (\w+),*.*$/>${2}_${3}\@${1}/' $f \
        >$RENAME_ALIGN_DIR/$out

    # Run forty-two on alignment $out
    $SCRIPT --config=$CONFIG $RENAME_ALIGN_DIR/$out

    # If ortholog found in alignment
    if [ $(grep -c '#NEW#' $RENAME_ALIGN_DIR/$prefix.42.fasta) -gt 0 ]
    then
        # Convert *.bak to *.fasta (msa)
        cp $RENAME_ALIGN_DIR/$prefix.42.fasta $OUT_DIR
        ali2fasta.pl $OUT_DIR/$prefix.42.fasta
    fi
done
