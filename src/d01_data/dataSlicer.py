
import pandas as pd
import sys, os


def data_slicer(path_in,path_out):
    '''
    function to slice the whole data set to small chunk

    input :  string: path of input file
    output:  string: path of output file
    '''

    article_complete = pd.read_json(path_in)
    article_20 = article_complete.head(20)   # make this a parameter
    article_20.to_csv('path_out')


