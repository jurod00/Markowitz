from mathematics.sensitivityLocal import SensitivityLocal
from portfolio.portfolio import Portfolio

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import pathlib as pl

class PlotSensitivityLocal:
    def __init__(self, portfolio: Portfolio, sensitivityLocal=None):
        # Memory
        self.portfolio = portfolio
        # Optional Dependency Injection
        self.sensitivityLocal = sensitivityLocal if sensitivityLocal is not None else SensitivityLocal()
        # Default parameters
        self.alpha = 0.95
        self.beta = 0.5
        self.my = 0.2
        # Design
        self._color = plt.get_cmap("Greens")
        self._marker = ["^", "s", "o", "*", "X"]
        self._markerNumber = 1000
        
        plt.rcParams.update(
            {
                "font.size": 16,
                "axes.titlesize": 14,
                "axes.labelsize": 14,
                "xtick.labelsize": 16,
                "ytick.labelsize": 16,
                "legend.fontsize": 14,
            }
        )

    def plotSensitivityMinimumReturnMARKOWITZ(self, returnMin: float=float(1e-3), returnMax: float=0.25, shortSellingAllowed: bool=True, method: str="default", format: str="svg"):
        symbolsStock = list(self.portfolio.symbols)
        symbolsCall = list(self.portfolio.symbolsCall)
        symbolsPut = list(self.portfolio.symbolsPut)

        symbols = symbolsStock + symbolsCall + symbolsPut

        d0 = len(symbolsStock)
        d1 = len(symbolsCall)
        d2 = len(symbolsPut)

        d = len(symbolsStock) + len(symbolsCall) + len(symbolsPut)

        indicesCall = list(self.portfolio.indicesCall)
        indicesPut = list(self.portfolio.indicesPut)

        mys = np.linspace(returnMin, returnMax, 20)

        fig, ax = plt.subplots(figsize=(7, 4.5), layout="constrained")

        for j in range(d0):
            sj = [self.sensitivityLocal.minimumReturnMARKOWITZ(portfolio=self.portfolio, minimumReturn=my, shortSellingAllowed=shortSellingAllowed, method=method)[j] for my in mys]

            ax.plot(
                mys, 
                sj, 
                label=symbols[j], 
                color=self._color(1/3), 
                marker=self._marker[j], 
                markeredgecolor=self._color(1/3), 
                markerfacecolor="white"
            )

        for j0, j in enumerate(indicesCall):
            sj = [self.sensitivityLocal.minimumReturnMARKOWITZ(portfolio=self.portfolio, minimumReturn=my, shortSellingAllowed=shortSellingAllowed, method=method)[d0+j0] for my in mys]

            ax.plot(
                mys, 
                sj, 
                label=symbolsCall[j0], 
                color=self._color(2/3), 
                marker=self._marker[j], 
                markeredgecolor=self._color(2/3), 
                markerfacecolor="white"
            )

        for j0, j in enumerate(indicesPut):
            sj = [self.sensitivityLocal.minimumReturnMARKOWITZ(portfolio=self.portfolio, minimumReturn=my, shortSellingAllowed=shortSellingAllowed, method=method)[d0+d1+j0] for my in mys]

            ax.plot(
                mys, 
                sj, 
                label=symbolsPut[j0], 
                color=self._color(1.0), 
                marker=self._marker[j], 
                markeredgecolor=self._color(1.0), 
                markerfacecolor="white"
            )

        # x-axis
        ax.set_xlim(returnMin, returnMax)
        ax.set_xlabel("Minimum return " + r"$\mu$")
    
        # y-axis
        ax.set_ylabel("Sensitivity " + r"$\mathcal{S}(\mu)$")
        # ax.set_ylim(-0.05, 1.05)
        # ax.yaxis.set_major_formatter(mtick.FormatStrFormatter("%.1f"))
        # ax.yaxis.set_major_locator(mtick.MultipleLocator(0.1))
    
        # legend
        ax.legend(loc="center left", bbox_to_anchor=(0.05, 0.3), ncol=3, frameon=False)
    
        pathAssets = pl.Path(__file__).resolve().parent / "assets"
        pathAssets.mkdir(exist_ok=True)
    
        fig.savefig(pathAssets / f"plotSensitivityMinimumReturnMARKOWITZ.{format}", bbox_inches="tight", pad_inches=0.05)

    def plotSensitivityStockMARKOWITZ(self, epsilonMin: float=0, epsilonMax: float=0.02, shortSellingAllowed: bool=True, method: str="default", format: str="svg"):
        symbolsStock = list(self.portfolio.symbols)
        symbolsCall = list(self.portfolio.symbolsCall)
        symbolsPut = list(self.portfolio.symbolsPut)

        symbols = symbolsStock + symbolsCall + symbolsPut

        d0 = len(symbolsStock)
        d1 = len(symbolsCall)
        d2 = len(symbolsPut)

        d = len(symbolsStock) + len(symbolsCall) + len(symbolsPut)

        indicesCall = list(self.portfolio.indicesCall)
        indicesPut = list(self.portfolio.indicesPut)

        epsilons = np.linspace(epsilonMin, epsilonMax, 2)
        epsilons = [0]

        fig, ax = plt.subplots(figsize=(7, 4.5), layout="constrained")

        for j in range(d0):
            sj = [self.sensitivityLocal.stockMARKOWITZ(h=epsilon, portfolio=self.portfolio, minimumReturn=self.my, shortSellingAllowed=shortSellingAllowed, method=method)[j] for epsilon in epsilons]
            print(j)
            ax.plot(
                epsilons, 
                sj, 
                label=symbols[j], 
                color=self._color(1/3), 
                marker=self._marker[j], 
                markeredgecolor=self._color(1/3), 
                markerfacecolor="white"
            )

        for j0, j in enumerate(indicesCall):
            sj = [self.sensitivityLocal.stockMARKOWITZ(h=epsilon, portfolio=self.portfolio, minimumReturn=self.my, shortSellingAllowed=shortSellingAllowed, method=method)[d0+j0] for epsilon in epsilons]
            print(j)
            ax.plot(
                epsilons, 
                sj, 
                label=symbolsCall[j0], 
                color=self._color(2/3), 
                marker=self._marker[j], 
                markeredgecolor=self._color(2/3), 
                markerfacecolor="white"
            )

        for j0, j in enumerate(indicesPut):
            sj = [self.sensitivityLocal.stockMARKOWITZ(h=epsilon, portfolio=self.portfolio, minimumReturn=self.my, shortSellingAllowed=shortSellingAllowed, method=method)[d0+d1+j0] for epsilon in epsilons]
            print(j)
            ax.plot(
                epsilons, 
                sj, 
                label=symbolsPut[j0], 
                color=self._color(1.0), 
                marker=self._marker[j], 
                markeredgecolor=self._color(1.0), 
                markerfacecolor="white"
            )

        # x-axis
        ax.set_xlim(epsilonMin, epsilonMax)
        ax.set_xlabel("Minimum return " + r"$\mu$")
    
        # y-axis
        ax.set_ylabel("Sensitivity " + r"$\mathcal{S}(\mu)$")
        # ax.set_ylim(-0.05, 1.05)
        # ax.yaxis.set_major_formatter(mtick.FormatStrFormatter("%.1f"))
        # ax.yaxis.set_major_locator(mtick.MultipleLocator(0.1))
    
        # legend
        ax.legend(loc="center left", bbox_to_anchor=(0.05, 0.3), ncol=3, frameon=False)
    
        pathAssets = pl.Path(__file__).resolve().parent / "assets"
        pathAssets.mkdir(exist_ok=True)
    
        fig.savefig(pathAssets / f"plotSensitivityStockMARKOWITZ.{format}", bbox_inches="tight", pad_inches=0.05)

    def plotSensitivityMinimumReturnIRM(self, returnMin: float=float(1e-3), returnMax: float=0.25, shortSellingAllowed: bool=False, method: str="default", format: str="svg"):
        symbolsStock = list(self.portfolio.symbols)
        symbolsCall = list(self.portfolio.symbolsCall)
        symbolsPut = list(self.portfolio.symbolsPut)

        symbols = symbolsStock + symbolsCall + symbolsPut

        d0 = len(symbolsStock)
        d1 = len(symbolsCall)
        d2 = len(symbolsPut)

        d = len(symbolsStock) + len(symbolsCall) + len(symbolsPut)

        indicesCall = list(self.portfolio.indicesCall)
        indicesPut = list(self.portfolio.indicesPut)

        mys = np.linspace(returnMin, returnMax, 50)

        fig, ax = plt.subplots(figsize=(7, 4.5), layout="constrained")

        for j in range(d0):
            sj = [self.sensitivityLocal.minimumReturnIRM(portfolio=self.portfolio, alpha=self.alpha, beta=self.beta, minimumReturn=my, shortSellingAllowed=shortSellingAllowed, method=method)[j] for my in mys]

            ax.plot(
                mys, 
                sj, 
                label=symbols[j], 
                color=self._color(1/3), 
                marker=self._marker[j], 
                markeredgecolor=self._color(1/3), 
                markerfacecolor="white"
            )

        for j0, j in enumerate(indicesCall):
            sj = [self.sensitivityLocal.minimumReturnIRM(portfolio=self.portfolio, alpha=self.alpha, beta=self.beta, minimumReturn=my, shortSellingAllowed=shortSellingAllowed, method=method)[d0+j0] for my in mys]

            ax.plot(
                mys, 
                sj, 
                label=symbolsCall[j0], 
                color=self._color(2/3), 
                marker=self._marker[j], 
                markeredgecolor=self._color(2/3), 
                markerfacecolor="white"
            )

        for j0, j in enumerate(indicesPut):
            sj = [self.sensitivityLocal.minimumReturnIRM(portfolio=self.portfolio, alpha=self.alpha, beta=self.beta, minimumReturn=my, shortSellingAllowed=shortSellingAllowed, method=method)[d0+d1+j0] for my in mys]

            ax.plot(
                mys, 
                sj, 
                label=symbolsPut[j0], 
                color=self._color(1.0), 
                marker=self._marker[j], 
                markeredgecolor=self._color(1.0), 
                markerfacecolor="white"
            )

        # x-axis
        ax.set_xlim(returnMin, returnMax)
        ax.set_xlabel("Minimum return " + r"$\mu$")
        
        # y-axis
        ax.set_ylabel("Sensitivity " + r"$\mathcal{S}(\mu)$")
        # ax.set_ylim(-0.05, 1.05)
        # ax.yaxis.set_major_formatter(mtick.FormatStrFormatter("%.1f"))
        # ax.yaxis.set_major_locator(mtick.MultipleLocator(0.1))
        
        # legend
        ax.legend(loc="center left", bbox_to_anchor=(0.05, 0.3), ncol=3, frameon=False)
        
        pathAssets = pl.Path(__file__).resolve().parent / "assets"
        pathAssets.mkdir(exist_ok=True)
        
        fig.savefig(pathAssets / f"plotSensitivityMinimumReturnIRM.{format}", bbox_inches="tight", pad_inches=0.05)

    def plotSensitivityAlphaIRM(self, alphaMin: float=0.01001, alphaMax: float=0.98999, shortSellingAllowed: bool=False, method: str="default", format: str="svg"):
        symbolsStock = list(self.portfolio.symbols)
        symbolsCall = list(self.portfolio.symbolsCall)
        symbolsPut = list(self.portfolio.symbolsPut)

        d0 = len(symbolsStock)
        d1 = len(symbolsCall)
        d2 = len(symbolsPut)

        indicesCall = list(self.portfolio.indicesCall)
        indicesPut = list(self.portfolio.indicesPut)

        alphas = np.linspace(alphaMin, alphaMax, 50)

        fig, ax = plt.subplots(figsize=(7, 4.5), layout="constrained")

        for j in range(d0):
            sj = [self.sensitivityLocal.alphaIRM(portfolio=self.portfolio, alpha=alpha, beta=self.beta, minimumReturn=self.my, shortSellingAllowed=shortSellingAllowed, method=method)[j] for alpha in alphas]

            ax.plot(
                alphas, 
                sj, 
                label=symbolsStock[j], 
                color=self._color(1/3), 
                marker=self._marker[j], 
                markeredgecolor=self._color(1/3), 
                markerfacecolor="white"
            )

        for j0, j in enumerate(indicesCall):
            sj = [self.sensitivityLocal.minimumReturnIRM(portfolio=self.portfolio, alpha=alpha, beta=self.beta, minimumReturn=self.my, shortSellingAllowed=shortSellingAllowed, method=method)[d0+j0] for alpha in alphas]

            ax.plot(
                alphas, 
                sj, 
                label=symbolsCall[j0], 
                color=self._color(2/3), 
                marker=self._marker[j], 
                markeredgecolor=self._color(2/3), 
                markerfacecolor="white"
            )

        for j0, j in enumerate(indicesPut):
            sj = [self.sensitivityLocal.minimumReturnIRM(portfolio=self.portfolio, alpha=alpha, beta=self.beta, minimumReturn=self.my, shortSellingAllowed=shortSellingAllowed, method=method)[d0+d1+j0] for alpha in alphas]

            ax.plot(
                alphas, 
                sj, 
                label=symbolsPut[j0], 
                color=self._color(1.0), 
                marker=self._marker[j], 
                markeredgecolor=self._color(1.0), 
                markerfacecolor="white"
            )

        # x-axis
        ax.set_xlim(alphaMin, alphaMax)
        ax.set_xlabel("parameter " + r"$\alpha$")
        
        # y-axis
        ax.set_ylabel("sensitivity " + r"$\mathcal{S}(\alpha)$")
        # ax.set_ylim(-0.05, 1.05)
        # ax.yaxis.set_major_formatter(mtick.FormatStrFormatter("%.1f"))
        # ax.yaxis.set_major_locator(mtick.MultipleLocator(0.1))
        
        # legend
        ax.legend(loc="upper center", ncol=3, frameon=False)
        
        pathAssets = pl.Path(__file__).resolve().parent / "assets"
        pathAssets.mkdir(exist_ok=True)
        
        fig.savefig(pathAssets / f"plotSensitivityAlphaIRM.{format}", bbox_inches="tight", pad_inches=0.05)

    def plotSensitivityBetaIRM(self, betaMin: float=0.01, betaMax: float=0.99, shortSellingAllowed: bool=False, method: str="default", format: str="svg"):
        symbolsStock = list(self.portfolio.symbols)
        symbolsCall = list(self.portfolio.symbolsCall)
        symbolsPut = list(self.portfolio.symbolsPut)

        d0 = len(symbolsStock)
        d1 = len(symbolsCall)
        d2 = len(symbolsPut)
        
        indicesCall = list(self.portfolio.indicesCall)
        indicesPut = list(self.portfolio.indicesPut)

        d = len(symbolsStock) + len(symbolsCall) + len(symbolsPut)

        betas = np.linspace(betaMin, betaMax, 50)

        fig, ax = plt.subplots(figsize=(7, 4.5), layout="constrained")

        for j in range(d0):
            sj = [self.sensitivityLocal.betaIRM(portfolio=self.portfolio, alpha=self.alpha, beta=beta, minimumReturn=self.my, shortSellingAllowed=shortSellingAllowed, method=method)[j] for beta in betas]

            ax.plot(
                betas, 
                sj, 
                label=symbolsStock[j], 
                color=self._color(1/3), 
                marker=self._marker[j], 
                markeredgecolor=self._color(1/3), 
                markerfacecolor="white"
            )

        for j0, j in enumerate(indicesCall):
            sj = [self.sensitivityLocal.minimumReturnIRM(portfolio=self.portfolio, alpha=self.alpha, beta=beta, minimumReturn=self.my, shortSellingAllowed=shortSellingAllowed, method=method)[d0+j0] for beta in betas]

            ax.plot(
                betas, 
                sj, 
                label=symbolsCall[j0], 
                color=self._color(2/3), 
                marker=self._marker[j], 
                markeredgecolor=self._color(2/3), 
                markerfacecolor="white"
            )

        for j0, j in enumerate(indicesPut):
            sj = [self.sensitivityLocal.minimumReturnIRM(portfolio=self.portfolio, alpha=self.alpha, beta=beta, minimumReturn=self.my, shortSellingAllowed=shortSellingAllowed, method=method)[d0+d1+j0] for beta in betas]

            ax.plot(
                betas, 
                sj, 
                label=symbolsPut[j0], 
                color=self._color(1.0), 
                marker=self._marker[j], 
                markeredgecolor=self._color(1.0), 
                markerfacecolor="white"
            )

        # x-axis
        ax.set_xlim(betaMin, betaMax)
        ax.set_xlabel("parameter " + r"$\beta$")
        
        # y-axis
        ax.set_ylabel("sensitivity " + r"$\mathcal{S}(\beta)$")
        # ax.set_ylim(-0.05, 1.05)
        # ax.yaxis.set_major_formatter(mtick.FormatStrFormatter("%.1f"))
        # ax.yaxis.set_major_locator(mtick.MultipleLocator(0.1))
        
        # legend
        ax.legend(loc="upper center", ncol=3, frameon=False)
        
        pathAssets = pl.Path(__file__).resolve().parent / "assets"
        pathAssets.mkdir(exist_ok=True)
        
        fig.savefig(pathAssets / f"plotSensitivityBetaIRM.{format}", bbox_inches="tight", pad_inches=0.05)
