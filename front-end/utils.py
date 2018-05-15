import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

amazon = pd.read_csv('static/data/amazon_sentiment100_results.csv')
sst = pd.read_csv('static/data/sst_sentiment100_results.csv')
twitter = pd.read_csv('static/data/twitter_sentiment100_results.csv')

standard = pd.read_csv('static/data/swim_thin.csv')
plus = pd.read_csv('static/data/swim_plus.csv')

box = {"amazon":amazon, "sst":sst, "twitter":twitter, "standard": standard, "plus" : plus}


def colorize(i):
	if i%2==0:
		return '#ED1C24'
	else:
		return '#00AEEF'


def plot(data,models):
	i = 0
	for m in models:
	    for d in data:
	        plt.figure(i)
	        col = box[d][m]
	        plt.hist(col, normed=True, bins=30, color = colorize(i))
	        plt.ylabel('Probability');
	        plt.title("{} => {}".format(d,m))
	        i+=1

from IPython.display import HTML
HTML('''
    <script type="text/javascript>
        IPython.notebook.kernel.execute("URL = ' + window.location + "'")
    </script>''')

def init(URL):
	return(unique(URL[URL.index('?data=')+6:URL.index('&')].split(',')), unique(URL[URL.index('&model=')+7:].split(',')))

def unique(x):
	return(list(set(x)))


def summarize(data, models):
	print("using datatsets: '{}".format("','".join(data)) + "'")
	print("using models: '{}".format("','".join(models)) + "'")
	print("access raw values with 'box[<data>][<model>]'")
	for d in data:
		try:
			datum = box[d]
			try:
				print("Stimulus mean is {}".format(datum['label'].mean()))
			except:
				pass
			for m in models:
				print("{} =>  {} = '{}' (mean)".format(d, m.capitalize(), round(datum[m].mean(),4)))		
		except:
			pass






