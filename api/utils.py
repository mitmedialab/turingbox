import json
import pandas as pd
from time import gmtime, strftime

def turing_box(algorithm, args):
	y = ""
	success = True 
	try:
		comcon = algorithm(args[1])
		y = "worked"
		comcon.to_csv("assets/comcon/{}.csv".format(args[2]))
	except Exception as e:
		print(e)
		y = str(e)
		success = False

	output = {"model_reply" : y, "data_url" : args[1], "success" : success, "time" : strftime("%Y-%m-%d %H:%M:%S", gmtime())}
	with open('assets/logs/{}.txt'.format(args[2]), 'w') as outfile:
		json.dump(output, outfile)

def evaluate_metric(metric, args):
	# try:
	output = metric(args[1])
	print(json.dumps(output))
	# except Exception as e:
		# print("metric failed")