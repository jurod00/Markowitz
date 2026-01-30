import datetime as dt
import pandas as pd
import pandas_datareader.data as pdd

class Input:

    def __init__(self):
        self.stocks = []

    data: pd.core.series.Series
    time: list
    stock: list
    stocks: list
    
    def getData(self) -> pd.core.series.Series:
        return self.data
    
    def getTime(self) -> list:
        return self.time
    
    def getStock(self) -> list:
        return self.stock
    
    def getStocks(self) -> list:
        return self.stocks

    def downloadShare(self, symbol: str, t0: dt.datetime, tn: dt.datetime):

        data = pdd.DataReader(name=[symbol], data_source="stooq", start=t0, end=tn)
        data = data.iloc[::-1]["Open"] # Datum aufsteigend sortieren und "Open"-Spalte
        data = data.iloc[:, 0] # "Symbols" entfernen
        
        self.data = data
        self.time = data.index.tolist()
        self.stock = data.tolist()

    def downloadShares(self, symbols: list, t0: dt.datetime, tn: dt.datetime):
        data = pdd.DataReader(name=symbols, data_source="stooq", start=t0, end=tn)
        data = data.iloc[::-1]["Open"]

        self.data = data
        self.time = data.index.tolist()
        self.stocks = []

        J = len(symbols)
        for j in range(J):
            self.stocks.append(data.iloc[:, j].tolist())

    def simulateData(self, shares: list, t0: dt.datetime, tn: dt.datetime):
        pass