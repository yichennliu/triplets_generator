#!/usr/bin/python3
# -*- coding: utf-8 -*-
import csv
import sys
from collections import defaultdict

input_file = sys.argv[1]
amount = int(sys.argv[2])  # amount of triplets for word graph
output_path = "./data/triplets/"
output_node_file = sys.argv[3]
output_edge_file = sys.argv[4]


def extract_node(outfile, gephi_dict):
    header = ['Id', 'Label']
    with open(outfile, 'w') as output:
        writer = csv.writer(output, delimiter=',')
        writer.writerow(i for i in header)
        for ent in gephi_dict:
            for id, v in gephi_dict[ent].items():
                data = []
                data.append(id)
                data.append(ent)
                writer.writerow(d for d in data)


def extract_edge(outfile, src_tgt_rel, gephi_dict):
    with open(outfile, 'w') as output:
        writer = csv.writer(output, delimiter=',')
        header = ['Source', 'Target', 'Type', 'Relation']
        writer.writerow(i for i in header)

        for (src, tgt), rel in src_tgt_rel.items():
            for src_id, _ in gephi_dict[src].items():
                for tgt_id, _ in gephi_dict[tgt].items():
                    data = []
                    data.append(src_id)
                    data.append(tgt_id)
                    data.append("Directed")
                    data.append(rel)
                    writer.writerow(d for d in data)


ent_freq = defaultdict(int)
gephi_dict = defaultdict(lambda: defaultdict(int))
src_tgt_rel = defaultdict(str)

with open(input_file, 'r') as input:
    for count, line in enumerate(input, start=1):
        # for line in input:
        if count % amount == 0:
            break

        else:

            # visualize only the triplets that have words from query
            # query = ['scietists', 'researchers', 'physicists', 'ibm', 'google', 'technology']

            line = line.split(',')
            source = line[0].strip()
            target = line[2].strip()
            relation = line[1].strip()
            # if source or target in query:
            ent_freq[source] += 1
            ent_freq[target] += 1
            src_tgt_rel[(source, target)] = relation

for index, (elm, freq) in enumerate(ent_freq.items()):
    gephi_dict[elm][str(index)] += 1

if __name__ == '__main__':
    extract_node(output_path + output_node_file, gephi_dict)
    extract_edge(output_path + output_edge_file, src_tgt_rel, gephi_dict)
