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
    port = rds_port
    name = rds_name

conn = psycopg2.connect(
    host=url,
    port=port,
    dbname=name,
    user=username,
    password=password)

data = """
    CREATE TABLE data (
        id              varchar(256) PRIMARY KEY,
        title           varchar(256),
        description     varchar(256),
        type            varchar(256),
        path            varchar(256)
    );
    """

models = """
    CREATE TABLE models (
        id              varchar(256),
        title           varchar(256),
        description     varchar(256),
        input_type      varchar(256),
        output_type     varchar(256),
        path            varchar(256)
    );
    """

jobs = """
    CREATE TABLE jobs (
        id              varchar(256),
        model_id        varchar(256),
        data_id         varchar(256),
        logfile         varchar(256),
        completed       boolean
    );
    """

add_data = """ INSERT INTO data VALUES  (%s, %s, %s, %s, %s)"""
add_model = """ INSERT INTO models VALUES  (%s, %s, %s, %s, %s, %s)"""


if __name__ == '__main__':

    cur = conn.cursor()
    cur.execute(data)
    cur.execute(add_data, (
        "1",
        "data1",
        "this is dummy data",
        "botsheet",
        "assets/data/data1.csv",))

    for i,swim in enumerate(os.listdir("assets/data/swim")):
        cur.execute(add_data, (
            hash_token(swim),
            "Swim Suite Image {}".format(i),
            swim,
            "image",
            "assets/data/swim/{}".format(swim)))


    cur.execute(models)
    cur.execute(add_model, (
        "0",
        "model1",
        "this is a dummy model",
        "botsheet",
        "magnitude",
        "assets/models/model1.py"))

    cur.execute(add_model, (
        "1",
        "Clarify",
        "Clarify's vision API",
        "image",
        "nsfw score",
        "assets/models/cf_main.py"))

    cur.execute(jobs)
    conn.commit()
    cur.close()
    conn.close()
