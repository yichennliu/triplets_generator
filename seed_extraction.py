import nltk
from nltk.corpus import wordnet

synonyms = []
antonyms = []

verb_list =[ 'reap','magnified','help','use', 'produce', 'manifacture']

for w in verb_list:
    for syn in wordnet.synsets(w):
        for l in syn.lemmas():
            synonyms.append(l.name())
        print(set(synonyms))
