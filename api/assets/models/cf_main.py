#!/usr/bin/env python

import os
import sys
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage

#clarifai API 

print("CLARAFAI")
app = ClarifaiApp(api_key='f0a9b3aa9a27429d9767e01746499400')
model_nsfw = app.models.get('e9576d86d2004ed1a38ba0cf39ecb4b1')


fn = sys.argv[1]
if os.path.exists(fn):
    print(fn)
    image = ClImage(file_obj=open(fn, 'rb'))
    data2 = model_nsfw.predict([image])
    print(data2['outputs'][0]['data']['concepts'][1]['value'])


