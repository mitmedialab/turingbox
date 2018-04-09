import psycopg2
import time
from creds import rds_username, rds_password, rds_url
from creds import rds_port, rds_db


conn = psycopg2.connect(
    host=rds_url,
    port=rds_port,
    dbname=rds_db,
    user=rds_username,
    password=rds_password)

data = """
    CREATE TABLE data (
        id              integer PRIMARY KEY,
        title           varchar(256),
        description     varchar(256),
        path            varchar(256)
    );
    """

models = """
    CREATE TABLE models (
        id              integer,
        title           varchar(256),
        description     varchar(256),
        path            varchar(256)
    );
    """

jobs = """
    CREATE TABLE jobs (
        id              integer,
        model_id        integer,
        data_id         integer,
        logfile         varchar(256),
        completed       boolean
    );
    """

add_data = """ INSERT INTO data VALUES  (%s, %s, %s, %s)"""
add_model = """ INSERT INTO model VALUES  (%s, %s, %s, %s)"""
add_job = """ INSERT INTO jobs VALUES (%s, %s,%s, %s, false)"""
complete_job = """ """



if __name__ == '__main__':

    cur = conn.cursor()
    cur.execute(data)
    cur.execute(add_data, (
        1,
        "data1",
        "this is dummy data",
        "assets/data/data1.csv"))

    cur.execute(model)
    cur.execute(add_model, (
        1,
        "model1",
        "this is a dummy model",
        "assets/models/model1.csv"))

    cur.execute(jobs)
    conn.commit()
    cur.close()
    conn.close()
