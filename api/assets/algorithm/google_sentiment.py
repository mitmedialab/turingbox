import requests 
import numpy as np
import csv
import os
import pandas as pd
import sys 

from google.cloud import language
from google.cloud.language import types
from google.cloud.language import enums

sys.path.append(os.path.realpath('../api'))
from utils import turing_box

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/js/fairnlp.json"

def run_google_sentiment(input_array): 
    # Instantiates a client
    client = language.LanguageServiceClient()

    result_arr = [] 
    # The text to analyze
    for twt in input_array: 
        document = types.Document(
            content=twt,
            type=enums.Document.Type.PLAIN_TEXT)

        # Detects the sentiment of the text
        try: 
            sentiment = client.analyze_sentiment(document=document).document_sentiment
            print('Text: {}'.format(twt))
            print('Sentiment: {}, {}'.format(sentiment.score, sentiment.magnitude))
            result_arr.append([sentiment.score, sentiment.magnitude])
        except: 
            print(twt)
            result_arr.append([0, 0])

    return result_arr


def call(path_to_data): 
    df = pd.read_csv(path_to_data, header=0, names=['X', 'Z', 'Y_true'])
    df['Y_pred'] = [0 for i in range(0,df.shape[0])]
    for index,row in df.iterrows():
        try:
            df.loc[index, 'Y_pred'] = run_google_sentiment(np.asarray([row['X']]))[0][0]

        except Exception as e:
            print("Google sentiment unsuccessful: ", e)
            df.loc[index, 'Y_pred'] = np.nan
        break
    return df

if __name__ == "__main__": 
    turing_box(call, sys.argv)