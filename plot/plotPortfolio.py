from mathematics.options import Options
from mathematics.returns import Returns
from mathematics.allocations import Allocations
from mathematics.stochastics import Stochastics
from portfolio.portfolio import Portfolio

import math
import numpy as np
import pathlib as pl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

cmap = plt.get_cmap("Greens")
markerNumber = 25

class PlotPortfolio:
    
    def __init__(self, portfolio: Portfolio):
        self.portfolio = portfolio

    def markers(self) -> list:
        stocks = list(self.portfolio.stocks)

        indicesCall = list(self.portfolio.indicesCall)
        indicesPut = list(self.portfolio.indicesPut)

        if len(stocks) == 1:
            stockMarkers = ["^"]
        elif len(stocks) == 2:
            stockMarkers = ["^", "s"]
        elif len(stocks) == 3:
            stockMarkers = ["^", "s", "o"]
        elif len(stocks) == 4:
            stockMarkers = ["^", "s", "o", "*"]
        elif len(stocks) == 5:
            stockMarkers = ["^", "s", "o", "*", "X"]

        if not indicesCall and not indicesPut:
            return stockMarkers
        elif indicesCall and not indicesPut or not indicesCall and indicesPut:
            return 2*stockMarkers
        elif indicesCall and indicesPut:
            return 3*stockMarkers

        return None
    
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------
    #                                                                           Stocks
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------

    def plotStocks(self, absRel: str="rel") -> None:
        times = list(self.portfolio.times)
        stocks = list(self.portfolio.stocks)
        symbols = list(self.portfolio.symbols)

        d = len(stocks)

        fig, ax = plt.subplots()
        if absRel == "abs":
            for j, stock in enumerate(stocks):
                ax.plot(
                    times, 
                    stock, 
                    color=cmap((j+1)/d), 
                    label=symbols[j]
                )
            ax.set_ylabel("absolute stock prices " + r"$S_t$")

        if absRel == "rel":
            for j, stock in enumerate(stocks):
                stocksRel = [stock[i]/stock[0] for i in range(len(times))]
                ax.plot(
                    times, 
                    stocksRel, 
                    color=cmap((j+1)/d), 
                    label=symbols[j]
                )
            ax.set_ylabel("relative stock prices " + r"$S_t\,/\,S_0$")
        
        ax.xaxis.set_major_formatter(mdates.DateFormatter(r"%m-%d"))
        
        ax.legend(loc="upper center", ncol=d, frameon=False)
        ax.set_xlim(times[0], times[-1])

        plt.xticks(rotation=45)
        # plt.show()

        pathAssets = pl.Path(__file__).resolve().parent / "assets"
        pathAssets.mkdir(exist_ok=True)

        fig.savefig(pathAssets / "plotStocks.svg")

    # ------------------------------------------------------------------------------------------------------------------------------------------------------------
    #                                                                           Allocations
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    def plotStackedBar(self, allocation: np.ndarray=None, minimumReturn: float=None, alpha: float=None, beta: float=None, riskAversion: float=None) -> None:
        if allocation is not None:
            symbols = list(self.portfolio.symbols)
            d = len(allocation)

            fig, ax = plt.subplots(figsize=(10, 2))
            for i in range(d):
                left = (0 if i == 0 else sum(allocation[:i]))
                ax.barh(
                    y=[0], 
                    width=allocation[i], 
                    left=left, 
                    color=cmap((i+1)/d), 
                    label=symbols[i]
                )
                ax.text(
                    x=left+0.5*allocation[i], 
                    y=-0.05, 
                    s="{:.2f}".format(100*allocation[i]) + "%", 
                    ha="center", 
                    color="white", 
                    weight="bold", 
                    size=10
                )
            
            ax.set_axis_off()
            ax.set_xlim(0, 1)
            ax.set_ylim(-1, 1)
            ax.legend(loc="upper center", ncol=d, frameon=False)

            # plt.show()

            pathAssets = pl.Path(__file__).resolve().parent / "assets"
            pathAssets.mkdir(exist_ok=True)

            fig.savefig(pathAssets / "plotStackedBar.svg")

        if minimumReturn is not None and (alpha is None or beta is None): # Markowitz
            symbols = list(self.portfolio.symbols)
            x = Allocations.allocationMarkowitz(portfolio=self.portfolio, minimumReturn=minimumReturn)
            d = len(x)

            fig, ax = plt.subplots(figsize=(10, 2))
            for i in range(d):
                left = (0 if i == 0 else sum(x[:i]))
                ax.barh(
                    y=[0], 
                    width=x[i], 
                    left=left, 
                    color=cmap((i+1)/d), 
                    label=symbols[i]
                )
                ax.text(
                    x=left+0.5*x[i], 
                    y=-0.05, 
                    s="{:.2f}".format(100*x[i]) + "%", 
                    ha="center", 
                    color="white", 
                    weight="bold", 
                    size=10
                )
            
            ax.set_axis_off()
            ax.set_xlim(0, 1)
            ax.set_ylim(-1, 1)
            ax.legend(loc="upper center", ncol=d, frameon=False)

            # plt.show()

            pathAssets = pl.Path(__file__).resolve().parent / "assets"
            pathAssets.mkdir(exist_ok=True)

            fig.savefig(pathAssets / "plotStackedBar.svg")

        if minimumReturn is not None and alpha is not None and beta is not None: # IntegratedRiskManagement
            pass
        if riskAversion is not None: # UtilityMaximization
            pass

    def plotAllocationMarkowitz(self, returnMin: float=0.0, returnMax: float=0.25) -> None:
        marker = ["^", "s", "o", "*", "X"]

        symbolsStock = list(self.portfolio.symbols)
        symbolsCall = list(self.portfolio.symbolsCall)
        symbolsPut = list(self.portfolio.symbolsPut)
        
        indicesCall = list(self.portfolio.indicesCall)
        indicesPut = list(self.portfolio.indicesPut)

        d0 = len(symbolsStock)
        d1 = len(symbolsCall)
        d2 = len(symbolsPut)

        mys = np.linspace(returnMin, returnMax, markerNumber)
        
        x0 = Allocations.allocationMarkowitz(portfolio=self.portfolio, minimumReturn=returnMin)
        x1 = Allocations.allocationMarkowitz(portfolio=self.portfolio, minimumReturn=returnMax)
        
        fig, ax = plt.subplots()
        for j in range(d0):
            m = (x1[j] - x0[j])/(returnMax - returnMin)
            n = x0[j] - m*returnMin

            xj = m*mys + n
            
            ax.plot(
                mys, 
                xj, 
                color=cmap(1/3), 
                label=symbolsStock[j], 
                marker=marker[j], 
                markeredgecolor=cmap(1/3), 
                markerfacecolor="white"
            )
        for j0, j in enumerate(indicesCall):
            m = (x1[d0+j0] - x0[d0+j0])/(returnMax - returnMin)
            n = x0[d0+j0] - m*returnMin

            xj = m*mys + n
            
            ax.plot(
                mys, 
                xj, 
                color=cmap(2/3), 
                label=symbolsCall[j0], 
                marker=marker[j], 
                markeredgecolor=cmap(2/3), 
                markerfacecolor="white"
            )
        for j0, j in enumerate(indicesPut):
            m = (x1[d0+d1+j0] - x0[d0+d1+j0])/(returnMax - returnMin)
            n = x0[d0+d1+j0] - m*returnMin

            xj = m*mys + n
            
            ax.plot(
                mys, 
                xj, 
                color=cmap(1.0), 
                label=symbolsPut[j0], 
                marker=marker[j], 
                markeredgecolor=cmap(1.0), 
                markerfacecolor="white"
            )
        ax.hlines(y=0, xmin=returnMin, xmax=returnMax, linewidth=1, color="black", zorder=-1)

        ax.set_xlabel("minimum return " + r"$\mu$")
        ax.set_ylabel("allocation " + r"$x^*(\mu)$")

        ax.set_xlim(returnMin, returnMax)
        # ax.set_ylim(-10, 10)
        # ax.set_ylim(-0.05, 1.05)

        ax.legend(loc="upper center", ncol=3, frameon=False)

        plt.subplots_adjust(bottom=0.1, top=0.975, left=0.09, right=0.975)
        # plt.show()

        pathAssets = pl.Path(__file__).resolve().parent / "assets"
        pathAssets.mkdir(exist_ok=True)

        fig.savefig(pathAssets / "plotAllocationMarkowitz.svg")

    def plotAllocationUtilityMaximization(self, riskAversionMin: float=float(1e-1), riskAversionMax: float=float(1e+6)) -> None:
        marker = ["^", "s", "o", "*", "X"]

        symbolsStock = list(self.portfolio.symbols)
        symbolsCall = list(self.portfolio.symbolsCall)
        symbolsPut = list(self.portfolio.symbolsPut)
        
        indicesCall = list(self.portfolio.indicesCall)
        indicesPut = list(self.portfolio.indicesPut)

        d0 = len(symbolsStock)
        d1 = len(symbolsCall)
        d2 = len(symbolsPut)

        base = 10
        start = np.log(riskAversionMin)/np.log(base)
        stop = np.log(riskAversionMax)/np.log(base)

        kappas = np.logspace(start=start, stop=stop, num=markerNumber, endpoint=True, base=base)

        fig, ax = plt.subplots()
        for j in range(d0):

            xj = [Allocations.allocationUtilityMaximization(portfolio=self.portfolio, riskAversion=kappa)[j] for kappa in kappas]

            ax.plot(
                kappas, 
                xj, 
                color=cmap(1/3), 
                label=symbolsStock[j], 
                marker=marker[j], 
                markeredgecolor=cmap(1/3), 
                markerfacecolor="white"
            )
        for j0, j in enumerate(indicesCall):

            xj = [Allocations.allocationUtilityMaximization(portfolio=self.portfolio, riskAversion=kappa)[d0+j0] for kappa in kappas]

            ax.plot(
                kappas, 
                xj, 
                color=cmap(2/3), 
                label=symbolsCall[j0], 
                marker=marker[j], 
                markeredgecolor=cmap(2/3), 
                markerfacecolor="white"
            )
        for j0, j in enumerate(indicesPut):

            xj = [Allocations.allocationUtilityMaximization(portfolio=self.portfolio, riskAversion=kappa)[d0+d1+j0] for kappa in kappas]

            ax.plot(
                kappas, 
                xj, 
                color=cmap(1.0), 
                label=symbolsPut[j0], 
                marker=marker[j], 
                markeredgecolor=cmap(1.0), 
                markerfacecolor="white"
            )
        ax.hlines(y=0, xmin=riskAversionMin, xmax=riskAversionMax, linewidth=1, color="black", zorder=-1)

        ax.set_xlabel("risk aversion " + r"$\kappa$")
        ax.set_ylabel("allocation " + r"$x^*(\kappa)$")

        ax.set_xscale("log")
        ax.set_xlim(riskAversionMin, riskAversionMax)
        # ax.set_ylim(-0.05, 1.05)

        ax.legend(loc="upper center", ncol=3, frameon=False)

        plt.subplots_adjust(bottom=0.1, top=0.975, left=0.09, right=0.975)
        # plt.show()

        pathAssets = pl.Path(__file__).resolve().parent / "assets"
        pathAssets.mkdir(exist_ok=True)

        fig.savefig(pathAssets / "plotAllocationUtilityMaximization.svg")

    def plotAllocationIntegratedRiskManagement(self, alpha: float=0.95, beta: float=0.5, returnMin: float=0.0, returnMax: float=0.25) -> None:
        marker = ["^", "s", "o", "*", "X"]

        symbolsStock = list(self.portfolio.symbols)
        symbolsCall = list(self.portfolio.symbolsCall)
        symbolsPut = list(self.portfolio.symbolsPut)
        
        indicesCall = list(self.portfolio.indicesCall)
        indicesPut = list(self.portfolio.indicesPut)

        d0 = len(symbolsStock)
        d1 = len(symbolsCall)
        d2 = len(symbolsPut)

        mys = np.linspace(returnMin, returnMax, markerNumber)

        fig, ax = plt.subplots()
        for j in range(d0):

            xj = [Allocations.allocationIntegratedRiskManagement(portfolio=self.portfolio, alpha=alpha, beta=beta, minimumReturn=my)[0][j] for my in mys]
            
            ax.plot(
                mys, 
                xj, 
                color=cmap(1/3), 
                label=symbolsStock[j], 
                marker=marker[j], 
                markeredgecolor=cmap(1/3), 
                markerfacecolor="white"
            )
        for j0, j in enumerate(indicesCall):

            xj = [Allocations.allocationIntegratedRiskManagement(portfolio=self.portfolio, alpha=alpha, beta=beta, minimumReturn=my)[0][d0+j0] for my in mys]
            
            ax.plot(
                mys, 
                xj, 
                color=cmap(2/3), 
                label=symbolsCall[j0], 
                marker=marker[j], 
                markeredgecolor=cmap(2/3), 
                markerfacecolor="white", 
                zorder=j
            )
        for j0, j in enumerate(indicesPut):

            xj = [Allocations.allocationIntegratedRiskManagement(portfolio=self.portfolio, alpha=alpha, beta=beta, minimumReturn=my)[0][d0+d1+j0] for my in mys]
            
            ax.plot(
                mys, 
                xj, 
                color=cmap(1.0), 
                label=symbolsPut[j0], 
                marker=marker[j], 
                markeredgecolor=cmap(1.0), 
                markerfacecolor="white", 
                zorder=j
            )
        ax.hlines(y=0, xmin=returnMin, xmax=returnMax, linewidth=1, color="black", zorder=-1)

        ax.set_xlabel("minimum return " + r"$\mu$")
        ax.set_ylabel("allocation " + r"$x^*(\mu)$")

        ax.set_xlim(returnMin, returnMax)
        # ax.set_ylim(-0.05, 1.05)

        ax.legend(loc="upper center", ncol=3, frameon=False)

        plt.subplots_adjust(bottom=0.1, top=0.975, left=0.09, right=0.975)
        # plt.show()

        pathAssets = pl.Path(__file__).resolve().parent / "assets"
        pathAssets.mkdir(exist_ok=True)

        fig.savefig(pathAssets / "plotAllocationIntegratedRiskManagement.svg")

    # ------------------------------------------------------------------------------------------------------------------------------------------------------------
    #                                                                           Statistics
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------

    def meanRisk(self):
        pass

    def plotCorrelation(self, callPut: str="call"):
        # Scatterplot (2D or 3D)
        # x-Achse stock value, y-Achse option value

        d0 = len(self.portfolio.symbols)
        d1 = len(self.portfolio.symbolsCall)

        xiStocks = Returns.initialRelativeReturn(portfolio=self.portfolio)
        xiCall = Returns.optionReturnCall(portfolio=self.portfolio)
        xiPut = Returns.optionReturnPut(portfolio=self.portfolio)

        xi = np.hstack((xiStocks, xiCall, xiPut))

        n = len(xi)

        r = Stochastics.expectation(portfolio=self.portfolio)

        x = []
        y = []

        if callPut == "call":
            for i, symbolCall in enumerate(self.portfolio.symbolsCall):
                for j, symbol in enumerate(self.portfolio.symbols):
                    if symbolCall[:-5] == symbol:
                        for i in range(n):
                            x.append(xi[i,j])
                            y.append(xi[i,d0+j])
        elif callPut == "put":
            for i, symbolPut in enumerate(self.portfolio.symbolsPut):
                for j, symbol in enumerate(self.portfolio.symbols):
                    if symbolPut[:-4] == symbol:
                        for i in range(n):
                            x.append(xi[i,j])
                            y.append(xi[i,d0+d1+j])
        elif callPut == "callPut":
            for i, symbolCall in enumerate(self.portfolio.symbolsCall):
                for j, symbolPut in enumerate(self.portfolio.symbolsPut):
                    if symbolCall[:-5] == symbolPut[:-4]:
                        for i in range(n):
                            x.append(xi[i,d0+j])
                            y.append(xi[i,d0+d1+j])

        fig, ax = plt.subplots()

        ax.scatter(x=x, y=y)

        ax.set_xlabel("stock return")
        ax.set_ylabel("option return")

        plt.show()

    def plotCovarianceMatrix(self):
        sigma = Stochastics.covariance(portfolio=self.portfolio)

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
        sigma = Stochastics.covariance(portfolio=self.portfolio)
        d = len(sigma)

        correlation = np.empty((d,d))
        for i in range(d):
            for j in range(d):
                denominator = math.sqrt(sigma[i,i])*math.sqrt(sigma[j,j])
                correlation[i,j] = sigma[i,j]/denominator

        fig, ax = plt.subplots()

        im = ax.matshow(correlation, cmap="coolwarm")
        fig.colorbar(im, ax=ax)

        labels = self.portfolio.symbols + self.portfolio.symbolsCall + self.portfolio.symbolsPut

        ax.set_xticks(range(len(labels)))
        ax.set_yticks(range(len(labels)))

        ax.set_xticklabels(labels, rotation=90)
        ax.set_yticklabels(labels)

        plt.show()

    def plotMarginalDistribution(self):
        pass