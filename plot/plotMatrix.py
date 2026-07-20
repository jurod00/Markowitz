from mathematics.covariance import Covariance
from portfolio.portfolio import Portfolio

import math
import numpy as np
import matplotlib.pyplot as plt

class PlotMatrix:

    def __init__(self, portfolio: Portfolio, covariance: Covariance=None):
        self.portfolio = portfolio

        self.covariance = covariance if covariance is not None else Covariance()

    def plotReturnMatrix(self):
        pass
    
    def plotCovarianceMatrix(self):
        sigma = self.covariance.covariance(portfolio=self.portfolio)

        fig, ax = plt.subplots()

        im = ax.matshow(sigma, cmap="coolwarm")
        fig.colorbar(im, ax=ax)

        labels = self.portfolio.symbols + self.portfolio.symbolsCall + self.portfolio.symbolsPut

        ax.set_xticks(range(len(labels)))
        ax.set_yticks(range(len(labels)))

        ax.set_xticklabels(labels, rotation=90)
        ax.set_yticklabels(labels)

        plt.show()

    def plotCorrelationMatrix(self):
        sigma = self.covariance.covariance(portfolio=self.portfolio)
        d = len(sigma)

        correlation = np.empty((d,d))
        for i in range(d):
            for j in range(d):
                denominator = math.sqrt(sigma[i,i])*math.sqrt(sigma[j,j])
                correlation[i,j] = sigma[i,j]/denominator

        fig, ax = plt.subplots()

        im = ax.matshow(correlation, cmap="RdYlGn", clim=(-1,1))
        fig.colorbar(im, ax=ax)

        labels = self.portfolio.symbols + self.portfolio.symbolsCall + self.portfolio.symbolsPut

        ax.set_xticks(range(len(labels)))
        ax.set_yticks(range(len(labels)))

        ax.set_xticklabels(labels, rotation=90)
        ax.set_yticklabels(labels)

        plt.show()