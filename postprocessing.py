#!/usr/bin/python3
# -*- coding: utf-8 -*-
import csv
import glob
import json
import os
import sys
from collections import defaultdict
from nltk import word_tokenize, pos_tag

keyword_list = open(sys.argv[1], 'r')  # json file of keywords
keywords = json.load(keyword_list)


def remove_type_labels(input):
    triplets = defaultdict(int)

    reader = csv.reader(input, delimiter=",")
    next(reader, None)
    for line in reader:
        # print(line)
        if len(line) == 5:
            type1 = line[0]
            ent1 = line[1].strip()
            rel = line[2].strip()
            type2 = line[3]
            ent2 = line[4].strip()
            triplets[(ent1, rel, ent2)] += 1

        if len(line) == 3:
            ent1 = line[0].strip()
            rel = line[1].strip()
            ent2 = line[2].strip()

            triplets[(ent1, rel, ent2)] += 1

    return triplets


def pos_tagging(elem):
    elem_to_tag = word_tokenize(elem)
    elem_tagged = pos_tag(elem_to_tag)
    tagged_list = []

    for e in elem_tagged:
        tagged_list.append(e[1])

    return tagged_list


# remove grammatically incorrect triplets
def check_grammar(triplets):
    e1_result = defaultdict(int)
    rel_result = defaultdict(int)
    final_result = defaultdict(int)

    verbs = ['MD', 'VB', 'VBD', 'VBP', 'VBZ']
    pp = ['VBG', 'VBN']
    prep = ['IN']
    adverb = ['RB', 'RBR', 'RBS', 'JJ']
    pronouns = ['PRP', 'PRP$', 'DT']
    nouns = ['NN', 'NNS', 'NNP', 'NNPS']

    for elem in triplets:

        (e1, rel, e2) = elem
        e1_tagged_list = pos_tagging(e1)

        if e1_tagged_list[0] not in pronouns and verbs and pronouns and adverb and pp and prep:
            e1_result[(e1, rel, e2)] += 1

    for trip in e1_result:

        (subj, relation, object) = trip
        rel_tagged_list = pos_tagging(relation)

        for t in range(0, len(rel_tagged_list) - 1):

            pos = rel_tagged_list[t]
            n_1 = rel_tagged_list[t - 1]
            followed = rel_tagged_list[t + 1]

            if pos in verbs and n_1 not in adverb:
                rel_result[(subj, relation, object)] += 1

            if pos == 'VBZ' or 'VBN' and n_1 in verbs:
                rel_result[(subj, relation, object)] += 1

            if pos == 'VBZ' or 'VBD' and followed in pp:
                rel_result[(subj, relation, object)] += 1

    for obj in rel_result:

        (s, v, o) = obj
        e2_tagged_list = pos_tagging(o)

        for i in range(0, len(e2_tagged_list) - 1):
            obj_pos = e2_tagged_list[i]
            followed = e2_tagged_list[i + 1]
            last_pos = e2_tagged_list[-1]

            incorrect = ['VB', 'VBD', 'VBP', 'VBG', 'VBN', 'MD', 'VBZ', 'WDT', 'IN']
            if obj_pos and followed and last_pos not in incorrect:
                final_result[(s, v, o)] += 1

    return final_result


# filter out the triplets that do not have certain keywords
def match_keyword(result, keywords):
    words = defaultdict(int)
    matching_e1 = defaultdict(int)
    matching_e2 = defaultdict(int)
    combined_matching = defaultdict(int)  # triplets that have keywords both in subject and object

    for articles in keywords:
        for a in articles:
            words[a] += 1

    for word in words:

        if len(word) > 1:
            w = word.split()
            for (e1, r, e2) in result:
                m1 = all([k in e1 for k in w])
                m2 = all([voc in e2 for voc in w])
                if m1 == True:
                    matching_e1[(e1, r, e2)] += 1
                if m2 == True:
                    matching_e2[(e1, r, e2)] += 1

        else:

            for (e1, r, e2) in result:
                m1 = all([k in e1 for k in word])
                m2 = all([voc in e2 for voc in word])
                if m1 == True:
                    matching_e1[(e1, r, e2)] += 1
                if m2 == True:
                    matching_e2[(e1, r, e2)] += 1

    matching_set1 = set(matching_e1)
    matching_set2 = set(matching_e2)

    for trip in matching_set1.intersection(matching_set2):
        combined_matching[trip] += matching_e2[trip]

    return combined_matching


def create_files(infile, result):
    output_path = "./data/output/postprocessed/"
    op_filename = output_path + "postp_" + infile.split('/')[-1].split('.')[0] + ".csv"
    with open(op_filename, "w") as op:
        for postp in result:
            ent1, rel, ent2 = postp
            op.write(ent1 + ',')
            op.write(rel + ',')
            op.write(ent2 + '\n')


if __name__ == "__main__":

    csv_files = []
    for cs_file in glob.glob(os.getcwd() + "/data/output/output_trip_with_ner/*.csv"):
        csv_files.append(cs_file)

    for cs_file in csv_files:
        with open(cs_file, 'r') as ip:
            original = remove_type_labels(ip)
            filtered_1 = check_grammar(original)
            filtered_2 = match_keyword(filtered_1, keywords)
            create_files(cs_file, filtered_2)
