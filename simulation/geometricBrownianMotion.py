import numpy as np

from mathematics.financialMathematics import FinancialMathematics as FiMa

class GeometricBrownianMotion:

    def __init__(self, time: list):
        self.time = time

    def getStock(self) -> list:
        return self.stock
    
    def setS0(self, s0: float) -> None:
        self.s0 = s0

    def setDrift(self, drift: float) -> None:
        self.drift = drift

    def setVolatility(self, volatility: float) -> None:
        self.volatility = volatility

    def setSeed(self, s) -> None:
        np.random.seed(s)

    def simulate(self):
        self.stock = []
        self.stock.append(self.s0)

        n = FiMa.numberTimestamps(time=self.time)
        prob = FiMa.prob(time=self.time)
        
        for i in range(n):
            stockPrev = self.stock[i]
            stockNext = stockPrev*np.exp((self.drift - self.volatility**2/2)*prob[i] + self.volatility*np.random.normal(0, np.sqrt(prob[i])))
            self.stock.append(stockNext)