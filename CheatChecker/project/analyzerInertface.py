class AnalyzerInterface:

    def __init__(self):
        super().__init__()
        self.path = ""


    def set_data_path(self,path:str):
        self.path = path

    def load_data(self):
        pass

    def analyze_data(self):
        pass