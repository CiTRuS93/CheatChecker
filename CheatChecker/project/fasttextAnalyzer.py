import fasttext
import numpy as np
import scipy
from scipy import spatial
from analyzerInertface import AnalyzerInterface
import pandas
import math

class fasttextAnalyzer(AnalyzerInterface):
    def __init__(self):
        super().__init__()
        self.df = None
        self.model_path = "D:\hackaton\CheatChecker\CheatChecker\project\wiki-he/wiki.he.bin"
        self.model = fasttext.load_model(self.model_path)

    def load_data(self):
        dataset=pandas.read_csv(self.path)
        colNames = dataset.columns[dataset.columns.str.contains(pat = 'תגובות') | dataset.columns.str.contains(pat = 'דוא"ל')  |dataset.columns.str.contains(pat = 'Response') | dataset.columns.str.contains(pat = 'Email')] 
        df = pandas.DataFrame(columns = colNames) 
        self.df = dataset[colNames]


    
    def str_compare(self,data_1,data_2):
        sent1_emb = np.mean([self.model[x] for word in data_1 for x in word.split()],axis=0)
        sent2_emb = np.mean([self.model[x] for word in data_2 for x in word.split()],axis=0)
        
        cosine = np.dot(sent1_emb, sent2_emb) / (np.linalg.norm(sent1_emb) * np.linalg.norm(sent2_emb))
        return 1/(1 + math.exp(-100*(cosine - 0.95)))

    def analyze_data(self):
        df = pandas.DataFrame(columns = self.df.columns) 
        for i, row in self.df.iterrows():
            for j, row_2 in self.df.iterrows():
                    if row[0]!=row_2[0] and j>i:
                        new_row = []
                        new_row.append(row[0]+' && '+row_2[0])
                        for k in range(1,len(row)):
                            
                            new_row.append(self.str_compare(row[k],row_2[k]))
                        df = df.append(pandas.Series(new_row, index=self.df.columns ), ignore_index=True)
        return df