# File for preprocessing tweets 
import tokenizer
import re 
import pandas as pd

def process_tweet(raw_twt, lower=True): 
    t = re.sub(r"http\S+", "", raw_twt)
    t = re.sub(r"@\S+", "", t)
    t = re.sub(r"#\S+", "", t)
    t = re.sub(r"&amp;", "&", t)
    t = re.sub(r"&gt;;", ">", t)
    t = re.sub(r"&lt;;", "<", t)
    t = re.sub(r"’", "'", t) #replace weird apostrophy with normal one

    t = tokenizer.tokenize(t)
    if lower: 
        t = " ".join(t).lower()
        return t.split(" ")
    return t 

def extract_and_preprocess(filenames_list, encoding='utf-8'): 
    tweet_list = [] 
    for file in filenames_list: 
        df = pd.read_csv(file, encoding = encoding)
        text = df['tweet_text'].tolist()
        tweet_list += [process_tweet(t) for t in text if isinstance(t,str)]
    print("extraction completed. Length: ", len(tweet_list))
    return tweet_list

def extract_and_preprocess_n(filenames_list, n=100): 
    author_dict = {} 
    for fname in filenames_list: 
        df = pd.read_csv(fname)
        authors = list(set(df['user_screen_name']))
        for a in authors: 
            a_rows = df.loc[df['user_screen_name'] == a]
            text = a_rows['tweet_text'].tolist()
            if len(text) > n:
                text = text[:n]
                author_tweets = [process_tweet(t) for t in text]
                flat_list = [item for sublist in author_tweets for item in sublist]
                author_dict[a] = flat_list
    return author_dict.values() 

if __name__ == "__main__": 
    file_list = ["../datasets/raw/white_tweets.csv", "../datasets/raw/aae_tweets.csv"]

    a_tweets_list = extract_and_preprocess([file_list[0]], encoding='utf-8')
    b_tweets_list = extract_and_preprocess([file_list[1]], encoding='utf-8')

    with open('../datasets/tokenized/processed_white_tweets.txt', 'w') as f : 
        for twt in a_tweets_list: 
            if(len(twt) > 3): 
                f.write(" ".join(twt) + '\n')

    with open('../datasets/tokenized/processed_aae_tweets.txt', 'w') as f: 
        for twt in b_tweets_list: 
            if(len(twt) > 3):
                f.write(" ".join(twt) + '\n')
