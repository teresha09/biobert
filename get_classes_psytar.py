import csv
import os
import json

def get_class(text,entity,filename):
    f = open(os.path.join("data","{}.csv".format(entity)))
    csv_reader = csv.reader(f, delimiter=',')
    for row in csv_reader:
        if row[1] == filename and text == row[3]:
            return row[18]
    return ''