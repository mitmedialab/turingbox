import pandas as pd
import psycopg2
from flask import Flask, jsonify, request, abort
from sqlalchemy import create_engine, text
from creds import rds_username, rds_password, rds_url
from creds import rds_port, rds_db
import controller
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
    state = controller.get_current_state(request.json["user_id"], engine)
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

    controller.launch_job(model_id, data_id, user_id, conn)


if __name__ == '__main__':
    context = ('server.crt', 'server.key')
    app.run(
        host="0.0.0.0",
#	ssl_context=context,
        debug=True
    )