import numpy as np
from analyzerInertface import AnalyzerInterface
import pandas
import math
from bert_serving.client import BertClient
from scipy import spatial

class bertAnalyzer(AnalyzerInterface):
    def __init__(self):
        super().__init__()
        self.df = None
        self.bc = BertClient(check_length=False)

    def load_data(self):
        dataset=pandas.read_csv(self.path)
        colNames = dataset.columns[dataset.columns.str.contains(pat = 'תגובות') | dataset.columns.str.contains(pat = 'דוא"ל') |dataset.columns.str.contains(pat = 'Response') | dataset.columns.str.contains(pat = 'Email')] 
        df = pandas.DataFrame(columns = colNames) 
        self.df = dataset[colNames]


    
    def str_compare(self,data_1,data_2):
        query_vec_1, query_vec_2 = self.bc.encode([data_1,data_2])
        cosine = np.dot(query_vec_1, query_vec_2) / (np.linalg.norm(query_vec_1) * np.linalg.norm(query_vec_2))
        return 1/(1 + math.exp(-100*(cosine - 0.95)))

    def analyze_data(self):
        df = pandas.DataFrame(columns = self.df.columns) 
        for i, row in self.df.iterrows():
            for j, row_2 in self.df.iterrows():
                    if row[0]!=row_2[0] and j>i:
                        new_row = []
                        new_row.append(row[0]+' && '+row_2[0])
                        for k in range(1,len(row)):
                            
                            new_row.append(self.str_compare(row[k].replace('\n',' '),row_2[k].replace('\n',' ')))
                        df = df.append(pandas.Series(new_row, index=self.df.columns ), ignore_index=True)
        return df