import pandas as pd
import numpy as np
import sys
import json

#access code
sys.path.append('/Users/zive/GDrive/research/machine-behavior/turingbox/api')
from utils import turing_box

def function(row):
	return row['bot1'] + row['bot2'] + row['bot3'] + row['bot4'] + row['bot5'] + row['bot6']

def call(path_to_data):
	df = pd.read_csv(path_to_data)
	df['Y_pred'] = [0 for i in range(0,df.shape[0])]
	for index,row in df.iterrows():
		try:
			df.loc[index,'Y_pred'] = function(row)
		except:
			df.loc[index,'Y_pred'] = -1
	return df

if __name__ == "__main__":
	turing_box(call, sys.argv)
	
