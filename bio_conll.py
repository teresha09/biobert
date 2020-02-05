import os
import shutil


class BIO_conll:

    def __init__(self,fold_path,bio_path):
        self.fold_path = fold_path
        self.bio_path = bio_path

    def to_IOB_format(self, filename, out_file):
        f = open(filename, 'r')
        f1 = open(out_file, 'a+')
        for line in f.readlines():
            tokens = line.split("\t")
            if line == '\n':
                f1.write('\n')
                continue
            if len(tokens) < 3:
                continue
            if tokens[3] == '0':
                tokens[3] = 'O'
            f1.write(u'{}\t{}\n'.format(tokens[0], tokens[3][0]))
        f.close()
        f1.close()

    def get_bio(self):
        if not os.path.exists(self.bio_path):
            os.mkdir(self.bio_path)
        for directory in os.listdir(self.fold_path):
            fold_path = os.path.join(self.fold_path,directory)
            bio_fold_path = os.path.join(self.bio_path,directory)
            if not os.path.exists(bio_fold_path):
                os.mkdir(bio_fold_path)
            train = os.path.join(fold_path, "train.conll")
            train_bio = os.path.join(bio_fold_path, "train.tsv")
            self.to_IOB_format(train,train_bio)
            shutil.copyfile(train_bio, os.path.join(bio_fold_path, "train_dev.tsv"))
            test = os.path.join(fold_path, "test.conll")
            test_bio = os.path.join(bio_fold_path, "test.tsv")
            self.to_IOB_format(test,test_bio)
            shutil.copyfile(test_bio, os.path.join(bio_fold_path, "devel.tsv"))