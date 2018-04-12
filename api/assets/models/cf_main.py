#!/usr/bin/env python
import pandas as pd
import numpy as np
import sys
import json
import os
import sys
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage

sys.path.append('/Users/zive/GDrive/research/scalable/TuringBox/web/api')
from utils import turing_box

#clarifai API 

def call(path_to_data):
	app = ClarifaiApp(api_key='f0a9b3aa9a27429d9767e01746499400')
	model_nsfw = app.models.get('e9576d86d2004ed1a38ba0cf39ecb4b1')
	image = ClImage(file_obj=open(path_to_data, 'rb'))
	data2 = model_nsfw.predict([image])
	return data2['outputs'][0]['data']['concepts'][1]['value']

if __name__ == "__main__":
	turing_box(call, sys.argv)