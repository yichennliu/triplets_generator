#!/usr/bin/python3
# -*- coding: utf-8 -*-
import random
import sys
from collections import defaultdict
from math import floor
import ijson

json_file = sys.argv[1]
json_ouput = sys.argv[2]
number_of_articles = int(sys.argv[3])


def split_dataset(data):
    random.shuffle(data)
    split_id = floor(len(data) * 0.7)
    training = data[:split_id]
    testing = data[split_id:]
    return training, testing

# lower case all the text for stanford OpenIE
def to_lower(infile, outfile):
    with open(outfile, 'w') as output:
        with open(infile, 'r') as inf:
            for line in inf:
                for word in line:
                    word = word.lower()
                    output.write(word)


with open(json_ouput, 'w') as output:
    with open(json_file, 'r') as f:
        objects = ijson.items(f, 'text')
        columns = list(objects)
        article_collection = columns[0].values()
        for count in range(number_of_articles + 1):
            for i in article_collection:
                output.write(i + "." + "\n")


to_lower("quantum_10_articles", "quantum_10_articles-lc")
