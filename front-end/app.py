from flask import Flask, jsonify, request, abort
import requests
import json
import pandas as pd
from flask import render_template

# url = 'http://0.0.0.0:5000/api/v1/refresh/'
# payload = {'user_id': 'test47'}
# headers = {'content-type': 'application/json'}
# r = requests.get(url)
# data  = json.loads(r.text)

def ingest_static_data(path):
	data = pd.read_csv(path)
	rows = []
	for row in data.iterrows():
	    row = {"text": row[1][0][0:50]+"...", "label": row[1][1], "a_sent": round(row[1][2],2), "g_sent": round(row[1][3],2)}
	    rows.append(row)
	return rows

amazon = ingest_static_data('static/data/amazon_sentiment100_results.csv')
sst = ingest_static_data('static/data/sst_sentiment100_results.csv')
twitter = ingest_static_data('static/data/twitter_sentiment100_results.csv')


app = Flask(__name__)


@app.route('/')
def land():
    return render_template('land.html', data=data)

@app.route('/nlp')
def nlp_domain():
    return render_template('drag_and_drop.html', amazon=amazon, sst=sst, twitter = twitter)

@app.route('/cv')
def cv_domain():
    return render_template('drag_and_drop.html', amazon=amazon, sst=sst, twitter = twitter)

@app.route('/launchBox', methods = ['POST'])
def launch_box():
    print(47)
    return(47)


if __name__ == '__main__':
    app.run(
        port = 8080,
#	ssl_context=context,
        debug=True
    )
