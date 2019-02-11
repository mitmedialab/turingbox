import requests 
import numpy as np
import csv
import os
import pandas as pd
from textblob import TextBlob
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from api_cred import Credentials



from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/credientials.json"

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
        return scores.reshape(input_array.shape[0], 1)


def run_textblob(input_array): 
    result_arr = []
    for r in input_array: 
        blob = TextBlob(r)
        result_arr.append([blob.sentiment.polarity, blob.sentiment.subjectivity])
    return result_arr

def api_chunks(twt_list, n=1000):
    for i in range(0, len(twt_list), n): 
        yield twt_list[i:i+n]

def write_results(tweet_list, label_list, sensitive_attr, api_func, save_file, score_label): 
    with open(save_file, 'w') as f: 
        csv_writer = csv.writer(f)
        if len(score_label) == 1: 
            csv_writer.writerow(["text X", "Z", "label Y", score_label])
        else: 
            print(["text X", "Z", "label Y"] + score_label)
            csv_writer.writerow(["text X", "Z", "label Y"] + score_label)
        sentiment = [] 
        review_iter = api_chunks(tweet_list, 50)
        for sub_list in review_iter: 
            sentiment += list(api_func(np.array(sub_list)))

        for i, twt in enumerate(tweet_list): 
            if len(sentiment[i]) == 1: 
                csv_writer.writerow([twt, sensitive_attr[i], label_list[i], sentiment[i][0]])
            else: 
                csv_writer.writerow([twt, sensitive_attr[i], label_list[i]] + sentiment[i])

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


def run_custom_sentiment(input_array): 
    df = pd.read_csv('datasets/amazon_sentiment.csv')
    texts = df['text'].tolist() 
    labels = df['label'].tolist()
    vectorizer = CountVectorizer(stop_words='english', max_features=10000)
    train_features = vectorizer.fit_transform(texts[1000:9000])
    nb_model = MultinomialNB()
    nb_model.fit(train_features, labels[1000:9000])

    vocab = vectorizer.vocabulary_

    vectorizer = CountVectorizer(stop_words='english', vocabulary=vocab)
    test_features = vectorizer.fit_transform(input_array)
    predictions = nb_model.predict(test_features)
    prob = nb_model.predict_proba(test_features)
    predictions = nb_model.predict(test_features)

    class_prob = [[p[1]] for p in prob]
    return class_prob




if __name__ == "__main__": 

    reviews = [] 
    sensitive_attr = [] 
    labels = [] 
    dataset_str = 'movies'
    with open('datasets/' + dataset_str + '1000.csv', 'r') as f: 
        csv_reader = csv.reader(f)
        row = next(csv_reader)
        for row in csv_reader: 
            reviews.append(row[0])
            sensitive_attr.append(row[1])
            labels.append(row[2])

    #write_results(reviews, labels, sensitive_attr, run_azure, 'results/'+ dataset_str + '_azure_results.csv', ['sentiment'])
    
    #write_results(reviews, labels, sensitive_attr, run_textblob, 'results/'+ dataset_str + '_tb_results.csv', ['sentiment'])

    #write_results(reviews, labels, sensitive_attr, run_google_sentiment, 'results/'+ dataset_str + '_google_results.csv', ['sentiment', 'magnitude'])
