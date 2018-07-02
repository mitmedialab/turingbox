import pandas as pd
import sys
import numpy as np
sys.path.append('/Users/zive/GDrive/research/machine-behavior/turingbox/api')
from utils import evaluate_metric, Metric

class MeanDiffMetric(Metric): 
    def __init__(self): 
        self.name = 'mean_diff'
        self.dataset = None
        self.algorithm = None 
        self.df = None 
        self.ref_Z = None 
        self.comp_Z = [] 

    def calc_result(self): 
        mean_dict = {}
        for name, group in self.df.groupby('Z'): 
            mean_dict[name] = group.mean()['Y_true']
        comp_dict = {} 
        for comp in self.comp_Z: 
            comp_dict[comp] = mean_dict[comp] - mean_dict[self.ref_Z]
        comp_dict['ref'] = str(self.ref_Z)
        return comp_dict

def call(path_to_comcon): 
    metric = MeanDiffMetric() 
    metric.set_data(path_to_comcon)
    mean_dict = metric.calc_result()
    return mean_dict

if __name__ == "__main__": 
    evaluate_metric(call, sys.argv)
