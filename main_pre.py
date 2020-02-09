import os

from Folds import Folds
from json2conll import Json2conll
from bio_conll import BIO_conll
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-data", "--data", type=str, default="data/cadec,data/psytar")
parser.add_argument("-folds_path", "--folds_path", type=str, default="data/cadec_folds,data/psytar_folds")
parser.add_argument("-bio_paths", "--bio_paths", type=str, default="data/cadec_folds_biobert,data/psytar_folds_biobert")
parser.add_argument("-n_folds", "--n_folds", type=int, default=5)
parser.add_argument('--entity', '-entity', type=str, default='adr drug')
parser.add_argument('--tagger', '-tagger', type=str, default='averaged_perceptron_tagger')
parser.add_argument('--vocab_file', '-vocab_file', type=str, default='BIOBERT_DIR/vocab.txt')
parser.add_argument('--do_lower_case', '-do_lower_case', type=bool, default=True)

args = parser.parse_args()


dirs = args.data.split(",")
fold_dirs = args.folds_path.split(",")
bio_dirs = args.bio_paths.split(",")
entity = args.entity
tagger = args.tagger
vocab = args.vocab_file
lower_case = args.do_lower_case
for i in range(len(dirs)):
    folds = Folds(dirs[i], fold_dirs[i], args.n_folds)
    folds.get_folds()

for fold_dir,bio_dir in zip(fold_dirs,bio_dirs):
    conll = Json2conll(fold_dir, entity, tagger, vocab, lower_case)
    conll.get_conlls()
    bio = BIO_conll(fold_dir,bio_dir)
    bio.get_bio()

