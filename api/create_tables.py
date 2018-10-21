import psycopg2
import time
import os
from creds import db_username, db_password, db_url
from creds import db_port, db_name

from creds import rds_username, rds_password, rds_url
from creds import rds_port, rds_name
from controller import hash_token

local = True

if local:
    username = db_username
    password = db_password
    url = db_url
    port = db_port
    name = db_name
else:
    username = rds_username
    password = rds_password
    url = rds_url
    port = rds_port6
    name = rds_name

conn = psycopg2.connect(
    host=url,
    port=port,
    dbname=name,
    user=username,
    password=password)

assets = """
    CREATE TABLE assets (
        asset_id        varchar(256) PRIMARY KEY,
        type            varchar(256),
        path            varchar(256),
        imgpath         varchar(256),
        name            varchar(256),
        description     varchar(256),
        tags            varchar(256),
        task            varchar(256),
        framelink       varchar(256)
    );
    """

comcon = """
    CREATE TABLE comcon (
        id              varchar(256),
        alg1            varchar(256),
        alg2            varchar(256),
        stim1           varchar(256),
        stim2           varchar(256),
        task            varchar(256),
        path            varchar(256),
        completed       integer
    );
    """
metrics = """
    CREATE TABLE metrics (
        metric_id          varchar(256),
        comcon_id          varchar(256),
        output             varchar(256),
        label              varchar(256),
        referent           varchar(256)
    );
    """

comments = """
    CREATE TABLE comments (
        asset_id           varchar(256),
        comment            varchar(256),
        ts                 timestamp
    );
    """


drop_assets = """
    DROP TABLE assets;
    """

drop_comcon = """
    DROP TABLE comcon;
    """

drop_metrics = """
    DROP TABLE metrics;
    """

drop_comments = """
    DROP TABLE comments;
    """



add_asset = """ INSERT INTO assets VALUES  (%s, %s, %s, %s, %s,%s, %s, %s, %s)"""
add_comcon = """ INSERT INTO comcon VALUES  (%s, %s, %s, %s, %s, %s, %s, %s)"""
add_comment = """ INSERT INTO comments VALUES  (%s, %s, %s)"""


