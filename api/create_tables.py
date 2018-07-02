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
        task            varchar(256)
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



add_asset = """ INSERT INTO assets VALUES  (%s, %s, %s, %s, %s,%s, %s, %s)"""
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
        "img/MLalg.png",
        "Criminal Records",
        "raw data of criminal records used to make a risk assessment",
        "crime, predpol",
        "compas"))

    cur.execute(add_asset, (
        "stimulus2",
        "stimulus",
        "stimulus/dummy.csv",
        "img/MLalg.png",
        "spam",
        "spammy dummy data",
        "spam, dingus",
        "dummy"))

    cur.execute(add_asset, (
        "stimulus3",
        "stimulus",
        "stimulus/swim.csv",
        "img/MLalg.png",
        "MIT Swimsuite dataset",
        "curated images of swimsite model with sensitive feature z = plus or not",
        "computer vision, machine gaze, fairness",
        "swim"))

    cur.execute(add_asset, (
        "stimulus5",
        "stimulus",
        "stimulus/clothing1000.csv",
        "img/MLalg.png",
        "Clothing ",
        "dataset of clothing, 1000",
        "NLP, fairness",
        "NLP"))

    cur.execute(add_asset, (
        "stimulus6",
        "stimulus",
        "stimulus/movies1000.csv",
        "img/MLalg.png",
        "movies1000 Dataset",
        "data set of 1000 movie reviews, labelled",
        "NLP, fairness",
        "NLP"))

    cur.execute(add_asset, (
        "stimulus7",
        "stimulus",
        "stimulus/sst_sentiment100.csv",
        "img/MLalg.png",
        "Rotten Tomatoes dataset",
        "dataset of 100 rotten tomoatoes comments",
        "NLP, fairness",
        "NLP"))

    cur.execute(add_asset, (
        "stimulus8",
        "stimulus",
        "stimulus/twitter_sentiment100.csv",
        "img/MLalg.png",
        "Twitter",
        "datatset of 100 annotated tweets with sentiment",
        "NLP, fairness, twitter",
        "NLP"))

    cur.execute(add_asset, (
        "stimulus9",
        "stimulus",
        "stimulus/amazon_sentiment100.csv",
        "img/MLalg.png",
        "Yelp",
        "yelp dataset labelled with sentiment",
        "NLP, fairness, online shopping",
        "NLP"))


    cur.execute(add_asset, (
        "algorithm1",
        "algorithm",
        "algorithm/compas.py",
        "img/MLalg.png",
        "COMPAS*",
        "the COMPAS risk assessment algorithm by Northpointe. *To be clear, we do not have access to this algorithm at this time, although we would love to have it on the platform for the public to scrutinize.",
        "crime, predpol",
        "compas"))

    cur.execute(add_asset, (
        "algorithm2",
        "algorithm",
        "algorithm/dummy.py",
        "img/MLalg.png",
        "Spam Alg",
        "this is a janky spam alg",
        "spam, dingus",
        "dummy"))

    cur.execute(add_asset, (
        "algorithm3",
        "algorithm",
        "algorithm/cf_main.py",
        "img/MLalg.png",
        "Clarifai",
        "Clarifai's NSFW algorithm",
        "computer vision, NSFW",
        "swim"))

    cur.execute(add_asset, (
        "algorithm4",
        "algorithm",
        "algorithm/google_sentiment.py",
        "img/MLalg.png",
        "Google Sentiment",
        "Google's sentiment algorithm",
        "NLP, sentiment",
        "NLP"))

    cur.execute(add_asset, (
        "algorithm5",
        "algorithm",
        "algorithm/microsoft_sentiment.py",
        "img/MLalg.png",
        "Microsoft Sentiment",
        "Microsoft's sentiment algorithm",
        "NLP, sentiment",
        "NLP"))

    cur.execute(add_asset, (
        "algorithm6",
        "algorithm",
        "algorithm/textblob_sentiment.py",
        "img/MLalg.png",
        "Textblob Sentiment",
        "sentiment text blob",
        "NLP, sentiment",
        "NLP"))


    cur.execute(add_asset, (
        "metric1",
        "metric",
        "metric/average.py",
        "img/MLalg.png",
        "Difference in Means",
        "difference in y hat on one binary sensitive attribute",
        "stats, disparate treatment",
        "swim"))

    cur.execute(add_asset, (
        "metric2",
        "metric",
        "metric/acc_diff.py",
        "img/MLalg.png",
        "Difference in Accuracy",
        "difference in test set accuracy of classifier with respect to sensitive attribute",
        "stats, disparate mistreatment",
        "NLP"))

    cur.execute(add_asset, (
        "metric3",
        "metric",
        "metric/mean_diff.py",
        "img/MLalg.png",
        "Difference in Means",
        "difference in y hat on one binary sensitive attribute",
        "stats, disparate treatment",
        "NLP"))

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
