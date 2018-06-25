from flask import Flask, jsonify, request, abort, redirect, url_for
import requests
import json
import pandas as pd
import os
from flask import render_template
from wtforms import Form, BooleanField, StringField, FileField, validators
from werkzeug.utils import secure_filename
from werkzeug.datastructures import CombinedMultiDict

asset_library = '/Users/zive/GDrive/research/machine-behavior/turingbox/api/assets'


def get_assets():
    url = 'http://0.0.0.0:5000/api/v2/refresh/'
    payload = {'user_id': 'test47'}
    headers = {'content-type': 'application/json'}
    r = requests.get(url)
    data  = json.loads(r.text)
    return data

def get_box(box_id):
    url = 'http://0.0.0.0:5000/api/v2/get_box/'
    payload = {'box_id': box_id}
    headers = {'content-type': 'application/json'}
    r = requests.post(url, json = payload)
    data  = json.loads(r.text)
    return data

def get_asset_context(asset_id):
    url = 'http://0.0.0.0:5000/api/v2/get_asset/'
    payload = {'asset_id': asset_id}
    headers = {'content-type': 'application/json'}
    r = requests.post(url, json = payload)
    data  = json.loads(r.text)
    return data

def push_form(form, task, filename, asset_type):
    url = 'http://0.0.0.0:5000/api/v2/ingest_asset/'
    payload = {"form_data" : {'name': form.name.data, 'description' : form.description.data, 'tags' : form.tags.data, "task" : task, "asset_type" : asset_type, "filename" : filename}}
    headers = {'content-type': 'application/json'}
    r = requests.post(url, json = payload)
    data  = json.loads(r.text)
    print(data)

def ingest_static_data(path):
    data = pd.read_csv(path)
    rows = []
    for row in data.iterrows():
        row = {"text": row[1][0][0:50]+"...", "label": row[1][1], "a_sent": round(row[1][2],2), "g_sent": round(row[1][3],2),"minsky": row[1][4]}
        rows.append(row)
    return rows


def ingest_static_swim_data(path,t):
    data = pd.read_csv(path)
    rows = []
    for row in data.iterrows():
        row = {"path": "static/swim/{}".format(row[1][4]), "type": t, "google": row[1][1], "microsoft": row[1][2], "clarifai" : row[1][3]}
        rows.append(row)
    return rows

class AlgForm(Form):
    name = StringField('name', [validators.Length(min=4, max=25)])
    description = StringField('description', [validators.Length(min=6, max=35)])
    tags = StringField('tags', [validators.Length(min=6, max=35)])
    alg = FileField(u'algorithm file')

amazon = ingest_static_data('static/data/amazon_sentiment100_results.csv')
sst = ingest_static_data('static/data/sst_sentiment100_results.csv')
twitter = ingest_static_data('static/data/twitter_sentiment100_results.csv')

swim_thin = ingest_static_swim_data('static/data/swim_thin.csv', "thin")
swim_plus = ingest_static_swim_data('static/data/swim_plus.csv', "plus") 

app = Flask(__name__)
app.secret_key = 'skinner'

static_pages = ['index.html', 'about.html','launchBox.html','upload.html']


@app.route('/')
def land():
    return render_template('index.html')

@app.route('/index.html')
def landRoute():
    return render_template('index.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/launchBox.html')
def launchBox():
    payload = get_assets()
    stimuli = payload['stimuli']
    algorithms = payload['algorithms']
    metrics = payload['metrics']
    return render_template('launchBox.html', stimuli = stimuli, algorithms = algorithms, metrics = metrics)

@app.route('/upload.html')
def contribute():
    return render_template('upload.html')

@app.route('/report/<box_id>')
def report(box_id):
    if box_id in static_pages:
        return render_template(box_id)
    payload = get_box(box_id)
    if payload['success']:
        box = payload['box_details']
        box['success'] = True
    else:
        box = {"success" : False}
    return render_template('report.html', box_id = box_id, box = box)

@app.route('/context/<asset_type>/<asset_id>')
def context(asset_type, asset_id):
    if asset_id in static_pages:
        return render_template(asset_id)
    payload = get_asset_context(asset_id)
    return render_template('context.html', asset_type = asset_type, payload = payload)

@app.route('/submit/<asset_type>/<task>',  methods=['GET', 'POST'])
def submit(asset_type, task):
    if task in static_pages:
        return render_template(task)
    form = AlgForm(CombinedMultiDict((request.files, request.form)))
    if request.method == 'POST' and form.validate():
        file = request.files['alg']
        filename = secure_filename(file.filename)
        file.save(os.path.join(
            asset_library, asset_type, filename
        ))
        push_form(form,task,filename,asset_type)
        return redirect(url_for('land'))
    return render_template('submit.html', asset_type = asset_type, task = task, form = form)

@app.route('/cv')
def cv_domain():
    print(swim_thin)
    return render_template('cv.html', swim_thin = swim_thin,swim_plus = swim_plus)


if __name__ == '__main__':
    app.run(
        port = 8080,
#	ssl_context=context,
        debug=True
    )
