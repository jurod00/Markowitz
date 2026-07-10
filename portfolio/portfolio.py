import pandas as pd
import pathlib as pl
import datetime as dt

class Portfolio:

    def __init__(self):

        self.times: list=[]
        self.stocks: list=[]
        self.symbols: list=[]

        self.riskFreeRate: float=float(0.00)

        self.premiumCall: list=[]
        self.strikesCall: list=[]
        self.implVolCall: list=[]
        self.indicesCall: list=[]
        self.symbolsCall: list=[]

        self.premiumPut: list=[]
        self.strikesPut: list=[]
        self.implVolPut: list=[]
        self.indicesPut: list=[]
        self.symbolsPut: list=[]

    def setTimes(self, times: list) -> None:
        self.times = times

    def setStocks(self, stocks: list) -> None:
        self.stocks = stocks

    def setSymbols(self, symbols: list) -> None:
        self.symbols = symbols
        
        
    def setRiskFreeRate(self, riskFreeRate: float) -> None:
        self.riskFreeRate = riskFreeRate

    
    def setPremiumCall(self, premiumCall: list) -> None:
        self.premiumCall = premiumCall

    def setStrikesCall(self, strikesCall: list) -> None:
        self.strikesCall = strikesCall

    def setImplVolCall(self, implVolCall: list) -> None:
        self.implVolCall = implVolCall

    def setIndicesCall(self, indicesCall: list) -> None:
        self.indicesCall = indicesCall

    def setSymbolsCall(self, symbolsCall: list) -> None:
        self.symbolsCall = symbolsCall

    
    def setPremiumPut(self, premiumPut: list) -> None:
        self.premiumPut = premiumPut

    def setStrikesPut(self, strikesPut: list) -> None:
        self.strikesPut = strikesPut

    def setImplVolPut(self, implVolPut: list) -> None:
        self.implVolPut = implVolPut

    def setIndicesPut(self, indicesPut: list) -> None:
        self.indicesPut = indicesPut

    def setSymbolsPut(self, symbolsPut: list) -> None:
        self.symbolsPut = symbolsPut

    def setStockDataFromCSV(self, fileName: str="master.csv") -> None:
        pathDatabase = pl.Path(__file__).resolve().parent.parent / "iO" / "database"
        data = pd.read_csv(pathDatabase / fileName, delimiter=";").set_index("Date")
        
        self.setTimes([dt.datetime.strptime(time, "%Y-%m-%d") for time in data.index.tolist()])
        self.setStocks([data.iloc[:,j].tolist() for j in range(len(data.columns))])
        self.setSymbols(data.columns.values.tolist())

    def setOptionDataFromCSV(self, fileName: str="option.csv", symbolsOptions: list=None) -> None:
        if symbolsOptions == None:
            return None
        
        pathDatabase = pl.Path(__file__).resolve().parent.parent / "iO" / "database"
        data = pd.read_csv(pathDatabase / fileName, delimiter=";", index_col=0)

        d = len(self.symbols)
        
        for symbolOption in symbolsOptions:
            dataSymb = data.loc[:,symbolOption]

            self.riskFreeRate = dataSymb["riskFreeRate"]

            if "Call" in symbolOption:
                self.premiumCall.append(dataSymb["premium"])
                self.strikesCall.append(dataSymb["strikes"])
                self.implVolCall.append(dataSymb["implVol"])

                for j in range(d):
                    if symbolOption[:-5] == self.symbols[j]:
                        self.indicesCall.append(j)
                        break

                self.symbolsCall.append(symbolOption)

            if "Put" in symbolOption:
                self.premiumPut.append(dataSymb["premium"])
                self.strikesPut.append(dataSymb["strikes"])
                self.implVolPut.append(dataSymb["implVol"])

                for j in range(d):
                    if symbolOption[:-4] == self.symbols[j]:
                        self.indicesPut.append(j)
                        break

                self.symbolsPut.append(symbolOption)