import pandas as pd
import psycopg2
import json
from flask import Flask, jsonify, request, abort
from sqlalchemy import create_engine, text
from creds import db_username, db_password, db_url
from creds import db_port, db_name
from creds import rds_username, rds_password, rds_url
from creds import rds_port, rds_name
import controller
from flask_cors import CORS
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/assets/models'
ALLOWED_EXTENSIONS = set(['py'])


# from OpenSSL import SSL
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

creds = 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(
    username,
    password,
    url,
    port,
    name)
engine = create_engine(creds)

conn = psycopg2.connect(
    host=url,
    port=port,
    dbname=name,
    user=username,
    password=password)


app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



@app.route('/api/v2/refresh/', methods=['GET'])
def get_assets():
    """
    Input:
        {
            "user_id": str,
        }
    Returns JSON of data/models available
        {
            "assets": [
                {
                    "title": str,
                    "desc" : "str"
                }]
        }
    """
    print(47)
    state = controller.get_assets("47", engine)
    return(jsonify(state))


@app.route('/api/v1/launch/', methods=['POST'])
def launch_box():
    """
    Input:
        {
            "user_id": text,
            "data_id": text,
            "model_id": text,
            "job_id": text,
        }
    performs core computation
    """
    if not request.json:
        abort(400)
    print(request)
    controller.launch_job(request.json["model_id"], request.json["data_id"], request.json["user_id"],request.json["job_id"], conn, engine)
    return(request.json["job_id"])

@app.route('/api/v2/get_box/', methods = ['POST'])
def get_box():
    """
    Input:
        {
            "box_id": str,
        }
    Returns JSON of data/models available
        {
            "box": {
                    "title": str,
                    "desc" : "str"
                }
        }
    """
    
    if not request.json:
        abort(400)
    output = controller.get_box(request.json["box_id"], engine, from_db = False)
    print(output)
    return(json.dumps(output))


if __name__ == '__main__':
    context = ('server.crt', 'server.key')
    app.run(
        host="0.0.0.0",
#	ssl_context=context,
        debug=True
    )
