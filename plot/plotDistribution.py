from mathematics.allocations import Allocations
from mathematics.returns import Returns
from portfolio.portfolio import Portfolio

import numpy as np
import matplotlib.pyplot as plt

class PlotDistribution:

    def __init__(self, portfolio: Portfolio, allocations: Allocations=None, returns: Returns=None):
        self.portfolio = portfolio

        self.allocations = allocations if allocations is not None else Allocations()
        self.returns = returns if returns is not None else Returns()

    def plotMarginalDistribution(self):
        j0 = 2 # Component

        x = self.allocations.allocationMarkowitz(portfolio=self.portfolio, minimumReturn=0.1)
        r = self.returns.expectedReturn(portfolio=self.portfolio)

        d = len(x)

        X = np.linspace(start=0.0, stop=1.0, num=100)
        Y = []

        for x0 in X:
            delta = x0 - x[j0]
            xTemp = x

            for j in range(d):
                if j != j0:
                    xTemp[j] -= delta/(d - 1)

            Y.append(r.dot(xTemp))

        fig, ax = plt.subplots()
        ax.plot(X, Y)
        plt.show()