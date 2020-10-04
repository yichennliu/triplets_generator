#!/usr/bin/python3
# -*- coding: utf-8 -*-
import subprocess

print('Start')
subprocess.call(['', './data_extraction.py', './data/raw/json/quantum_with_text.json', 'qc_87_articles.txt', '87'],
                shell=True)
subprocess.call(['./stanford_ner.py'], shell=True)
subprocess.call(['./relation_extractor.py'], shell=True)
subprocess.call(['./create_structured_csv.py'], shell=True)
subprocess.call(['', './postprocessing.py', './data/raw/json/Quantum_bert2tag_keywords_30.json'], shell=True)

print('Process Completed')
