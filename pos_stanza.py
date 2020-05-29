#!/usr/bin/python3
# -*- coding: utf-8 -*-
import stanza
import sys


raw_file = "/home/yibsimo/PycharmProjects/Rokin_Dev/10_articles"
nlp = stanza.Pipeline(lang='en', processors='tokenize,pos')
text = open(raw_file,'r').readlines()
with open("pos_stanza", 'w') as file:
    for line in text:
        doc = nlp(line)
        for sent in doc.sentences:
            for word in sent.words:
                file.write('word:'+word.text+'\t'+ 'upos:'+word.upos+'\t')
                file.write('\n')