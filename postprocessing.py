#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
from collections import defaultdict
import nltk
from nltk import word_tokenize

input = sys.argv[1]
cleaned = sys.argv[2]


# remove possible triplets duplication created from stanford OpenIE
def remove_duplicates():
    triplets = defaultdict(int)
    with open(cleaned, 'w') as output:
        with open(input, 'r') as infile:

            for line in infile:
                tp1, ent1, rel, tp2, ent2 = line.split(',')
                triplets[(ent1, rel, ent2)] += 1

            for e1, r, e2 in triplets:
                output.write(e1 + ',')
                output.write(r + ',')
                output.write(e2)


# put cleaned triplets into seed file
def add_seed_triplets(input, output):
    seed = defaultdict(list)
    with open(output, 'w') as op:
        with open(input, 'r')as inp:
            for line in inp:
                ent1, rel, ent2 = line.split(',')
                seed[ent1].append((rel, ent2))

        for s, comb_list in seed.items():
            for tup in comb_list:
                rel = tup[0]
                e2 = tup[1]
                op.write(s + ',')
                op.write(rel + ',')
                op.write(e2)


# remove grammatically incorrect relations
def scan_relation():
    result = defaultdict(int)

    with open(cleaned, 'w') as op:
        with open(input, 'r') as ip:
            for line in ip:
                _, rel, e2 = line.split(',')
                verbs = ['MD', 'VB', 'VBD', 'VBP', 'VBZ']
                pp = ['VBG', 'VBN', 'IN']

                rel_to_tag = word_tokenize(rel)
                rel_tagged = nltk.pos_tag(rel_to_tag)
                rel_tagged_list = []
                for r in rel_tagged:
                    rel_tagged_list.append(r[1])

                for t in range(len(rel_tagged_list) - 1):

                    pos = rel_tagged_list[t]
                    followed = rel_tagged_list[t + 1]
                    if pos in verbs:
                        result[line] += 1
                    if pos == 'VBZ' and followed in pp:
                        result[line] += 1

                obj_to_tag = word_tokenize(e2)
                obj_tagged = nltk.pos_tag(obj_to_tag)
                obj_tagged_list = []

                for o in obj_tagged:
                    obj_tagged_list.append(o[1])

                for i in range(len(obj_tagged_list) - 1):
                    obj_pos = obj_tagged_list[i]
                    followed = obj_tagged_list[i:]

                    incorrect = ['VB', 'VBD', 'VBP', 'VBG', 'VBN', 'MD', 'VBZ']
                    if obj_pos not in incorrect and followed != 'WDT':
                        result[line] += 1

        for r in result:
            op.write(r)


scan_relation()
