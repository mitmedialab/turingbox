import requests 
import numpy as np
import csv
import os

AZURE_SUBSCRIPTION_KEY = ""
AZURE_ENDPOINT = ""

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/js/fairnlp.json"

def run_azure(input_array):
        headers = { 'Ocp-Apim-Subscription-Key' : AZURE_SUBSCRIPTION_KEY }
        sentiment_api_url =  AZURE_ENDPOINT + "sentiment"
        docs = []
        assert(len(input_array.flatten()) < 1000)
        for i, input_text in enumerate(input_array.flatten()):
            docs.append({'id' : str(i+1), 'language' : 'en', 'text' : input_text})
        documents = { 'documents' : docs }
        response = requests.post(sentiment_api_url, headers=headers, json=documents)
        sentiments = response.json()
        print(sentiments)
        scores = [x['score'] for x in sentiments['documents']]
        scores = np.array(scores)
        return scores.reshape(input_array.shape)

def write_results(tweet_list, label_list, api_func, save_file, score_label): 
    with open(save_file, 'w') as f: 
        csv_writer = csv.writer(f)
        if len(score_label) == 1: 
            csv_writer.writerow(["text", "label", score_label])
        else: 
            print(["text", "label"] + score_label)
            csv_writer.writerow(["text", "label"] + score_label)
        sentiment = api_func(np.array(tweet_list))
        for i, twt in enumerate(tweet_list): 
            if len(sentiment[i]) == 1: 
                csv_writer.writerow([twt, label_list[i], sentiment[i]])
            else: 
                csv_writer.writerow([twt, label_list[i]] + sentiment[i])

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

if __name__ == "__main__": 

    tweets = [] 
    labels = [] 

    with open('datasets/amazon_sentiment100.csv', 'r') as f: 
        csv_reader = csv.reader(f)
        row = next(csv_reader)
        for row in csv_reader: 
            tweets.append(row[0])
            labels.append(row[1])
    # write_results(tweets, labels, run_azure, 'results/twitter_sentiment100_results.csv')
    write_results(tweets, labels, run_google_sentiment, 'results/amazon_sentiment100_google_results.csv', ['g_sentiment', 'g_magnitude'])

