#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import subprocess
import glob
import shutil

def Stanford_Relation_Extractor():
    print('Relation Extraction Started')

    for f in glob.glob(os.getcwd() + '/data/raw/qc_87_articles.txt'):
        print("Extracting relations for " + f.split("/")[-1])
        current_directory = os.getcwd()
        os.chdir(current_directory + '/stanford-openie')

        p = subprocess.Popen(['./process_large_corpus.sh',f,f + '-out.csv'], stdout=subprocess.PIPE)

        output, err = p.communicate()

    print('Relation Extraction Completed')


def move_files():

    source_dir = './data/raw/'
    dst = './data/output/output_openIE/'
    files = glob.iglob(os.path.join(source_dir, '*.csv'))
    for file in files:
        if os.path.isfile(file):
            shutil.move(file, dst)



if __name__ == '__main__':
    Stanford_Relation_Extractor()
    move_files()

