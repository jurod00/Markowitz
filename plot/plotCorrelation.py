from portfolio.portfolio import Portfolio
from mathematics.returns import Returns

import matplotlib.pyplot as plt

class PlotCorrelation:

    def __init__(self, portfolio: Portfolio, returns: Returns=None):
        self.portfolio = portfolio

        self.returns = returns if returns is not None else Returns()

    def plotCorrelationStockCall(self):
        r = self.returns.expectedReturn(portfolio=self.portfolio)

        x = []
        y = []

        i0 = len(self.portfolio.symbols)

        for j0, j in enumerate(self.portfolio.indicesCall):
            x.append(r[j])
            y.append(r[i0+j0])

        fig, ax = plt.subplots()
        ax.scatter(x=x, y=y)
        plt.show()

    def plotCorrelationStockPut(self):
        r = self.returns.expectedReturn(portfolio=self.portfolio)

        x = []
        y = []

        i0 = len(self.portfolio.symbols) + len(self.portfolio.symbolsCall)

        for j0, j in enumerate(self.portfolio.indicesPut):
            x.append(r[j])
            y.append(r[i0+j0])

        fig, ax = plt.subplots()
        ax.scatter(x=x, y=y)
        plt.show()

    def plotCorrelationCallPut(self):
        pass

    def plotCorrelationStockCallPut(self):
        # 3D Plot
        pass