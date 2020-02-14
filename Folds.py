import math
import os

import pandas as pd
from sklearn.model_selection import KFold


class Folds:

    def __init__(self, first, output, folds):
        self.first = first
        self.output = output
        self.folds = folds

    def get_entity_and_slice(self,directory):
        result = []
        for filename in sorted(os.listdir(directory)):
            f = open(os.path.join(directory, filename))
            text = f.read().lower().split("\n")
            rev = []
            for elem in text[:-1]:
                sentence = elem.replace("\t", " ")
                words = sentence.split(" ")
                if words[0][0] == "#":
                    continue
                ent = words[1:4]
                ent.append(elem.split("\t")[-1])
                rev.append(ent)
            result.append(rev)
        return result

    def get_text(self,directory):
        result = []
        names = []
        n_s = []
        for filename in sorted(os.listdir(directory)):
            f = open(os.path.join(directory, filename))
            text = f.read()
            n_sen = text.count("\n")
            text = text.replace("\n", " ")
            text = text.lower()
            result.append(text)
            names.append(filename[:-4])
            n_s.append(n_sen)
            f.close()
        return result, names, n_s

    def make_entity_dictionary(self, ent, len_dataset):
        result = {}
        for i in range(len_dataset):
            d = {}

            for j in range(len(ent[i])):
                if ';' in ent[i][j][1]:
                    ent[i][j][1] = int(ent[i][j][1].split(";")[-1])
                if ';' in ent[i][j][2]:
                    ent[i][j][2] = int(ent[i][j][2].split(";")[-1])
                d[j] = {'start': ent[i][j][1], 'end': ent[i][j][2],
                        'entity': ent[i][j][0], 'text': ent[i][j][3]}
            result[i] = d
        return result

    def get_folds(self):
        df = pd.DataFrame(columns=['filename', 'text', 'sentences', 'entities'])

        text_path = os.path.join(self.first,"text")
        original_path = os.path.join(self.first,"original")

        text, names, n_s = self.get_text(text_path)
        ent_slice = self.get_entity_and_slice(original_path)

        len_dataset = len(list(os.listdir(text_path)))
        entity_dict = self.make_entity_dictionary(ent_slice, len_dataset)
        number = 0
        for i in list(entity_dict):
            df = df.append({'filename': names[i], 'text': text[i], 'sentences': n_s[i], 'entities': entity_dict[i]},
                           ignore_index=True)

        rkf = KFold(n_splits=self.folds)

        n_fold = 0
        if not os.path.exists(self.output):
            os.mkdir(self.output)
        for i_train, i_test in rkf.split(df):
            os.mkdir(os.path.join(self.output, str(n_fold // 10) + str(n_fold)))
            fold_path = os.path.join(self.output, str(n_fold // 10) + str(n_fold))
            train = df.iloc[i_train]
            test = df.iloc[i_test]
            train.to_json(os.path.join(fold_path, "train.json"), orient='table')
            test.to_json(os.path.join(fold_path, "test.json"), orient='table')
            n_fold += 1

