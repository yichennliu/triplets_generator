import nltk
from nltk.corpus import wordnet
from nltk import FreqDist
from collections import defaultdict
import csv
import sys

def extract_node(infile, outfile):
    ent = []
    with open(outfile, 'wt') as out:
        with open(infile, 'r') as input:
            for line in input:
                line = line.split(',')
                source = line[0]
                target = line[2]
                ent.append(source)
                ent.append(target)
            new_list = [(elm, str(index)) for index, elm in enumerate(ent)]
            header = ['Id', 'Label']
            writer = csv.writer(out, delimiter=',')
            writer.writerow(i for i in header)
            for tup in new_list:
                data =[]
                data.append(tup[1])
                data.append(tup[0])
                writer.writerow(d for d in data)

ent =[]
new_dict ={}
with open("/home/yibsimo/PycharmProjects/Rokin_Dev/data/preprocessed/quantum_titles-out.csv", 'r') as input:
    for line in input:
        line = line.split(',')
        source = line[0]
        target = line[2]
        ent.append(source)
        ent.append(target)
        new_list = [(elm, str(index)) for index, elm in enumerate(ent)]
        for tup in new_list:
            new_dict[tup[0]] = tup[1]

def extract_edge(infile, outfile):

    with open(outfile, 'wt') as out:
        with open(infile, 'r') as input:
            writer = csv.writer(out, delimiter=',')
            header = ['Source', 'Target', 'Type', 'Relation']
            writer.writerow(i for i in header)

            for line in input:
                data = []
                line = line.split(',')
                source = line[0]
                target = line[2]
                relation = line[1]
                data.append(new_dict[source])
                data.append(new_dict[target])
                data.append("Directed")
                data.append(relation)
                writer.writerow(d for d in data)

extract_edge("/home/yibsimo/PycharmProjects/Rokin_Dev/data/preprocessed/quantum_titles-out.csv", "qu_edge.csv")
