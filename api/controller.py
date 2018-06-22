import pandas as pd
import subprocess
import json
import json
import psycopg2
from sqlalchemy import create_engine, text
import hashlib

def query2json(query,engine):
	pd_data = pd.read_sql_query(text(query), engine)
	json_data = json.loads(pd_data.to_json(orient="records"))
	return json_data


def id2assets(asset_ids, engine):
	asset_list = []
	for asset_id in asset_ids:
		query = """ SELECT asset_id,name,imgpath from assets where asset_id = '{}' """.format(asset_id)
		data = query2json(query, engine)
		asset_list+=data
	return asset_list


def hash_token(mystring):
	return(hashlib.md5(mystring.encode()).hexdigest())


def get_assets(user_id, engine):
	"""
	returns data and models visible to user
	"""
	data_query = """ SELECT * from assets where type = 'data' """
	models_query = """ SELECT * from assets where type = 'model' """
	metrics_query = """ SELECT * from assets where type = 'metric' """

	return {"data" : query2json(data_query, engine),"models" : query2json(models_query, engine),"metrics" : query2json(metrics_query,engine)}


def get_box(box_id,engine, from_db):
	print(box_id)
	if not from_db:
		try:
			comcon_query = """ SELECT * from comcon where id = '{}' """.format(box_id)
			box = query2json(comcon_query, engine)
			if len(box) == 0:
				return({"success" : False})
			box = box[0]
			box['alg_data'] = id2assets([box["alg1"], box["alg2"]], engine)
			box['stim_data'] = id2assets([box["stim1"], box["stim2"]], engine)
		except:
			return({"success" : False})
	return({"success" : True, 'box_details' : box})


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