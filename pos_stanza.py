#!/usr/bin/python3
# -*- coding: utf-8 -*-
import stanza
import sys



nlp = stanza.Pipeline('en', processors='tokenize, pos', use_gpu=False, pos_batch_size=3000) # Build the pipeline, specify part-of-speech processor's batch size
# raw_file = open(sys.argv[1], 'r', encoding= 'UTF-8')
# output_tagged = sys.argv[2]
raw_file = open("/home/yibsimo/PycharmProjects/Rokin_Dev/10_articles", 'r')

content = raw_file.readlines()
with open("10_articles_tagged", 'w', encoding='UTF-8') as out_file:
    for line in content:
        doc = nlp(line)
        for sent in doc.sentences:
            for word in sent.words:
                out_file.write("Word:"+ word.text+"\t"+ "upos:"+ word.upos+"\t")
                if word.feats:
                    out_file.write(word.feats)
                else:
                    out_file.write("_")

                out_file.write("\n")




