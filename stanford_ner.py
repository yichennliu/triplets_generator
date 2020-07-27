#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pickle
import sys
from nltk import sent_tokenize
from pycorenlp import StanfordCoreNLP

raw = sys.argv[1]

corenlp = StanfordCoreNLP('http://localhost:9000')
corenlp_properties = {
    'annotators': 'tokenize, lemma, ner, parse',
    'outputFormat': 'json'
}


def get_tagged_from_server(input_text):
    """
    Send the input_text to the CoreNLP server and retrieve the tokens, named entity tags and part-of-speech tags.
    """
    corenlp_output = corenlp.annotate(input_text, properties=corenlp_properties).get("sentences", [])[0]
    tagged = [(t['originalText'], t['ner']) for t in corenlp_output['tokens']]
    return tagged


ner_to_dict = {}

with open(raw, "r") as infile:
    text = str(infile.read())
    sentences = sent_tokenize(text)
    for s in sentences:
        end_tag = get_tagged_from_server(s)
        for tup in end_tag:
            print(tup)
            ner_to_dict[tup[0]] = tup[1]

output_path = "./data/output/"

op_pickle_filename = output_path + "named_entity_quantum_10_articles" + ".pickle"
with open(op_pickle_filename, "wb") as f:
    pickle.dump(ner_to_dict, f)
