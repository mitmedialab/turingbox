import pandas as pd
import subprocess
import json
import psycopg2
from sqlalchemy import create_engine, text
import hashlib

def get_current_state(user_id, engine):
	"""
	returns data and models visible to user
	"""
	data_query = """ SELECT * from data """
	data = pd.read_sql_query(text(data_query), engine)
	
	model_query = """ SELECT * from models """
	models = pd.read_sql_query(text(model_query), engine)
	return {"data" : json.loads(data.to_json(orient="records")), "models" : json.loads(models.to_json(orient="records"))}


def launch_job(model_id, data_id, user_id, job_id, conn, engine):
	print("launching job {}".format(job_id))
	"""
	core computation that launch_box() calls in the API
	"""
	add_job = """ INSERT INTO jobs VALUES (%s, %s,%s, %s, FALSE)"""
	cur = conn.cursor()
	cur.execute(add_job, (job_id,model_id,data_id,job_id))

    #get model url from model_id
	get_model_path = """ SELECT path from models where id = '{}' """.format(model_id)
	model_path = pd.read_sql_query(text(get_model_path), engine)
	model_path = model_path.values[0][0]

	get_data_path = """ SELECT path from data where id = '{}' """.format(data_id)
	data_path = pd.read_sql_query(text(get_data_path), engine)
	data_path = data_path.values[0][0]
	print(job_id)
	subprocess.call("python3 {} {} {}".format(model_path,data_path, job_id), shell=True)
	
	update_job = """ UPDATE jobs SET completed = TRUE WHERE id = %s """
	cur.execute(update_job, (job_id,))
	#get logfile and user_id from job and send along to API 


def hash_token(mystring):
	return(hashlib.md5(mystring.encode()).hexdigest())


    