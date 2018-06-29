from metrics import Metric

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
        return comp_dict

if __name__ == "__main__": 
    metric = MeanDiffMetric() 
    metric.set_data('results/clothing_tb_results.csv')
    mean_dict = metric.calc_result()

