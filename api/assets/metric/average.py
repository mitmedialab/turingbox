#!/usr/bin/env python
import pandas as pd
import sys
import numpy as np

sys.path.append('/Users/zive/GDrive/research/machine-behavior/turingbox/api')
from utils import evaluate_metric

def metric(df,label,referent):
	diff = np.mean(df[df['z'] == label]['yhat']) - np.mean(df[df['z'] == referent]['yhat'])
	return diff 

def call(path_to_comcon):
	df = pd.read_csv(path_to_comcon)
	levels = list(df['z'].value_counts().index)
	referent = levels[0]
	levels.remove(referent)
	return [{"label" : label, "referent" : referent, "output" : metric(df,label,referent)} for label in levels]

#clarifai API 
if __name__ == "__main__":
	evaluate_metric(call, sys.argv)