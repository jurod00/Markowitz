from portfolio.portfolio import Portfolio
from mathematics.returns import Returns

import numpy as np
import pathlib as pl
import scipy.stats as stats
import matplotlib.ticker as mtick
import matplotlib.pyplot as plt

class PlotCorrelation:

    def __init__(self, portfolio: Portfolio, returns: Returns=None):
        # Memory
        self.portfolio = portfolio
        # Optional Dependency Injection
        self.returns = returns if returns is not None else Returns()

        plt.rcParams.update(
            {
                "font.size": 14,
                "axes.titlesize": 14,
                "axes.labelsize": 14,
                "xtick.labelsize": 12,
                "ytick.labelsize": 12,
                "legend.fontsize": 14,
            }
        )

    def plotCorrelationStockCall(self, format: str="svg"):
        r = self.returns.expectedReturn(portfolio=self.portfolio)

        x = []
        y = []

        i0 = len(self.portfolio.symbols)

        for j0, j in enumerate(self.portfolio.indicesCall):
            x.append(r[j])
            y.append(r[i0+j0])

        m, n = np.polyfit(x=x, y=y, deg=1)

        xMin = min(x)
        xMax = max(x)
        xRange = xMax - xMin

        yMin = min(y)
        yMax = max(y)
        yRange = yMax - yMin

        fig, ax = plt.subplots(figsize=(6, 6), layout="constrained")
        ax.scatter(
            x=x, 
            y=y, 
            color="green"
        )

        for i in range(len(x)):
            ax.annotate(
                self.portfolio.symbols[i], 
                (x[i], y[i]), 
                textcoords="offset points", 
                xytext=(0, 5), 
                ha="center"
            )

        ax.plot(
            [xMin - 0.1*xRange, xMax + 0.1*xRange], 
            [m*(xMin - 0.1*xRange) + n, m*(xMax + 0.1*xRange) + n], 
            color="forestgreen", 
            linewidth=1, 
            linestyle="--"
        )

        ax.text(
            x=0.05, 
            y=0.95, 
            s=fr"Pearson correlation $\rho(r_S, r_C) = {np.corrcoef(x, y)[0, 1]:.4f}$",
            transform=ax.transAxes, 
            verticalalignment="top"
        )

        # x-axis
        ax.set_xlabel("Stock Return $r_S$")
        ax.set_xlim(xMin - 0.1*xRange, xMax + 0.1*xRange)

        # y-axis
        ax.set_ylabel("Call Option Return $r_C$")
        ax.set_ylim(yMin - 0.1*yRange, yMax + 0.1*yRange)

        pathAssets = pl.Path(__file__).resolve().parent / "assets"
        pathAssets.mkdir(exist_ok=True)

        fig.savefig(pathAssets / f"plotCorrelationStockCall.{format}", bbox_inches="tight", pad_inches=0.05)

    def plotCorrelationStockPut(self, format: str="svg"):
        r = self.returns.expectedReturn(portfolio=self.portfolio)

        x = []
        y = []

        i0 = len(self.portfolio.symbols) + len(self.portfolio.symbolsCall)

        for j0, j in enumerate(self.portfolio.indicesPut):
            x.append(r[j])
            y.append(r[i0+j0])

        m, n = np.polyfit(x=x, y=y, deg=1)

        xMin = min(x)
        xMax = max(x)
        xRange = xMax - xMin

        yMin = min(y)
        yMax = max(y)
        yRange = yMax - yMin

        fig, ax = plt.subplots(figsize=(6, 6), layout="constrained")
        ax.scatter(
            x=x, 
            y=y, 
            color="green"
        )

        for i in range(len(x)):
            ax.annotate(
                self.portfolio.symbols[i], 
                (x[i], y[i]), 
                textcoords="offset points", 
                xytext=(0, 5), 
                ha="center"
            )

        ax.plot(
            [xMin - 0.1*xRange, xMax + 0.1*xRange], 
            [m*(xMin - 0.1*xRange) + n, m*(xMax + 0.1*xRange) + n], 
            color="forestgreen", 
            linewidth=1, 
            linestyle="--"
        )

        ax.text(
            x=0.20, 
            y=0.95, 
            s=fr"Pearson correlation $\rho(r_S, r_P) = {np.corrcoef(x, y)[0, 1]:.4f}$",
            transform=ax.transAxes, 
            verticalalignment="top"
        )

        # x-axis
        ax.set_xlabel("Stock Return $r_S$")
        ax.set_xlim(xMin - 0.1*xRange, xMax + 0.1*xRange)

        # y-axis
        ax.set_ylabel("Put Option Return $r_P$")
        ax.set_ylim(yMin - 0.1*yRange, yMax + 0.1*yRange)

        pathAssets = pl.Path(__file__).resolve().parent / "assets"
        pathAssets.mkdir(exist_ok=True)

        fig.savefig(pathAssets / f"plotCorrelationStockPut.{format}", bbox_inches="tight", pad_inches=0.05)

    def plotCorrelationCallPut(self, format: str="svg"):
        if self.portfolio.indicesCall != self.portfolio.indicesPut:
            raise ValueError("The indices of call options and put options must be the same.")
        
        r = self.returns.expectedReturn(portfolio=self.portfolio)

        x = []
        y = []

        i0 = len(self.portfolio.symbols)

        for i in range(len(self.portfolio.symbols)):
            x.append(r[i0+i])
            y.append(r[2*i0+i])

        m, n = np.polyfit(x=x, y=y, deg=1)

        xMin = min(x)
        xMax = max(x)
        xRange = xMax - xMin

        yMin = min(y)
        yMax = max(y)
        yRange = yMax - yMin

        fig, ax = plt.subplots(figsize=(6, 6), layout="constrained")
        ax.scatter(
            x=x, 
            y=y, 
            color="green"
        )

        for i in range(len(x)):
            ax.annotate(
                self.portfolio.symbols[i], 
                (x[i], y[i]), 
                textcoords="offset points", 
                xytext=(0, 5), 
                ha="center"
            )

        ax.plot(
            [xMin - 0.1*xRange, xMax + 0.1*xRange], 
            [m*(xMin - 0.1*xRange) + n, m*(xMax + 0.1*xRange) + n], 
            color="forestgreen", 
            linewidth=1, 
            linestyle="--"
        )

        ax.text(
            x=0.20, 
            y=0.95, 
            s=fr"Pearson correlation $\rho(r_C, r_P) = {np.corrcoef(x, y)[0, 1]:.4f}$",
            transform=ax.transAxes, 
            verticalalignment="top"
        )

        # x-axis
        ax.set_xlabel("Call Option Return $r_C$")
        ax.set_xlim(xMin - 0.1*xRange, xMax + 0.1*xRange)

        # y-axis
        ax.set_ylabel("Put Option Return $r_P$")
        ax.set_ylim(yMin - 0.1*yRange, yMax + 0.1*yRange)

        pathAssets = pl.Path(__file__).resolve().parent / "assets"
        pathAssets.mkdir(exist_ok=True)

        fig.savefig(pathAssets / f"plotCorrelationCallPut.{format}", bbox_inches="tight", pad_inches=0.05)

    def plotCorrelationStockCallPut(self, format: str="svg"):
        # 3D Plot
        pass