if __name__ == '__main__':

    cur = conn.cursor()
    cur.execute(drop_assets)
    cur.execute(assets)
    cur.execute(add_asset, (
        "stimulus1",
        "stimulus",
        "stimulus/criminalHistory.csv",
        "img/assets/crimeStim.png",
        "Criminal Records",
        "raw data of criminal records used to make a risk assessment",
        "crime, predpol",
        "compas",
        ""))

    cur.execute(add_asset, (
        "stimulus2",
        "stimulus",
        "stimulus/dummy.csv",
        "img/MLalg.png",
        "spam",
        "spammy dummy data",
        "spam, dingus",
        "dummy",
        ""))

    cur.execute(add_asset, (
        "stimulus3",
        "stimulus",
        "stimulus/swim.csv",
        "img/assets/thin_stim.png",
        "MIT Swimsuit dataset",
        "Curated images of swimsuit models. Sensitive feature is if the model is plus sized or not",
        "computer vision, machine gaze, fairness",
        "swim",
        "mitswim.png"))

    cur.execute(add_asset, (
        "stimulus5",
        "stimulus",
        "stimulus/clothing1000.csv",
        "img/assets/text_stim.png",
        "Women Clothing E-Commerce Shopping Reviews ",
        "1000 clothing reviews including review text, binarized (0/1) ratings and shopper age",
        "NLP, fairness, shopping",
        "NLP",
        ""))

    cur.execute(add_asset, (
        "stimulus6",
        "stimulus",
        "stimulus/movies1000.csv",
        "img/assets/text_stim.png",
        "Amazon Movie Reviews",
        "1000 movie reviews from 1997 - 2012 including review text, binarized (0/1) ratings and inferred reviewer gender based on first name ",
        "NLP, fairness, movies",
        "NLP",
        ""))

    cur.execute(add_asset, (
        "stimulus7",
        "stimulus",
        "stimulus/yelp1000.csv",
        "img/assets/text_stim.png",
        "Yelp Business Reviews",
        "1000 business reviews from Yelp including review text, binarized (0/1) ratings and inferred reviewer gender based on first name ",
        "NLP, fairness",
        "NLP",
        ""))

    cur.execute(add_asset, (
        "algorithm1",
        "algorithm",
        "algorithm/compas.py",
        "img/assets/compas.png",
        "COMPAS*",
        "the COMPAS risk assessment algorithm by Northpointe. *To be clear, we do not have access to this algorithm at this time, although we would love to have it on the platform for the public to scrutinize.",
        "crime, predpol",
        "compas",
        ""))

    cur.execute(add_asset, (
        "algorithm2",
        "algorithm",
        "algorithm/dummy.py",
        "img/MLalg.png",
        "Spam Alg",
        "this is a janky spam alg",
        "spam, dingus",
        "dummy",
        ""))

    cur.execute(add_asset, (
        "algorithm3",
        "algorithm",
        "algorithm/cf_main.py",
        "img/assets/clarifai.png",
        "Clarifai",
        "Clarifai's NSFW algorithm",
        "computer vision, NSFW",
        "swim",
        ""))

    cur.execute(add_asset, (
        "algorithm4",
        "algorithm",
        "algorithm/google_sentiment.py",
        "img/assets/google.png",
        "Google Sentiment Analysis",
        "Sentiment score form Google's sentiment algorithm from Cloud Natural Language API",
        "NLP, sentiment",
        "NLP",
        ""))

    cur.execute(add_asset, (
        "algorithm5",
        "algorithm",
        "algorithm/microsoft_sentiment.py",
        "img/assets/microsoft.png",
        "Microsoft Sentiment Analysis",
        "Sentiment score form Microsoft sentiment algorithm from Azure Text Analytics API",
        "NLP, sentiment",
        "NLP",
        ""))

    # cur.execute(add_asset, (
    #     "algorithm6",
    #     "algorithm",
    #     "algorithm/textblob_sentiment.py",
    #     "img/assets/Textblob.png",
    #     "Textblob Sentiment Analysis",
    #     "Sentiment polarity score from python Textblob library",
    #     "NLP, sentiment",
    #     "NLP",
    #     ""))


    cur.execute(add_asset, (
        "metric1",
        "metric",
        "metric/average.py",
        "img/assets/metric.png",
        "Difference in Means",
        "difference in y hat on one binary sensitive attribute",
        "stats, disparate treatment",
        "swim",
        ""))

    cur.execute(add_asset, (
        "metric4",
        "metric",
        "metric/average.py",
        "img/assets/metric.png",
        "Difference in Means",
        "difference in y hat on one binary sensitive attribute",
        "stats, disparate treatment",
        "compas",
        ""))

    # cur.execute(add_asset, (
    #     "metric2",
    #     "metric",
    #     "metric/acc_diff.py",
    #     "img/MLalg.png",
    #     "Difference in Accuracy",
    #     "difference in test set accuracy of classifier with respect to sensitive attribute",
    #     "stats, disparate mistreatment",
    #     "NLP"))

    cur.execute(add_asset, (
        "metric3",
        "metric",
        "metric/mean_diff.py",
        "img/assets/metric.png",
        "Difference in Means",
        "difference in y hat on one binary sensitive attribute",
        "stats, disparate treatment",
        "NLP",
        ""))

    cur.execute(drop_comcon)
    cur.execute(comcon)
    cur.execute(add_comcon, (
        "0",
        "algorithm2",
        "",
        "stimulus2",
        "",
        "dummy",
        "comcon/dummy.csv",
        1))

    cur.execute(add_comcon, (
        "criminalHistory_compas_results",
        "algorithm1",
        "",
        "stimulus1",
        "",
        "compas",
        "comcon/criminalHistory_compas_results.csv",
        1))

    cur.execute(add_comcon, (
        "2",
        "algorithm3",
        "",
        "stimulus3",
        "",
        "swim",
        "comcon/swim.csv",
        1))
    cur.execute(drop_metrics)
    cur.execute(metrics)

    cur.execute(drop_comments)
    cur.execute(comments)
    cur.execute(add_comment, (
        "algorithm2",
        "this algorithm is bogus",
        '2016-06-22 19:10:25-07'))

    conn.commit()
    cur.close()
    conn.close()
