import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

amazon = pd.read_csv('static/data/amazon_sentiment100_results.csv')
sst = pd.read_csv('static/data/sst_sentiment100_results.csv')
twitter = pd.read_csv('static/data/twitter_sentiment100_results.csv')

datoids = {"amazon":amazon, "sst":sst, "twitter":twitter}




def plot(x):
	plt.hist(x, normed=True, bins=30)
	plt.ylabel('Probability');

from IPython.display import HTML
HTML('''
    <script type="text/javascript>
        IPython.notebook.kernel.execute("URL = ' + window.location + "'")
    </script>''')

def init(URL):
	return(URL[URL.index('?data=')+6:URL.index('&')].split(','), URL[URL.index('&model=')+7:].split(','))

def summarize(data, models):
	for d in data:
		try:
			datum = datoids[d]
			print("Data set mean is {}".format(datum['label'].mean()))
			for m in models:
				print("{} classifier mean is {}".format(m.capitalize(), datum[m].mean()))		
		except:
			pass






