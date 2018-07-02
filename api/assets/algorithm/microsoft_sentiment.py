import requests 
import numpy as np
import csv
import os
import sys 
import pandas as pd
from api_cred import Credentials

sys.path.append(os.path.realpath('../api'))
from utils import turing_box

def run_azure(input_array):
        creds = Credentials().get('azure')
        headers = { 'Ocp-Apim-Subscription-Key' : creds['subscription_key'] }
        sentiment_api_url =  creds['endpoint'] + "sentiment"
        docs = []
        assert(len(input_array.flatten()) <= 1000)
        for i, input_text in enumerate(input_array.flatten()):
            docs.append({'id' : str(i+1), 'language' : 'en', 'text' : input_text})
        documents = { 'documents' : docs }
        response = requests.post(sentiment_api_url, headers=headers, json=documents)
        sentiments = response.json()
        print(sentiments)
        scores = [x['score'] for x in sentiments['documents']]
        scores = np.array(scores)
        print(scores)
        return scores.reshape(input_array.shape[0], 1)

def call(path_to_data): 
    df = pd.read_csv(path_to_data, header=0)
    df['Y_pred'] = [0 for i in range(0,df.shape[0])]
    for index,row in df.iterrows():
        try:
            df.loc[index, 'Y_pred'] = run_azure(np.asarray([row['X']]))[0]

        except Exception as e:
            print("Microsft sentiment unsuccessful: ", e)
            df.loc[index, 'Y_pred'] = np.nan
        break
    return df

if __name__ == "__main__": 
    turing_box(call, sys.argv)