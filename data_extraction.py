#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import ijson
from nltk import sent_tokenize

json_file = open(sys.argv[1], 'r')
output_path = "./data/raw/"
data_output = open(sys.argv[2], 'w')
number_of_articles = int(sys.argv[3])


# extract number of articles from json file and preprocess them with tokenization and lowercase
def load_json():
    objects = ijson.items(json_file, 'text')
    columns = list(objects)

    article_collection = columns[0].values()
    count = 0
    while count <= number_of_articles:
        for i in article_collection:
            for sent in sent_tokenize(i):
                sent = sent.lower()
                data_output.write(sent + '\n')
                count += 1


if __name__ == '__main__':
    load_json()
