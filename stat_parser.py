#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import nltk
from collections import defaultdict
import re
from pycorenlp import StanfordCoreNLP
import pickle
import os
from nltk.tree import Tree
from nltk.draw.tree import TreeViewstat_
import numpy

input = sys.argv[1]
output = sys.argv[2]
corenlp = StanfordCoreNLP('http://localhost:9000')

with open(input) as infile:
    relation = defaultdict(list)

    for line in infile:
        e1, r, e2 = line.split(', ')
        relation[(e1, r)].append(e2)

    for (en1, rel), entity_list in relation.items():
        parse_tree_prob = defaultdict(int)
        rulesets = defaultdict(list)
        lhs_freq = defaultdict(int)
        rule_freq = defaultdict(lambda: defaultdict(int))
        svo_gram = defaultdict(str)

        for e in entity_list:
            line = str(en1 + rel + e)
            output = corenlp.annotate(line, properties={
                'annotators': 'tokenize,ssplit,pos,depparse,parse',
                'outputFormat': 'json'
            })

            parsed = output['sentences'][0]['parse']
            t = Tree.fromstring(str(parsed))
            grammar = t.productions()
            svo_gram[grammar] += line
            rulesets[(en1, rel)].append(grammar)
            for g in grammar:
                lhs = g.lhs()
                rhs = g.rhs()
                lhs_freq[lhs] += 1
                rule_freq[g][lhs] += 1

        # print(rule_freq)
        for (ent1, r), gram in rulesets.items():
            best = 0

            for gr in gram:
                best_gram = str()
                rp = []
                for rule in gr:
                    count_rule = sum(rule_freq[rule].values())
                    for rul in rule_freq:
                        for lh in rule_freq[rul]:
                            print(lh)
                            count_lhs = lhs_freq[lh]
                            print(count_lhs)
                            rule_prob = count_rule / count_lhs
                            rp.append(rule_prob)

                result = numpy.prod(rp)
                if result > best:
                    best = result
                    best_gram = gr

    # for sent, analysis in parsed.items():
    #     t = Tree.fromstring(str(analysis))
    #     grammar = t.productions()
    # for g in grammar:
    #     print(g.lhs())
    #     print(g.rhs())

    # t.draw()
    # for s in t.subtrees(lambda t: t.height() == 2):
    #     print(s)
    #     # # TreeView(t)._cframe.print_to_file('output.ps')
    #     # # os.system('convert output.ps output.png')
    #     print(analysis.split())
    #     for i in analysis.split():
    #        word = tuple()



