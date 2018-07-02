from metrics import Metric
import pandas as pd 
import numpy as np 

class AccDiffMetric(Metric): 
    def __init__(self): 
        self.name = 'acc_diff'
        self.dataset = None
        self.algorithm = None 
        self.df = None 
        self.ref_Z = None 
        self.comp_Z = [] 

    def calc_result(self):
        mean_dict = {}
        for name, group in self.df.groupby('Z'): 
            mean_dict[name] = len(np.where(group['Y_true'] == group['Y_pred_abs'])[0])/len(group)
        comp_dict = {} 
        for comp in self.comp_Z: 
            comp_dict[comp] = mean_dict[comp] - mean_dict[self.ref_Z]
        return comp_dict

def call(path_to_comcon): 
    metric = AccDiffMetric() 
    metric.set_data(path_to_comcon)
    acc_dict = metric.calc_result()
    return acc_dict

if __name__ == "__main__": 
    evaluate_metric(call, sys.argv)
