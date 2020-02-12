#!/bin/bash
TMP_DIR=$1
cadecarr=()
psytararr=()
SCRIPTPATH=$( cd "$(dirname "$0")" ; pwd -P )
BIOBERT_DIR=${SCRIPTPATH}/BIOBERT_DIR
IFS=$'\n'
python3 main_pre.py -data data/cadec,data/psytar -folds_path data/cadec_folds,data/psytar_folds \
    -bio_paths data/cadec_folds_biobert,data/psytar_folds_biobert -n_folds 5 \
    -entity adr -tagger averaged_perceptron_tagger -vocab_file ${BIOBERT_DIR}/vocab.txt
for directory in ${SCRIPTPATH}/data/cadec_folds_biobert/*
do
for fold in $directory
do
echo $fold
cadecarr+=("$fold")
done
done
for directory1 in ${SCRIPTPATH}/data/psytar_folds_biobert/*
do
for fold1 in $directory1
do
echo $fold1
psytararr+=("$fold1")
done
done
mkdir $TMP_DIR
for (( i=0; i < "${#cadecarr[@]}"; i++ ))
do
mkdir "${TMP_DIR}/cadec_fold_0${i}_cadec_test"
outputdir=${TMP_DIR}/cadec_fold_0${i}_cadec_test
python3 run_ner.py --do_train=true --do_eval=true --vocab_file=${BIOBERT_DIR}/vocab.txt \
    --bert_config_file=${BIOBERT_DIR}/bert_config.json \
    --init_checkpoint=${BIOBERT_DIR}/biobert_model.ckpt \
    --num_train_epochs=50.0 \
    --data_dir="${cadecarr[$i]}" \
    --output_dir=$outputdir
cp ${TMP_DIR}/cadec_fold_0${i}_cadec_test -R ${TMP_DIR}/cadec_fold_0${i}_psytar_test
outputdir1=${TMP_DIR}/cadec_fold_0${i}_psytar_test
python3 run_ner.py --do_train=false --do_predict=true --do_eval=true --vocab_file=${BIOBERT_DIR}/vocab.txt \
    --bert_config_file=${BIOBERT_DIR}/bert_config.json \
    --init_checkpoint=${BIOBERT_DIR}/biobert_model.ckpt \
    --num_train_epochs=50.0 \
    --data_dir="${cadecarr[$i]}" \
    --output_dir=$outputdir
python3 run_ner.py --do_train=false --do_predict=true --do_eval=true --vocab_file=${BIOBERT_DIR}/vocab.txt \
    --bert_config_file=${BIOBERT_DIR}/bert_config.json \
    --init_checkpoint=${BIOBERT_DIR}/biobert_model.ckpt \
    --num_train_epochs=50.0 \
    --data_dir="${psytararr[$i]}" \
    --output_dir=$outputdir1
python3 main_post.py -data_bio ${cadecarr[$i]} -result_folder ${outputdir} -data ${SCRIPTPATH}/data/cadec_folds/0${i} -entity adr -perl_path biocodes/conlleval.pl
python3 main_post.py -data_bio ${psytararr[$i]} -result_folder ${outputdir1} -data ${SCRIPTPATH}/data/psytar_folds/0${i}/test.json -entity adr -perl_path biocodes/conlleval.pl
done
for (( i=0; i < "${#psytararr[@]}"; i++ ))
do
mkdir "${TMP_DIR}/psytar_fold_0${i}_cadec_test"
outputdir=${TMP_DIR}/psytar_fold_0${i}_cadec_test
python3 run_ner.py --do_train=true --do_eval=true --vocab_file=${BIOBERT_DIR}/vocab.txt \
    --bert_config_file=${BIOBERT_DIR}/bert_config.json \
    --init_checkpoint=${BIOBERT_DIR}/biobert_model.ckpt \
    --num_train_epochs=50.0 \
    --data_dir="${psytararr[$i]}" \
    --output_dir=$outputdir
cp ${TMP_DIR}/psytar_fold_0${i}_cadec_test -R ${TMP_DIR}/psytar_fold_0${i}_psytar_test
outputdir1=${TMP_DIR}/psytar_fold_0${i}_psytar_test
python3 run_ner.py --do_train=false --do_predict=true --do_eval=true --vocab_file=${BIOBERT_DIR}/vocab.txt \
    --bert_config_file=${BIOBERT_DIR}/bert_config.json \
    --init_checkpoint=${BIOBERT_DIR}/biobert_model.ckpt \
    --num_train_epochs=50.0 \
    --data_dir="${cadecarr[$i]}" \
    --output_dir=$outputdir
python3 run_ner.py --do_train=false --do_predict=true --do_eval=true --vocab_file=${BIOBERT_DIR}/vocab.txt \
    --bert_config_file=${BIOBERT_DIR}/bert_config.json \
    --init_checkpoint=${BIOBERT_DIR}/biobert_model.ckpt \
    --num_train_epochs=50.0 \
    --data_dir="${psytararr[$i]}" \
    --output_dir=$outputdir1
python3 main_post.py -data_bio ${cadecarr[$i]} -result_folder ${outputdir} -data ${SCRIPTPATH}/data/cadec_folds/0${i} -entity adr -perl_path biocodes/conlleval.pl
python3 main_post.py -data_bio ${psytararr[$i]} -result_folder ${outputdir1} -data ${SCRIPTPATH}/data/psytar_folds/0${i}/test.json -entity adr -perl_path biocodes/conlleval.pl
done