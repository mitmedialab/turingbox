import pandas as pd
import subprocess
from subprocess import PIPE, run
import json
import json
import psycopg2
from sqlalchemy import create_engine, text
import hashlib
from time import gmtime, strftime

add_asset = """ INSERT INTO assets VALUES  (%s, %s, %s, %s, %s,%s, %s, %s)"""
add_comcon = """ INSERT INTO comcon VALUES  (%s, %s, %s, %s, %s, %s, %s, %s)"""
add_metric = """ INSERT INTO metrics VALUES  (%s, %s, %s, %s, %s)"""
add_comment = """ INSERT INTO comments VALUES  (%s, %s, %s)"""

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


def get_assets(task, engine):
	"""
	returns data and models visible to user
	"""
	data_query = """ SELECT * from assets where type = 'stimulus' and task = '{}' """.format(task)
	models_query = """ SELECT * from assets where type = 'algorithm' and task = '{}'""".format(task)
	metrics_query = """ SELECT * from assets where type = 'metric' and task = '{}' """.format(task)

	return {"stimuli" : query2json(data_query, engine),"algorithms" : query2json(models_query, engine),"metrics" : query2json(metrics_query,engine)}


def get_box(box_id,engine, from_db):
	if not from_db:
		# try:
		comcon_query = """ SELECT * from comcon where id = '{}' """.format(box_id)
		print(box_id)
		box = query2json(comcon_query, engine)
		if len(box) == 0:
			return({"success" : False})
		box = box[0]
		box['alg_data'] = id2assets([box["alg1"], box["alg2"]], engine)
		box['stim_data'] = id2assets([box["stim1"], box["stim2"]], engine)
		metrics_query = """ SELECT * from metrics where comcon_id = '{}' """.format(box_id)
		metrics = query2json(metrics_query, engine)
		print(metrics)
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

			comment_query = """ SELECT * from comments where asset_id = '{}' """.format(asset_id)
			commets = query2json(comment_query, engine)
		except:
			return({"success" : False})
	return({"success" : True, 'asset_context' : asset_context, "boxes" : boxes,  "commets" : commets})

def ingest_asset(form_data, conn, from_db):
	if not from_db:
		cur = conn.cursor()
		cur.execute(add_asset, (
	        form_data['asset_type'] + hash_token(form_data['filename']),
	        form_data['asset_type'],
	        form_data['asset_type'] + "/" + form_data['filename'],
	        "img/assets/{}.png".format(form_data['asset_type']),
	        form_data['name'],
	        form_data['description'],
	        form_data['tags'],
	        form_data['task']))
		conn.commit()
		cur.close()
	return({"success" : True})

def ingest_comment(comment, asset_id, conn, from_db):
	ts = strftime("%Y-%m-%d %H:%M:%S", gmtime())
	if not from_db:
		cur = conn.cursor()
		cur.execute(add_comment, (
	        asset_id,
	        comment,
	        ts))
		conn.commit()
		cur.close()
	return({"success" : True})


def launch_job(stimulus, algorithm, metric, task, conn, engine):
	"""
	core computation that launch_box() calls in the API
	"""
	print(algorithm)
	model_path = get_asset_property('path', algorithm, engine)
	data_path = get_asset_property('path',stimulus, engine)
	

	cur = conn.cursor()


	clean = lambda s,ft: s.split("/")[-1].replace(ft,"")

	job_id = "{}_{}_results".format(clean(data_path, ".csv"),clean(model_path,".py"))

	comcon_query = """ SELECT * from comcon where id = '{}' """.format(job_id)
	box = query2json(comcon_query, engine)
	if len(box) != 0:
		print("job already completed. serving static data")
	else:

		print("doing job {}".format(job_id))

		run_algorithm = "python3 assets/{} assets/{} {}".format(model_path,data_path, job_id)
		print("bash is running : {}".format(run_algorithm))
		subprocess.call(run_algorithm, shell=True)
		print("finished run")
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

	metric_query = """ SELECT * from metrics where metric_id = '{}' and comcon_id = '{}' """.format(metric,job_id)
	previous_metric = query2json(metric_query, engine)
	if len(previous_metric) != 0 or len(metric)==0:
		print("metric already computed or no metric was given. serving static data")
		return({"box_id" : job_id})
	else:
		metric_path = get_asset_property('path',metric, engine)
		print("metric_path: {}".format(metric_path))
		print("job_id: {}".format(job_id))
		command = ["python3","assets/"+metric_path, "assets/comcon/{}.csv".format(job_id)]
		print("bash is running (metric): {}".format(" ".join(command)))
		result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=False)
		print(result)
		print(result.stdout)
		print("out: {}".format(result.stdout))
		metric_outputs = json.loads(result.stdout)
		ref = metric_outputs['ref']
		print(metric)
		for key, value in metric_outputs.items():
			if key != 'ref':
				print("metric result: {}".format(metric_outputs[key]))
				cur.execute(add_metric, (
			        metric,
			        job_id,
			        metric_outputs[key],
			        key,
			        ref))

		conn.commit()
		cur.close()
	return({"box_id" : job_id})

