import numpy as np
import pandas as pd
import datetime as dt
import scipy.optimize as opt

from mathematics.financialMathematics import FinancialMathematics as FiMa
from simulation.geometricBrownianMotion import GeometricBrownianMotion as Gbm
# from iO.input import Input

class PortfolioSharesOptions:

    def __init__(self):
        self.time : list=None
        self.stocks : list=None
        self.options : dict=None
        self.symbols : list=None

    def getTime(self) -> list:
        return self.time
    
    def setTime(self, time: list) -> None:
        self.time = time

    def getStocks(self) -> list:
        return self.stocks
    
    def setStocks(self, stocks: list) -> None:
        self.stocks = stocks

    def getOptions(self) -> dict:
        return self.options
    
    def setOptions(self, options: dict) -> None:
        self.options = options
        self.addSymbols()

    def getSymbols(self) -> list:
        return self.symbols
    
    def setSymbols(self, symbols: list) -> None:
        self.symbols = symbols

    def addSymbols(self):
        for callIndex in self.options["callIndices"]:
            self.symbols += ["Call " + str(callIndex)]
        for putIndex in self.options["putIndices"]:
            self.symbols += ["Put " + str(putIndex)]

    def databasePortfolio(self) -> None:
        # data = pd.read_csv(r"C:\Users\j.rode\Desktop\Markowitz\iO\database\lecture.csv", delimiter=";").set_index("Date")
        data = pd.read_csv(r"C:\Users\j.rode\Desktop\Markowitz\iO\database\master.csv", delimiter=";").set_index("Date")
        
        self.symbols = data.columns.values.tolist()

        timeTemp = data.index.tolist()
        self.time = [dt.datetime.strptime(t, "%Y-%m-%d") for t in timeTemp]

        self.stocks = []
        J = len(self.symbols)

        for j in range(J):
            self.stocks.append(data.iloc[:, j].tolist())