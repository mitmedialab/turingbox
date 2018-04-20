from flask import Flask, jsonify, request, abort
import requests
import json
from flask import render_template

url = 'http://0.0.0.0:5000/api/v1/refresh/'
payload = {'user_id': 'test47'}
headers = {'content-type': 'application/json'}
r = requests.get(url)
data  = json.loads(r.text)


app = Flask(__name__)


@app.route('/')
def land():
    return render_template('land.html', data=data)

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
