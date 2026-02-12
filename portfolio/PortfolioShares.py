import numpy as np
import pandas as pd
import datetime as dt
import scipy.optimize as opt

from simulation import GeometricBrownianMotion as Gbm
from util import Time

from iO import Input

from util import AuxiliaryQuantities as Aq

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
    
    def setSymbols(self, symbols) -> list:
        self.symbols = symbols
    
    def downloadPortfolio(self) -> None:
        input = Input()
        input.downloadShares(self.symbols, self.time[0], self.time[-1])

        self.time = input.getTime()
        self.stocks = input.getStocks()
    
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
        data = pd.read_csv(r"C:\Users\j.rode\Desktop\Markowitz\iO\database\lecture.csv", delimiter=";").set_index("Date")
        
        self.symbols = data.columns.values.tolist()

        timeTemp = data.index.tolist()
        self.time = [dt.datetime.strptime(t, "%Y-%m-%d") for t in timeTemp]

        self.stocks = []
        J = len(self.symbols)

        for j in range(J):
            self.stocks.append(data.iloc[:, j].tolist())

    def addRiskFreeAsset(self, symbol: str="risk-free asset", interestRate: float=0.02):
        aq = Aq()
        n = aq.numberTimestamps(self.time)

        self.symbols.append(symbol)

        stock = [100.0]
        for i in range(n):
            stock.append(stock[i]*np.exp(1/n*interestRate))

        self.stocks.append(stock)


    def calculateAllocationBasic(self, my0: float=0.0, my1: float=0.25) -> None:
        aq = Aq()
        self.x0 = aq.allocationBasic(self.time, self.stocks, my0)
        self.x1 = aq.allocationBasic(self.time, self.stocks, my1)

        self.a, self.b, self.c, self.d = aq.abcdQuantities(self.time, self.stocks)

        self.my0 = my0
        self.my1 = my1

    def calculateAllocationUtilityMaximization(self, kappas: list) -> None:
        aq = Aq()
        self.kappas = kappas
        self.xSet = []

        for kappa in kappas:
            x = aq.allocationUtilityMaximization(self.time, self.stocks, kappa)
            self.xSet.append(x)

    def calculateAllocationLinearProgram(self, mySet: list) -> None:
        aq = Aq()

        c = aq.objectiveCostVector(self.time, self.stocks, 0.95, 1)
        bounds = aq.constraintsBounds(self.time, self.stocks)

        self.mySet = mySet
        self.xSet = []

        J = aq.numberStocks(self.stocks)
        for my in mySet:
            A_ub = aq.constraintsInequality(self.time, self.stocks, my, "left")
            A_eq = aq.constraintsEquality(self.time, self.stocks, "left")

            b_ub = aq.constraintsInequality(self.time, self.stocks, my, "right")
            b_eq = aq.constraintsEquality(self.time, self.stocks, "right")

            solution = opt.linprog(
                c=c, 
                A_ub=A_ub, 
                b_ub=b_ub, 
                A_eq=A_eq, 
                b_eq=b_eq, 
                bounds=bounds, 
                method="highs")
            
            x = solution.x[:J]
            print(sum(x))
            print(x)
            self.xSet.append(x)

    def getX0(self):
        return self.x0
    
    def getX1(self):
        return self.x1
    
    def getMy0(self):
        return self.my0
    
    def getMy1(self):
        return self.my1
    
    def getA(self) -> float:
        return self.a
    
    def getB(self) -> float:
        return self.b
    
    def getC(self) -> float:
        return self.c
    
    def getD(self) -> float:
        return self.d
    
    def getKappas(self) -> list:
        return self.kappas
    
    def getMySet(self) -> list:
        return self.mySet
    
    def getXSet(self) -> list:
        return self.xSet