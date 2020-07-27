#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
from collections import defaultdict

all_triplets = defaultdict(int)

file_1 = sys.argv[1]
file_2 = sys.argv[2]
output = sys.argv[3]


for n in sys.argv[1:3]:
    input = open(n, "r")
    op = open(output, "w")


    for line in input:
        en, rel, en1 = line.split(', ')
        all_triplets[(en,rel,en1)] += 1


    for t in all_triplets:
        e1, r, e2 = t
        op.write(e1+',')
        op.write(r+',')
        op.write(e2)






