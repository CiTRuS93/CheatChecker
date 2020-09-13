from nltk.tokenize import word_tokenize
import pandas

class cosineStringAnalyzer(AnalyzerInterface):
    def __init__(self):
        super().__init__()
        self.df = None
    def load_data(self):
        dataset=pandas.read_csv(self.path)
        colNames = dataset.columns[dataset.columns.str.contains(pat = 'תגובות') | dataset.columns.str.contains(pat = 'דוא"ל')] 
        df = pandas.DataFrame(columns = colNames) 
        self.df = dataset[colNames]


    def analyze_data(self):
        df = pandas.DataFrame(columns = self.df.columns) 
        for i, row in self.df.iterrows():
            for j, row_2 in self.df.iterrows():
                    if row[0]!=row_2[0] and j>i:
                        new_row = []
                        new_row.append(row[0]+' '+row_2[0])
                        for k in range(1,len(row)):
                            
                            new_row.append(str_compare(row[k],row_2[k]))
                        df = df.append(pandas.Series(new_row, index=self.df.columns ), ignore_index=True)
        return df
    def str_compare(self,X,Y):
        X_list = word_tokenize(X)
        Y_list = word_tokenize(Y)

        # sw contains the list of stopwords
        #sw = stopwords.words('english')
        l1 = []
        l2 = []

        # remove stop words from the string
        X_set = {w for w in X_list}
        Y_set = {w for w in Y_list}

        # form a set containing keywords of both strings
        rvector = X_set.union(Y_set)

        for w in rvector:
            if w in X_set:
                l1.append(1)  # create a vector
            else:
                l1.append(0)
            if w in Y_set:
                l2.append(1)
            else:
                l2.append(0)
        c = 0

        # cosine formula
        for i in range(len(rvector)):
            c += l1[i]*l2[i]
        cosine = c / float((sum(l1)*sum(l2))**0.5)
        return cosine