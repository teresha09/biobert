import csv
import os

import pandas as pd
from sklearn.model_selection import KFold

import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--psytar', '-psytar', type=str, default='data/psytar_folds')
parser.add_argument('--psytar_text', '-psytar_text', type=str, default='data/Copy_of_PsyTAR_dataset.csv')
parser.add_argument('--psytar_adr', '-psytar_adr', type=str, default='data/Copy_of_PsyTAR_dataset_adr.csv')
parser.add_argument('--psytar_disease', '-psytar_disease', type=str, default='data/Copy_of_PsyTAR_dataset_disease.csv')
parser.add_argument('--psytar_symptoms', '-psytar_symptoms', type=str, default='data/Copy_of_PsyTAR_dataset_symptoms.csv')
parser.add_argument('--folds', '-folds', type=int, default=5)
args = parser.parse_args()


folds_path = args.psytar
text_path = args.psytar_text
adr_path = args.psytar_adr
disease_path = args.psytar_disease
symptom_path = args.psytar_symptoms
n_folds = args.folds


def get_text(filename):
    text = {}
    n_sen = {}
    f = open(filename)
    csv_reader = csv.reader(f, delimiter=',')
    line = 0
    for row in csv_reader:
        if line == 0:
            line += 1
            continue
        else:
            if row[2] in text:
                text[row[2]] += row[4] + "\n"
            else:
                text[row[2]] = row[4] + "\n"
            if row[2] in n_sen:
                n_sen[row[2]] += 1
            else:
                n_sen[row[2]] = 1

    f.close()
    return text, n_sen


def get_adr_entity(filename, full_text):
    f = open(filename)
    text = {}
    csv_reader = csv.reader(f, delimiter=',')
    line = 0
    s = 0
    for row in csv_reader:
        if line == 0:
            line += 1
            continue
        else:
            for col in row[4:]:
                col = col.lower()
                if col == '':
                    break
                length = len(col)
                copy_col = col
                copy_col1 =col
                full_text[row[1]].lower().replace("\n",'')
                while len(copy_col) > 0:
                    start = full_text[row[1]].find(copy_col)
                    if start == -1:
                        if copy_col.rfind(" ") == -1:
                            break
                        copy_col = copy_col[:copy_col.rfind(" ")]
                    else:
                        break
                while len(copy_col1) > 0:
                    end = full_text[row[1]].find(copy_col1)
                    if end == -1:
                        if copy_col1.find(" ") == -1:
                            break
                        copy_col1 = copy_col1[copy_col1.find(" ")+1:]
                    else:
                        break
                if start == -1 or end == -1:
                    continue
                end = end + len(copy_col1)
                if row[1] in text:
                    text[row[1]].append({'start': start, 'end': end, 'entity': 'adr', 'text': col})
                else:
                    text[row[1]] = [{'start': start, 'end': end, 'entity': 'adr', 'text': col}]
    return text


def get_disease_entity(filename, full_text):
    f = open(filename)
    text = {}
    csv_reader = csv.reader(f, delimiter=',')
    line = 0
    s = 0
    for row in csv_reader:
        if line == 0:
            line += 1
            continue
        else:
            for col in row[4:]:
                col = col.lower()
                if col == '':
                    break
                length = len(col)
                copy_col = col
                copy_col1 = col
                full_text[row[1]].lower().replace("\n", '')
                while len(copy_col) > 0:
                    start = full_text[row[1]].find(copy_col)
                    if start == -1:
                        if copy_col.rfind(" ") == -1:
                            break
                        copy_col = copy_col[:copy_col.rfind(" ")]
                    else:
                        break
                while len(copy_col1) > 0:
                    end = full_text[row[1]].find(copy_col1)
                    if end == -1:
                        if copy_col1.find(" ") == -1:
                            break
                        copy_col1 = copy_col1[copy_col1.find(" ") + 1:]
                    else:
                        break
                if start == -1 or end == -1:
                    continue
                end = end + len(copy_col1)
                if row[1] in text:
                    text[row[1]].append({'start': start, 'end': end, 'entity': 'symptom', 'text': col.lower()})
                else:
                    text[row[1]] = [{'start': start, 'end': end, 'entity': 'symptom', 'text': col.lower()}]
    return text


def get_symptom_entity(filename, full_text):
    f = open(filename)
    text = {}
    csv_reader = csv.reader(f, delimiter=',')
    line = 0
    s = 0
    for row in csv_reader:
        if row[1] == "lexapro.43":
            print("debug")
        if line == 0:
            line += 1
            continue
        else:
            for col in row[4:]:
                col = col.lower()
                if col == '':
                    break
                length = len(col)
                copy_col = col
                copy_col1 = col
                full_text[row[1]].lower().replace("\n", '')
                while len(copy_col) > 0:
                    start = full_text[row[1]].find(copy_col)
                    if start == -1:
                        if copy_col.rfind(" ") == -1:
                            break
                        copy_col = copy_col[:copy_col.rfind(" ")]
                    else:
                        break
                while len(copy_col1) > 0:
                    end = full_text[row[1]].find(copy_col1)
                    if end == -1:
                        if copy_col1.find(" ") == -1:
                            break
                        copy_col1 = copy_col1[copy_col1.find(" ") + 1:]
                    else:
                        break
                if start == -1 or end == -1:
                    continue
                end = end + len(copy_col1)
                if row[1] in text:
                    text[row[1]].append({'start': start, 'end': end, 'entity': 'SSI', 'text': col.lower()})
                else:
                    text[row[1]] = [{'start': start, 'end': end, 'entity': 'SSI', 'text': col.lower()}]
    return text


def make_entity_dict(text, adr, disease, symtom):
    result = {}
    for key in text:
        d = {}
        i = 0
        if adr.get(key) is not None:
            for j in range(len(adr[key])):
                d[i] = adr[key][j]
                i += 1
        if disease.get(key) is not None:
            for j in range(len(disease[key])):
                d[i] = disease[key][j]
                i += 1
        if symtom.get(key) is not None:
            for j in range(len(symtom[key])):
                d[i] = symtom[key][j]
                i += 1
        result[key] = d
    return result


df = pd.DataFrame(columns=['filename', 'text', 'sentences', 'entities'])
text, n_sentences = get_text(text_path)
adr_entity = get_adr_entity(adr_path, text)
disease_entity = get_disease_entity(disease_path, text)
symptom_entity = get_symptom_entity(symptom_path, text)
entity_dict = make_entity_dict(text,adr_entity,disease_entity,symptom_entity)


for key in text:
    df = df.append({'filename':key,'text': text[key], 'sentences':n_sentences[key] , 'entities': entity_dict[key]}, ignore_index=True)


if not os.path.exists("data/psytar"):
    os.mkdir("data/psytar")
    os.mkdir("data/psytar/original")
    os.mkdir("data/psytar/text")
counter = 0
for row in df.iterrows():
    print(counter)
    t = open("data/psytar/text/{}.txt".format(row[1][0]), "a+")
    e = open("data/psytar/original/{}.ann".format(row[1][0]), "a+")
    t.write(row[1][1])
    t.close()
    ent = row[1][3]
    for i in ent:
        e.write("T{}\t{} {} {}\t{}\n".format(i,ent[i]['entity'], ent[i]['start'], ent[i]['end'], ent[i]['text']))
    e.close()
    counter += 1
