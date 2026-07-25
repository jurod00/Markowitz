from mathematics.covariance import Covariance
from portfolio.portfolio import Portfolio

import math
import numpy as np
import pathlib as pl
import matplotlib.pyplot as plt

class PlotMatrix:

    def __init__(self, portfolio: Portfolio, covariance: Covariance=None):
        # Memory
        self.portfolio = portfolio
        # Optional Dependency Injection
        self.covariance = covariance if covariance is not None else Covariance()

        plt.rcParams.update(
            {
                "font.size": 14,
                "axes.titlesize": 14,
                "axes.labelsize": 14,
                "xtick.labelsize": 14,
                "ytick.labelsize": 14,
                "legend.fontsize": 14,
            }
        )

    def plotReturnMatrix(self):
        pass
    
    def plotCovarianceMatrix(self, format: str="svg"):
        sigma = self.covariance.covariance(portfolio=self.portfolio)

        # np.set_printoptions(threshold=np.inf, linewidth=np.inf)
        # print(sigma)

        fig, ax = plt.subplots(figsize=(6, 6), layout="constrained")

        im = ax.matshow(sigma, cmap="RdYlGn", clim=(-100, 100))

        tolerance = 1e-12

        for (row, col), value in np.ndenumerate(sigma):
            if value > tolerance:
                sign = "+"
            elif value < -tolerance:
                sign = "−"
            else:
                sign = "0"

            ax.text(
                col,
                row,
                sign,
                ha="center",
                va="center",
                color="black",
                fontsize=10
            )

        fig.colorbar(
            im,
            ax=ax,
            shrink=0.8,
            fraction=0.05
        )

        labels = self.portfolio.symbols + self.portfolio.symbolsCall + self.portfolio.symbolsPut

        ax.set_xticks(range(len(labels)))
        ax.set_yticks(range(len(labels)))

        ax.set_xticklabels(labels, rotation=90)
        ax.set_yticklabels(labels)

        pathAssets = pl.Path(__file__).resolve().parent / "assets"
        pathAssets.mkdir(exist_ok=True)

        fig.savefig(pathAssets / f"plotCovarianceMatrix.{format}", bbox_inches="tight", pad_inches=0.05)

    def plotCorrelationMatrix(self, format: str="svg"):
        sigma = self.covariance.covariance(portfolio=self.portfolio)
        d = len(sigma)

        correlation = np.empty((d,d))
        for i in range(d):
            for j in range(d):
                denominator = math.sqrt(sigma[i,i])*math.sqrt(sigma[j,j])
                correlation[i,j] = sigma[i,j]/denominator

        fig, ax = plt.subplots(figsize=(6, 6), layout="constrained")

        im = ax.matshow(correlation, cmap="RdYlGn", clim=(-1,1))

        tolerance = 1e-12

        for (row, col), value in np.ndenumerate(correlation):
            if value > tolerance:
                sign = "+"
            elif value < -tolerance:
                sign = "−"
            else:
                sign = "0"

            ax.text(
                col,
                row,
                sign,
                ha="center",
                va="center",
                color="black",
                fontsize=10
            )

        fig.colorbar(
            im,
            ax=ax,
            shrink=0.8,
            fraction=0.05
        )

        labels = self.portfolio.symbols + self.portfolio.symbolsCall + self.portfolio.symbolsPut

        ax.set_xticks(range(len(labels)))
        ax.set_yticks(range(len(labels)))

        ax.set_xticklabels(labels, rotation=90)
        ax.set_yticklabels(labels)

        pathAssets = pl.Path(__file__).resolve().parent / "assets"
        pathAssets.mkdir(exist_ok=True)

        fig.savefig(pathAssets / f"plotCorrelationMatrix.{format}", bbox_inches="tight", pad_inches=0.05)