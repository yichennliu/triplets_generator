import random
import shutil
from math import floor

de_data = ["../../../news_tok_lcased.de", "../../../europarl-v9-tok-lc.de"]
en_data = ["../../../news_tok_lcased.en", "../../../europarl-v9-tok-lc.en"]


fr_gen_data = ["../../Dataset/SH_gen_fr_tok_lc.txt", "../../Dataset/news_tok_lcased.fr",
               "../../Dataset/europarl-v7-tok-lc.fr", "../../Dataset/tok_lcased.nc.fr"]
en_med_data = ["../../Dataset/SH_med_en_tok_lc.txt", "../../Dataset/medical_en_tok_lc.txt"]
de_med_data = ["../../Dataset/SH_med_de_tok_lc.txt", "../../Dataset/medical_de_tok_lc.txt"]
fr_med_data = ["../../Dataset/SH_med_fr_tok_lc.txt", "../../Dataset/medical_fr_tok_lc.txt"]




# split the dataset into 70% train set and 30% test set
def split_dataset(data):
    random.shuffle(data)
    split_id = floor(len(data) * 0.7)
    training = data[:split_id]
    testing = data[split_id:]
    return training, testing


# build the dataset
def extract_files(final_data, shuffle_op):
    with open(shuffle_op, 'wb') as shuf:
        for f in final_data:
            with open(f, 'rb') as input:
                shutil.copyfileobj(input, shuf)



if __name__ == '__main__':

    en_train_no_share, en_noshare_test = split_dataset(en_data)
    de_train_no_share, de_noshare_test = split_dataset(de_data)
    extract_files(en_train_no_share, "../../shuffle-en-train-NOS")
    extract_files(en_noshare_test, "../../shuffle-en-test-NOS")
    extract_files(de_train_no_share, "../../shuffle-de-train-NOS")
    extract_files(de_noshare_test, "../../shuffle-de-test-NOS")
