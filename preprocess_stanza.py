#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pickle

import stanza

nlp = stanza.Pipeline('en', processors='tokenize,pos,ner', use_gpu=False,
                      pos_batch_size=3000)  # Build the pipeline, specify part-of-speech processor's batch size
# raw_file = open(sys.argv[1], 'r', encoding= 'UTF-8')
# output_tagged = sys.argv[2]
raw_file = open("/home/yibsimo/PycharmProjects/Rokin_Dev/data/Raw/10_articles", 'r')

content = raw_file.readlines()

ner_dict = {}

with open("10_articles_preprocessed", 'w', encoding='UTF-8') as out_file:
    for line in content:
        doc = nlp(line)
        for sent in doc.sentences:
            for word in sent.words:
                out_file.write("Word ID:" + str(
                    word.id) + "\t" + "Word:" + word.text + "\t" + "xpos:" + word.xpos + "\t" + word.upos + "\n")

                # if word.feats:
                #     out_file.write("feats:"+word.feats+"\t")
                # else:
                #     out_file.write("feats: _\t")

            #     out_file.write("Head ID:"+str(word.head)+"\t")
            #
            #     if word.head > 0:
            #         out_file.write("Head:"+sent.words[word.head-1].text+"\t")
            #     else:
            #         out_file.write("Head: root\t")
            #
            #     out_file.write("deprel:"+ word.deprel+"\n")

            for ent in sent.ents:
                out_file.write("Entity:" + ent.text + "\t" + ent.type + "\n")
                ner_dict[ent.text] = ent.type

output_path = "data/preprocessed/"
op_pickle_filename = output_path + "seed_named_entities" + ".pickle"
op_filename = output_path + "kg_text"

with open(op_pickle_filename, "wb") as f:
    pickle.dump(ner_dict, f)


def read_and_create(infile, outfile):
    with open(outfile, "w+") as output:
        with open(infile, "r") as f:
            lines = f.read().splitlines()
            doc = ""
            for line in lines:
                doc += line
            output.write(doc)


read_and_create("/home/yibsimo/PycharmProjects/Rokin_Dev/data/Raw/10_articles", op_filename)
