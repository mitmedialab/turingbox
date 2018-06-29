import pandas as pd
import subprocess
from subprocess import PIPE, run
import json
import json
import psycopg2
from sqlalchemy import create_engine, text
import hashlib

add_asset = """ INSERT INTO assets VALUES  (%s, %s, %s, %s, %s,%s, %s, %s)"""
add_comcon = """ INSERT INTO comcon VALUES  (%s, %s, %s, %s, %s, %s, %s, %s)"""
add_metric = """ INSERT INTO metrics VALUES  (%s, %s, %s, %s, %s)"""

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

def get_asset_property(prop, asset_id, engine):
	get_path = """ SELECT {} from assets where asset_id = '{}' """.format(prop, asset_id)
	path = query2json(get_path, engine)
	return(path[0][prop])


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
		# try:
		comcon_query = """ SELECT * from comcon where id = '{}' """.format(box_id)
		box = query2json(comcon_query, engine)
		if len(box) == 0:
			return({"success" : False})
		box = box[0]
		box['alg_data'] = id2assets([box["alg1"], box["alg2"]], engine)
		box['stim_data'] = id2assets([box["stim1"], box["stim2"]], engine)
		print(4747)
		metrics_query = """ SELECT * from metrics where comcon_id = '{}' """.format(box_id)
		metrics = query2json(metrics_query, engine)
		for metric in metrics:
			metric_name = get_asset_property('name', metric['metric_id'], engine)
			metric['name'] = metric_name
		box['metrics'] = metrics
		# except:
		# 	return({"success" : False})
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


def launch_job(stimulus, algorithm, metric, task, conn, engine):
	"""
	core computation that launch_box() calls in the API
	"""
	model_path = get_asset_property('path', algorithm, engine)
	data_path = get_asset_property('path',stimulus, engine)
	metric_path = get_asset_property('path',metric, engine)

	job_id = hash_token(data_path + model_path)

	comcon_query = """ SELECT * from comcon where id = '{}' """.format(job_id)
	box = query2json(comcon_query, engine)
	if len(box) != 0:
		print("job already completed. serving static data")
		return({"box_id" : job_id, "preprocessed" : 1})
	else:

		print("doing job {}".format(job_id))

		subprocess.call("python3 assets/{} assets/{} {}".format(model_path,data_path, job_id), shell=True)
		print("finished run")
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
		print("added to db")

		if metric:
			command = ["python3","assets/"+metric_path, "assets/comcon/{}.csv".format(job_id)]
			result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=False)
			print("out: {}".format(result.stdout))
			metric_outputs = json.loads(result.stdout)
			for metric_output in metric_outputs:
				print("metric result: {}".format(metric_output))
				cur.execute(add_metric, (
			        metric,
			        job_id,
			        metric_output['output'],
			        metric_output['label'],
			        metric_output['referent']))

		conn.commit()
		cur.close()
		return({"box_id" : job_id, "preprocessed" : 0})

