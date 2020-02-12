import os
import subprocess

from biocodes_detok import Detok
from res_brat import Result_brat

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-data_bio", "--data_bio", type=str)
parser.add_argument("-result_folder", "--result_folder", type=str)
parser.add_argument("-data", "--data", type=str)
parser.add_argument("-entity", "--entity", type=str)
parser.add_argument("-perl_path", "--perl_path", type=str, default="biocodes/conlleval.pl")
args = parser.parse_args()

detok = Detok(os.path.join(args.data_bio, "test.tsv"), os.path.join(args.result_folder, "token_test.txt"),
              os.path.join(args.result_folder, "label_test.txt"),
              os.path.join(args.result_folder, "NER_result_conll.txt"))
detok.get_detok()

## perl
subprocess.check_call([args.perl_path, args.result_folder])

brat_files = Result_brat(args.data, args.result_folder, args.entity)
brat_files.get_brat_folder()

