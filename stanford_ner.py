#!/usr/bin/python3
# -*- coding: utf-8 -*-
import glob
import os
import pickle
from nltk import sent_tokenize
from pycorenlp import StanfordCoreNLP


corenlp = StanfordCoreNLP('http://localhost:9000')
corenlp_properties = {
    'annotators': 'tokenize, lemma, depparse, ner',
    'outputFormat': 'json'
}


def get_tagged_from_server(input_text):
    """
    Send the input_text to the CoreNLP server and retrieve the tokens, named entity tags and part-of-speech tags.
    """
    corenlp_output = corenlp.annotate(input_text, properties=corenlp_properties).get("sentences", [])[0]
    tagged = [(t['originalText'], t['ner']) for t in corenlp_output['tokens']]
    return tagged


def create_pickle(infile, ner_dict):

    output_path = "./data/output/output_ner/"

    op_pickle_filename = output_path + "qc_ner_" + infile.split('/')[-1].split('.')[0] + ".pickle"
    with open(op_pickle_filename, "wb") as f:
        pickle.dump(ner_dict, f)


if __name__ == "__main__":

    ner_to_dict = {}
    raw_files = []
    for raw in glob.glob(os.getcwd() + "/data/raw/*.txt"):
        raw_files.append(raw)

    for rf in raw_files:
        with open(rf, 'r') as ip:
            text = str(ip.read())
            sentences = sent_tokenize(text)
            for s in sentences:
                end_tag = get_tagged_from_server(s)
                for tup in end_tag:
                    print(tup)
                    ner_to_dict[tup[0]] = tup[1]

            create_pickle(rf, ner_to_dict)


