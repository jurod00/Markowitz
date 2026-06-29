import numpy as np
import pandas as pd
import datetime as dt
import scipy.optimize as opt

from mathematics.financialMathematics import FinancialMathematics as FiMa
from simulation.geometricBrownianMotion import GeometricBrownianMotion as Gbm
# from iO.input import Input

class PortfolioShares:

    def __init__(self):
        self.time = []
        self.stocks = []
        self.symbols = []

    def getTime(self) -> list:
        return self.time
    
    def setTime(self, time) -> None:
        self.time = time

    def getStocks(self) -> list:
        return self.stocks
    
    def setStocks(self, stocks) -> None:
        self.stocks = stocks

    def getSymbols(self) -> list:
        return self.symbols
    
    def setSymbols(self, symbols) -> None:
        self.symbols = symbols
    
    # def downloadPortfolio(self) -> None:
    #     input = Input()
    #     input.downloadShares(self.symbols, self.time[0], self.time[-1])

    #     self.time = input.getTime()
    #     self.stocks = input.getStocks()
    
    def simulatePortfolio(self, s0: list, drift: list, volatility: list) -> None:
        J = len(self.symbols)

        if len(s0) != J or len(drift) != J or len(volatility) != J:
            print("Übergebene Listen müssen diesselbe Größe wie Symbols haben!")
            return None
        
        gbm = Gbm(self.time)
        
        for j in range(J):
            gbm.setS0(s0[j])
            gbm.setDrift(drift[j])
            gbm.setVolatility(volatility[j])

            gbm.setSeed(j)
            gbm.simulate()

            self.stocks.append(gbm.getStock())

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

    # def addRiskFreeAsset(self, symbol: str="risk-free asset", interestRate: float=0.02):
    #     n = FiMa.numberTimestamps(time=self.time)

    #     self.symbols.append(symbol)

    #     stock = [100.0]
    #     for i in range(n):
    #         stock.append(stock[i]*np.exp(1/n*interestRate))

    #     self.stocks.append(stock)