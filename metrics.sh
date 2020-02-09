#!/bin/bash
outputdir=$1
SCRIPTPATH=$( cd "$(dirname "$0")" ; pwd -P )
IFS=$'\n'
perl ${SCRIPTPATH}/biocodes/conlleval.pl < ${outputdir}/NER_result_conll.txt
cp ${SCRIPTPATH}/metrics.txt ${outputdir}/metrics.txt
rm metrics.txt