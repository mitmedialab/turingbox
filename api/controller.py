import pandas as pd
import subprocess
import json
import json
import psycopg2
from sqlalchemy import create_engine, text
import hashlib

add_asset = """ INSERT INTO assets VALUES  (%s, %s, %s, %s, %s,%s, %s, %s)"""
add_comcon = """ INSERT INTO comcon VALUES  (%s, %s, %s, %s, %s, %s, %s, %s)"""

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
	data_query = """ SELECT * from assets where type = 'stimulus' """
	models_query = """ SELECT * from assets where type = 'algorithm' """
	metrics_query = """ SELECT * from assets where type = 'metric' """

	return {"stimuli" : query2json(data_query, engine),"algorithms" : query2json(models_query, engine),"metrics" : query2json(metrics_query,engine)}


def get_box(box_id,engine, from_db):
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

def get_asset_context(asset_id,engine, from_db):
	if not from_db:
		try:
			query = """ SELECT * from assets where asset_id = '{}' """.format(asset_id)
			asset_context = query2json(query, engine)
			if len(asset_context) == 0:
				return({"success" : False})

			asset_context = asset_context[0]

			comcon_query = """ SELECT * from comcon where alg1 = '{}' or alg2 = '{}' or stim1 = '{}' or stim2 = '{}' """.format(asset_id,asset_id,asset_id,asset_id)
			boxes = query2json(comcon_query, engine)
		except:
			return({"success" : False})
	return({"success" : True, 'asset_context' : asset_context, "boxes" : boxes})

def ingest_asset(form_data, engine, conn, from_db):
	if not from_db:
		cur = conn.cursor()
		cur.execute(add_asset, (
	        form_data['asset_type'] + hash_token(form_data['filename']),
	        form_data['asset_type'],
	        form_data['asset_type'] + "/" + form_data['filename'],
	        "img/MLalg.png",
	        form_data['name'],
	        form_data['description'],
	        form_data['tags'],
	        form_data['task']))
		conn.commit()
		cur.close()
	return({"success" : True})


def launch_job(stimulus, algorithm, task, conn, engine):
	"""
	core computation that launch_box() calls in the API
	"""

    #get model url from model_id
	get_model_path = """ SELECT path from assets where asset_id = '{}' """.format(algorithm)
	model_path = query2json(get_model_path, engine)
	model_path = model_path[0]['path']

	get_data_path = """ SELECT path from assets where asset_id = '{}' """.format(stimulus)
	data_path = query2json(get_data_path, engine)
	data_path = data_path[0]['path']

	job_id = hash_token(data_path + model_path)

	comcon_query = """ SELECT * from comcon where id = '{}' """.format(job_id)
	box = query2json(comcon_query, engine)
	if len(box) != 0:
		print("job already completed. serving static data")
		return({"box_id" : job_id, "preprocessed" : 1})
	else:

		print("doing job{}".format(job_id))
		print(model_path,data_path)

		subprocess.call("python3 assets/{} assets/{} {}".format(model_path,data_path, job_id), shell=True)
		cur = conn.cursor()
		cur.execute(add_comcon, (
	        job_id,
	        algorithm,
	        '',
	        stimulus,
	        '',
	        task,
	        "comcon/{}.csv".format(job_id),
	        1))
		conn.commit()
		cur.close()
		return({"box_id" : job_id, "preprocessed" : 0})

