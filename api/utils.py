import json
from time import gmtime, strftime

def turing_box(algorithm, args):
	y = ""
	success = True 
	try:
		y = algorithm(args[1])
	except Exception as e:
		y = str(e)
		success = False

	output = {"model_reply" : y, "data_url" : args[1], "success" : success, "time" : strftime("%Y-%m-%d %H:%M:%S", gmtime())}
	with open('assets/logs/{}.txt'.format(args[2]), 'w') as outfile:
		json.dump(output, outfile)