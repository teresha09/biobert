import json
import os


class Result_brat:

    def __init__(self,data,out,entity):
        self.data = os.path.join(data, "test.json")
        self.out = os.path.join(out,"NER_result_conll.txt")
        self.conll = os.path.join(data, "test.conll")
        self.entity = entity
        self.brat_folder = os.path.join(out,"brat_result")

    def annotation_builder(self, output_string, out_file):
        words = output_string.split("\n")
        in_flag = False
        entity_counter = 0
        start = 0
        end = 0
        s1 = ""
        ann_file = open(out_file, "w+")
        for word in words:
            if word == '':
                continue
            if word.split(" ")[2] == "B-MISC":
                if in_flag:
                    ann_file.write("{}{}\t{}\n".format(s, end, s1[:-1]))
                    s = ""
                    s1 = ""
                in_flag = True
                entity_counter += 1
                start = word.split(" ")[-2]
                s = "T{}\t{} {} ".format(entity_counter, self.entity, start)
            if word.split(" ")[2] == "O-MISC" and in_flag:
                ann_file.write("{}{}\t{}\n".format(s, end, s1[:-1]))
                in_flag = False
                s = ""
                s1 = ""
            if in_flag:
                end = word.split(" ")[-1]
                s1 += word.split(" ")[0] + " "
        ann_file.close()
    def get_brat_folder(self):
        f = open(self.data)
        js_data = json.load(f)
        del js_data['schema']
        js_data = js_data['data']
        i = 0
        token_counter = 0
        output = open(self.out)
        conll = open(self.conll)
        review_string = ""
        conll_list = conll.readlines()
        output_list = output.readlines()
        index = 0
        index1 = 0
        os.mkdir(self.brat_folder)
        while index < len(output_list) and index1 < len(conll_list):
            if output_list[index] == '\n' and conll_list[index1] == '\n':
                index += 1
                index1 += 1
                continue
            if output_list[index] == '\n' and conll_list[index1] != '\n':
                index += 1
                continue
            if output_list[index] != '\n' and conll_list[index1] == '\n':
                index1 += 1
                continue
            if conll_list[index1] != '\n' and output_list[index] != '\n':
                token_counter += 1
                line1_list = conll_list[index1].split("\t")
                review_string += output_list[index][:-1] + " " + line1_list[4] + " " + line1_list[5] + "\n"
                index += 1
                index1 += 1
            if token_counter == js_data[i]['n_token'] or js_data[i]['n_token'] == 0:
                token_counter = 0
                out_file = os.path.join(self.brat_folder, js_data[i]['filename'])
                self.annotation_builder(review_string, out_file)
                review_string = ""
                i += 1
        if review_string != "":
            out_file = os.path.join(self.brat_folder, js_data[i]['filename'])
            self.annotation_builder(review_string, out_file)
