import pandas as pd

class ReadDatabase:
    def __init__(self):
        data = pd.read_csv(r"C:\Users\j.rode\Desktop\Markowitz\iO\database\lecture.csv", delimiter=";").set_index("Date")
        self.symbols = data.columns.values.tolist()
        self.data = data
        self.time = data.index.tolist()

        self.stocks = []
        J = len(self.symbols)

        for j in range(J):
            self.stocks.append(data.iloc[:, j].tolist())

    def getData(self):
        return self.data
    
    def getTime(self):
        return self.time
    
    def getStocks(self):
        return self.stocks
    
    def getSymbols(self):
        return self.symbols