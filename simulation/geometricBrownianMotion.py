import numpy as np

from mathematics.financialMathematics import FinancialMathematics as FiMa

class GeometricBrownianMotion:

    # def __init__(self, time: list):
    #     self.time = time

    def __init__(self):
        self.times = None
        self.stock = None

        self.s0 = None
        self.drift = None
        self.volatility = None

        self.seed = None

    def getStock(self) -> list:
        return self.stock

    def setTimes(self, times: list) -> None:
        self.times = times
    
    def setS0(self, s0: float) -> None:
        self.s0 = s0

    def setDrift(self, drift: float) -> None:
        self.drift = drift

    def setVolatility(self, volatility: float) -> None:
        self.volatility = volatility

    def setSeed(self, seed: float) -> None:
        self.seed = seed

    def simulateExp(self) -> None:
        np.random.seed(self.seed)

        self.stock = [self.s0]
        n = len(self.times) - 1
        
        for i in range(n):
            stockPrev = self.stock[-1]

            dt = (self.times[i+1] - self.times[i])/(self.times[-1] - self.times[0])
            my = self.drift - 0.5*self.volatility**2

            stockNext = stockPrev*np.exp(my*dt + self.volatility*np.random.normal(0, dt**0.5))
            self.stock.append(stockNext)

    def simulatePDE(self) -> None:
        np.random.seed(self.seed)

        self.stock = [self.s0]
        n = len(self.times) - 1

        for i in range(n):
            stockPrev = self.stock[-1]

            dt = (self.times[i+1] - self.times[i])/(self.times[-1] - self.times[0])
            dS = self.drift*stockPrev*dt + self.volatility*stockPrev*np.random.normal(0, dt**0.5)

            stockNext = stockPrev + dS
            self.stock.append(stockNext)