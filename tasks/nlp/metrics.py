
import numpy as np 
import pandas as pd 

class Metric: 
    def __init__(self): 
        self.dataset = None
        self.algorithm = None 
        self.df = None 
        self.ref_Z = None 
        self.comp_Z = [] 
        return 

    def set_data(self, dataset_path): 
        path_arr = dataset_path.split("/")
        box_arr = path_arr[-1].split("_")
        self.dataset = box_arr[0]
        self.algorithm = box_arr[1]
        self.df = pd.read_csv(dataset_path, header=0, names=['X', 'Z', 'Y_true', "Y_pred"], usecols=[0, 1, 2, 3])
        Z_arr = list(set(self.df['Z'].tolist()))
        self.ref_Z = self.df['Z'][0]
        for comp in Z_arr: 
            if comp != self.ref_Z: 
                self.comp_Z.append(comp)

        # add 1/0 pred
        if self.algorithm == 'azure': 
            cutoff = 0.5
        else: 
            cutoff = 0.0 

        predict = self.df['Y_pred'].tolist()
        predict = [1 if p > cutoff else 0 for p in predict]
        self.df['Y_pred_abs'] = pd.Series(predict)

        return 

    def set_ref_Z(self, ref): 
        self.ref_Z = ref 
        Z_arr = set(self.df['Z'].tolist())
        for comp in Z_arr: 
            if comp != ref: 
                self.comp_Z.append(comp)
        return 

def mean_per_class(file_df): 
    mean_dict = {}
    for name, group in file_df.groupby('Z'): 
        print(name)
        print(group.mean()['Y_true'])
        mean_dict[name] = group.mean()['Y_true']
    return mean_dict

def accuracy_per_class(file_df): 
    pass 

def false_pos_per_class(file_df): 
    pass

def false_negative_per_class(file_df): 
    pass 


if __name__ == "__main__": 

    filename = 'results/clothing_tb_results.csv'
    df = pd.read_csv(filename, header =0, names=['X', 'Z', 'Y_true', "Y_predict"], usecols=[0, 1, 2, 3])
    mean_per_class(df)

