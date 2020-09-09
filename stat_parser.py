#!/usr/bin/python3
# -*- coding: utf-8 -*-
import csv
import os
import sys
from collections import defaultdict
import numpy
from nltk.tree import Tree
from pycorenlp import StanfordCoreNLP

output_path = "./data/output/postprocessed/parsed/"
input = sys.argv[1]
output = output_path + sys.argv[2]

corenlp = StanfordCoreNLP('http://localhost:9000')
chosen = defaultdict(str)

with open(output, 'w') as op:

    relation = defaultdict(list)

    with open(input) as infile:
        reader = csv.reader(infile, delimiter=',')
        for row in reader:
            if (len(row) == 3):
                e1 = row[0]
                r = row[1]
                e2 = row[2]

                relation[(e1, r)].append(e2)

        for (en1, rel), entity_list in relation.items():
            rulesets = defaultdict(list)
            lhs_freq = defaultdict(int)
            rule_freq = defaultdict(lambda: defaultdict(int))
            svo_gram = defaultdict(lambda: defaultdict(str))

            # parse the duplicated triplets with stanford parser
            for e in entity_list:
                line = str(en1 + rel + e)
                output = corenlp.annotate(line, properties={
                    'annotators': 'tokenize,ssplit,pos,parse',
                    'outputFormat': 'json'
                })

                parsed = output['sentences'][0]['parse']
                t = Tree.fromstring(str(parsed))

                grammar = t.productions()

                # save the grammar rules into rulesets
                svo_gram[str(grammar).strip('[]')][line] = (en1, rel, e)
                rulesets[(en1, rel)].append(grammar)  # rulesets keys: subject and the relation as tuples
                # values: all possible grammars of the same tuples as a list
                for g in grammar:
                    lhs = g.lhs()
                    rhs = g.rhs()
                    lhs_freq[lhs] += 1  # calculate the frequency of left hand rules
                    rule_freq[g][lhs] += 1  # calculate the frequency of left hand rules under the certain grammar

            for (ent1, r), gram in rulesets.items():
                best = 0

                for gr in gram:
                    all_gram = defaultdict(
                        lambda: 0.0)  # initialize the dictionary to save the probibilities of each analysis
                    best_gram = str()
                    print(best_gram)
                    rp = []  # list for temporary saving of rule probabilities
                    for rule in gr:
                        count_rule = sum(rule_freq[rule].values())
                        for rul in rule_freq:
                            for lh in rule_freq[rul]:
                                print(lh)
                                count_lhs = lhs_freq[lh]
                                print(count_lhs)

                                rule_prob = count_rule / count_lhs
                                rp.append(rule_prob)

                    result = numpy.prod(rp)  # calculate the total probability of a grammar
                    all_gram[str(grammar).strip('[]')] += result
                    weight = result / sum(all_gram.values())

                    # calculate weights and reweighting
                    if weight > best:
                        weight = result
                        print(weight)
                        best_gram = str(gr).strip('[]')

                    # choose the sentence with the grammar that has the highest probability
                    for best_gram in svo_gram:
                        for candidate, tripl in svo_gram[best_gram].items():
                            (e1, r, e2) = tripl
                            print(candidate)
                            print(tripl)
                            chosen[(e1, r, e2)] += candidate

        for c, v in chosen.items():
            en1, r, en2 = c

            op.write(en1 + ",")
            op.write(r + ",")
            op.write(en2 + "\n")

