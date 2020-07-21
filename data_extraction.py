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


# remove triplets duplication created from stanford OpenIE
def remove_duplicates(infile, outfile):
    with open(outfile, 'w') as output:
        with open(infile, 'r') as file:
            trip = defaultdict()
            for line in file:
                ent1, rel, ent2 = line.split(',')
                output.write(ent1 + ",")
                output.write(rel + ",")
                output.write(ent2)

                trip[line] = 1

            for triplet in trip:
                output.write(triplet)


# lower case all the text for relation OpenIE
def to_lower(infile, outfile):
    with open(outfile, 'w') as output:
        with open(infile, 'r') as inf:
            for line in inf:
                for word in line:
                    word = word.lower()
                    output.write(word)


with open(json_ouput, 'w') as output:
    with open(json_file, 'r') as f:
        objects = ijson.items(f, 'title')
        columns = list(objects)
        article_collection = columns[0].values()
        for count in range(number_of_articles + 1):
            for i in article_collection:
                output.write(i + "." + "\n")
