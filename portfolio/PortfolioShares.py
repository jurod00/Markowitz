import numpy as np
import pandas as pd
import datetime as dt

from simulation import GeometricBrownianMotion as Gbm
from util import Time

from iO import Input
from iO.database import ReadDatabase

class PortfolioShares:

    def __init__(self, time: list, symbols: list):
        self.time = time
        self.stocks = []
        self.symbols = symbols

    def getStocks(self) -> list:
        return self.stocks
    
    def setStocks(self, stocks) -> None:
        self.stocks = stocks
    
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

    allocation : list

    def getAllocation(self) -> list:
        return self.allocation