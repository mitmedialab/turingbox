import requests 
import numpy as np

AZURE_SUBSCRIPTION_KEY = ""
AZURE_ENDPOINT = ""

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

def write_results(tweet_list, label_list, api_func, save_file): 
    with open(save_file, 'w') as f: 
        csv_writer = csv.writer(f)
        csv_writer.writerow(["text", "label", str(api_func)])
        sentiment = api_func(np.array(tweet_list))
        for i, twt in enumerate(tweet_list): 
            csv_writer.writerow([twt, label_list[i], sentiment[i]])


if __name__ == "__main__": 

    tweets = [] 
    labels = [] 

    with open('datasets/twitter_sentiment100.csv', 'r') as f: 
        csv_reader = csv.reader(f)
        row = next(csv_reader)
        for row in csv_reader: 
            tweets.append(row[0])
            labels.append(row[1])

    write_results(tweets, labels, run_azure, 'results/twitter_sentiment100_results.csv')