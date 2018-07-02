import requests 
import numpy as np
import csv
import os
import pandas as pd
import sys 
from textblob import TextBlob

sys.path.append(os.path.realpath('../api'))
from utils import turing_box

def run_textblob(input_array): 
    result_arr = []
    for r in input_array: 
        blob = TextBlob(r)
        result_arr.append([blob.sentiment.polarity, blob.sentiment.subjectivity])
    return result_arr

def call(path_to_data): 
    df = pd.read_csv(path_to_data, header=0)
    df['Y_pred'] = [0 for i in range(0,df.shape[0])]
    for index,row in df.iterrows():
        try:
            df.loc[index, 'Y_pred'] = run_textblob(np.asarray([row['X']]))[0][0]

        except Exception as e:
            print("Textblob sentiment unsuccessful: ", e)
            df.loc[index, 'Y_pred'] = np.nan
        break
    return df

if __name__ == "__main__": 
    turing_box(call, sys.argv)
