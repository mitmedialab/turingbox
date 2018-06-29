#!/usr/bin/env python
import pandas as pd
import sys
import numpy as np

sys.path.append('/Users/zive/GDrive/research/machine-behavior/turingbox/api')
from utils import evaluate_metric

def metric(path_to_comcon):
	df = pd.read_csv(path_to_comcon)
	diff = np.mean(df[df['z']]['yhat']) - np.mean(df[~df['z']]['yhat'])
	return diff 

#clarifai API 
if __name__ == "__main__":
	evaluate_metric(metric, sys.argv)