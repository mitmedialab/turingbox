import pandas as pd
import psycopg2
from flask import Flask, jsonify, request, abort
from sqlalchemy import create_engine, text
from creds import rds_username, rds_password, rds_url
from creds import rds_port, rds_db
import util
# from OpenSSL import SSL

# rds_creds = 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(
#     rds_username,
#     rds_password,
#     rds_url,
#     rds_port,
#     rds_db)
# engine = create_engine(rds_creds)
# conn = psycopg2.connect(
#     host=rds_url,
#     port=rds_port,
#     dbname=rds_db,
#     user=rds_username,
#     password=rds_password)


app = Flask(__name__)


@app.route('/api/v1/refresh/', methods=['POST'])
def get_state():
    """
    Input:
        {
            "user_id": str,
        }
    Returns JSON of data/models available
        {
            "data": [
                {
                    "title": str,
                    "desc" : "str"
                }],
            "models": [
                {
                    "title": str,
                    "desc" : "str"
                }]
        }
    """
    if not request.json:
        abort(400)
    state = get_current_state(request.json["user_id"])
    return state


@app.route('/api/v1/launch/', methods=['POST'])
def launch_box():
    """
    Input:
        {
            "user_id": text,
            "data_id": text,
            "model_id": text
        }
    performs core computation
    """
    if not request.json:
        abort(400)
    if request.json["up_vote"] == 1:
        update_flash = """ UPDATE flash
                    SET upvotes = upvotes + 1
                    WHERE id = %s"""
        update_user = """ INSERT INTO user_flashes VALUES (%s, %s, %s, %s, now(), %s, %s)"""
    elif request.json["down_vote"] == 1:
        update_flash = """ UPDATE flash
                    SET downvotes = downvotes + 1
                    WHERE id = %s"""
        update_user = """ INSERT INTO user_flashes VALUES (%s, %s, %s, %s, now(), %s, %s)"""
    cur = conn.cursor()
    cur.execute(update_user, (request.json["device_id"],
                              request.json["flash_id"],
                              False,
                              True,
                              request.json["lat"],
                              request.json["lon"]))
    print(request.json["flash_id"])
    cur.execute(update_flash, (request.json["flash_id"], ))
    conn.commit()
    cur.close()
    state = get_current_state(
        request.json["lat"],
        request.json["lon"],
        request.json["device_id"])
    return state


@app.route('/api/v1/submit/', methods=['POST'])
def submit():
    """
    Input:
        {
            "device_id": text,
            "title": text,
            "desc": text,
            "lat": float,
            "lon": float,
            "start_time": date
            "end_time": date
        }
    Updates database with flash, returns JSON of active flashes within 1/8 mile
    """
    if not request.json:
        abort(400)
    data = pd.read_sql_query(
        text("SELECT MAX(id) as max_id FROM flash"), engine)
    next_id = int(data.max_id[0] + 1)
    update_user = """ INSERT INTO user_flashes VALUES
                   (%s, %s, %s, %s, now(), %s, %s)"""
    update_flash = """ INSERT INTO flash VALUES
                    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                 """
    cur = conn.cursor()
    cur.execute(update_user, (request.json["device_id"],
                              next_id,
                              True,
                              True,
                              request.json["lat"],
                              request.json["lon"]))
    cur.execute(update_flash, (
        next_id,
        request.json["title"],
        request.json["text"],
        request.json["lat"],
        request.json["lon"],
        request.json["start_time"],
        request.json["end_time"],
        1,
        0,
        request.json["urgency"]))
    conn.commit()
    cur.close()
    state = get_current_state(
        request.json["lat"],
        request.json["lon"],
        request.json["device_id"])
    return state


if __name__ == '__main__':
    context = ('server.crt', 'server.key')
    app.run(
        host="0.0.0.0",
#	ssl_context=context,
        debug=True
    )
