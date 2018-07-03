import json
import pandas as pd
from time import gmtime, strftime
import numpy as np 
from IPython.display import HTML

def turing_box(algorithm, args):
	y = ""
	success = True 
	try:
		comcon = algorithm(args[1])
		y = "worked"
		comcon.to_csv("assets/comcon/{}.csv".format(args[2]))
	except Exception as e:
		print(e)
		y = str(e)
		success = False

	output = {"model_reply" : y, "data_url" : args[1], "success" : success, "time" : strftime("%Y-%m-%d %H:%M:%S", gmtime())}
	with open('assets/logs/{}.txt'.format(args[2]), 'w') as outfile:
		json.dump(output, outfile)

def evaluate_metric(metric, args):
	# try:
	output = metric(args[1])
	print(json.dumps(output))
	# except Exception as e:
		# print("metric failed")

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
        self.df = pd.read_csv(dataset_path, header=0)
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


HTML('''
    <script type="text/javascript>
        IPython.notebook.kernel.execute("URL = ' + window.location + "'")
    </script>''')

def init(URL):
    comcon = URL[URL.index('?comcon=')+8:URL.index('&')]
    df = pd.read_csv("assets/comcon/{}.csv".format(comcon))
    return df

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






