import pandas as pd
import numpy as np
import sys
import json

#access code
sys.path.append('/Users/zive/GDrive/research/scalable/TuringBox/web/api')
import utils

def call(path_to_data):
	df = pd.read_csv(path_to_data)
	x = np.matrix(df[['bot1', 'bot2','bot3', 'bot4','bot5', 'bot6']])
	hidden = np.matmul(x,np.transpose(x))
	yhat = np.sqrt(np.sum(hidden))
	return yhat

if __name__ == "__main__":
	utils.turing_box(call, sys.argv)
	
