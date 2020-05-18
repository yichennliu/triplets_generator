#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import ijson
import re
import shutil
import random
from math import floor
from collections import Counter
from nltk.corpus import stopwords


json_file = sys.argv[1]
out_file = sys.argv[2]
number_of_articles = int(sys.argv[3])



def split_dataset(data):
    random.shuffle(data)
    split_id = floor(len(data) * 0.7)
    training = data[:split_id]
    testing = data[split_id:]
    return training, testing


# remove digits, punctuation, and stopwords
def remove_digit_punct_stopword(infile, outfile, lang):
    set_stopword = set(stopwords.words(lang))
    with open(outfile, 'w', encoding='UTF8') as f:
        for line in open(infile, 'r', encoding='UTF8'):
            # split into words
            extract_words = line.split()
            for word in extract_words:
                filtered_word = re.sub('[^a-zöäüßA-ZÖÄÜ\s]', '', word)
                if not filtered_word in set_stopword:
                     if not filtered_word.isdigit():
                        f.writelines(filtered_word + "\n")


def extract_most_frequent(infile, outfile):
    with open(outfile, 'w', encoding= 'UTF8') as file:
        with open(infile, "r", encoding= 'UTF8') as input:
            count = Counter(line for line in input)
            for word in count.most_common(2000):
                file.writelines(word[0] + "\n")



with open(out_file, 'w' , encoding= 'UTF-8') as output:
    with open(json_file, 'r', encoding= 'UTF-8') as f:
        objects = ijson.items(f, '2')
        columns = list(objects)
        article_collection = columns[0].values()
        for count in range(number_of_articles+1):
            for i in article_collection:
                output.write(i)