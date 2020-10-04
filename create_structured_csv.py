#!/usr/bin/python3
# -*- coding: utf-8 -*-
import glob
import os
import pickle
import pandas as pd


def main():
    # create a list of pickle file names
    print("start")
    pickles = []
    for file in glob.glob(os.getcwd() + "/data/output/output_ner/qc_ner_87_articles.pickle"):
        pickles.append(file)
    print("processing")
    # load each pickle file and create the resultant csv file
    for file in pickles:
        with open(file, 'rb') as f:
            entities = pickle.load(f)

        # add all the names in entity set
        entity_set = set(entities.keys())
        final_list = []
        curr_dir = os.getcwd()
        file_name_list = file.split('/')[-1].split('.')[0].split('_')[2:]
        file_name = file_name_list[0]
        flag = True
        for str in file_name_list[1:]:
            file_name += '_'
            file_name += str
            print(file_name)


        df = pd.read_csv(os.getcwd() + "/data/output/output_openIE/qc_87_articles-out.csv", error_bad_lines=False)

        # parse every row present in the intermediate csv file
        triplet = set()
        for i, j in df.iterrows():
            j[0] = j[0].strip()
            # if entity is present in entity set, only then parse further
            if j[0] in entity_set:
                added = False
                e2_sentence = j[2].split(' ')
                # check every word in entity2, and add a new row triplet if it is present in entity2
                for entity in e2_sentence:
                    if entity in entity_set:
                        _ = (entities[j[0]], j[0], j[1], entities[entity], j[2])
                        triplet.add(_)
                        added = True
                if not added:
                    _ = (entities[j[0]], j[0], j[1], 'O', j[2])
                    triplet.add(_)
        # convert the pandas dataframe into csv
        processed_pd = pd.DataFrame(list(triplet), columns=['Type', 'Entity 1', 'Relationship', 'Type', 'Entity2'])
        processed_pd.to_csv("./data/output/output_trip_with_ner/" + file.split("/")[-1].split(".")[0] + '.csv',
                            encoding='utf-8', index=False)

        print("Processed " + file.split("/")[-1])

    print("Files processed and saved")


if __name__ == '__main__':
    main()
