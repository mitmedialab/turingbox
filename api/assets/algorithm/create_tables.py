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

drop_assets = """
    DROP TABLE assets;
    """

drop_comcon = """
    DROP TABLE comcon;
    """

add_asset = """ INSERT INTO assets VALUES  (%s, %s, %s, %s, %s,%s, %s, %s)"""
add_comcon = """ INSERT INTO comcon VALUES  (%s, %s, %s, %s, %s, %s, %s, %s)"""


if __name__ == '__main__':

    cur = conn.cursor()
    cur.execute(drop_assets)
    cur.execute(assets)
    cur.execute(add_asset, (
        "stimulus1",
        "stimulus",
        "stimulus/dummy.csv",
        "img/MLalg.png",
        "recidivism",
        "raw data for recidivism risk score",
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
        "data/swim.csv",
        "img/MLalg.png",
        "MIT Swimsuite dataset",
        "curated images of swimsite model with sensitive feature z = plus or not",
        "computer vision, machine gaze, fairness",
        "CV"))

    cur.execute(add_asset, (
        "algorithm1",
        "algorithm",
        "algorithm/dummy.py",
        "img/MLalg.png",
        "COMPAS*",
        "the COMPAS recidivism algorithm by Northpointe",
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
        "1",
        "algorithm1",
        "",
        "stimulus1",
        "",
        "compas",
        "comcon/compas.csv",
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

    conn.commit()
    cur.close()
    conn.close()
