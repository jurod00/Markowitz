from mathematics.allocations import Allocations
from portfolio.portfolio import Portfolio

import numpy as np
import pathlib as pl
import matplotlib.pyplot as plt

class PlotAllocation:

    def __init__(self, portfolio: Portfolio, allocations=None):
        # Memory
        self.portfolio = portfolio
        # Optional Dependency Injection
        self.allocations = allocations if allocations is not None else Allocations()
        # Design
        self._color = plt.get_cmap("Greens")
        self._marker = ["^", "s", "o", "*", "X"]
        self._markerNumber = 25

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

    def plotAllocationMarkowitz(self, returnMin: float=0.0, returnMax: float=0.25, format: str="svg") -> None:
        symbolsStock = list(self.portfolio.symbols)
        symbolsCall = list(self.portfolio.symbolsCall)
        symbolsPut = list(self.portfolio.symbolsPut)
        
        indicesCall = list(self.portfolio.indicesCall)
        indicesPut = list(self.portfolio.indicesPut)

        d0 = len(symbolsStock)
        d1 = len(symbolsCall)
        d2 = len(symbolsPut)

        mys = np.linspace(returnMin, returnMax, self._markerNumber)
        
        x0 = self.allocations.allocationMarkowitz(portfolio=self.portfolio, minimumReturn=returnMin)
        x1 = self.allocations.allocationMarkowitz(portfolio=self.portfolio, minimumReturn=returnMax)
        
        fig, ax = plt.subplots(figsize=(7, 4.5), layout="constrained")

        for j in range(d0):
            m = (x1[j] - x0[j])/(returnMax - returnMin)
            n = x0[j] - m*returnMin

            xj = m*mys + n
            
            ax.plot(
                mys, 
                xj, 
                label=symbolsStock[j], 
                color=self._color(1/3), 
                marker=self._marker[j], 
                markeredgecolor=self._color(1/3), 
                markerfacecolor="white"
            )

        for j0, j in enumerate(indicesCall):
            m = (x1[d0+j0] - x0[d0+j0])/(returnMax - returnMin)
            n = x0[d0+j0] - m*returnMin

            xj = m*mys + n
            
            ax.plot(
                mys, 
                xj, 
                label=symbolsCall[j0], 
                color=self._color(2/3), 
                marker=self._marker[j], 
                markeredgecolor=self._color(2/3), 
                markerfacecolor="white"
            )

        for j0, j in enumerate(indicesPut):
            m = (x1[d0+d1+j0] - x0[d0+d1+j0])/(returnMax - returnMin)
            n = x0[d0+d1+j0] - m*returnMin

            xj = m*mys + n
            
            ax.plot(
                mys, 
                xj, 
                label=symbolsPut[j0], 
                color=self._color(1.0), 
                marker=self._marker[j], 
                markeredgecolor=self._color(1.0), 
                markerfacecolor="white"
            )

        ax.hlines(y=0, xmin=returnMin, xmax=returnMax, linewidth=1, color="black", zorder=-1)

        # x-axis
        ax.set_xlim(returnMin, returnMax)
        ax.set_xlabel("minimum return " + r"$\mu$")

        # y-axis
        ax.set_yticks([])
        ax.set_ylabel("allocation " + r"$x^*(\mu)$")
        # ax.set_ylim(-0.05, 1.05)

        # legend
        ax.legend(loc="lower center", ncol=3, frameon=False)

        pathAssets = pl.Path(__file__).resolve().parent / "assets"
        pathAssets.mkdir(exist_ok=True)

        fig.savefig(pathAssets / f"plotAllocationMarkowitz.{format}", bbox_inches="tight", pad_inches=0.05)

    def plotAllocationUtilityMaximization(self, riskAversionMin: float=float(1e-1), riskAversionMax: float=float(1e+6), format: str="svg") -> None:
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

        kappas = np.logspace(start=start, stop=stop, num=self._markerNumber, endpoint=True, base=base)

        fig, ax = plt.subplots(figsize=(7, 4.5), layout="constrained")
        for j in range(d0):

            xj = [self.allocations.allocationUtilityMaximization(portfolio=self.portfolio, riskAversion=kappa)[j] for kappa in kappas]

            ax.plot(
                kappas, 
                xj, 
                label=symbolsStock[j], 
                color=self._color(1/3), 
                marker=self._marker[j], 
                markeredgecolor=self._color(1/3), 
                markerfacecolor="white"
            )
        for j0, j in enumerate(indicesCall):

            xj = [self.allocations.allocationUtilityMaximization(portfolio=self.portfolio, riskAversion=kappa)[d0+j0] for kappa in kappas]

            ax.plot(
                kappas, 
                xj, 
                label=symbolsCall[j0], 
                color=self._color(2/3), 
                marker=self._marker[j], 
                markeredgecolor=self._color(2/3), 
                markerfacecolor="white"
            )
        for j0, j in enumerate(indicesPut):

            xj = [self.allocations.allocationUtilityMaximization(portfolio=self.portfolio, riskAversion=kappa)[d0+d1+j0] for kappa in kappas]

            ax.plot(
                kappas, 
                xj, 
                label=symbolsPut[j0], 
                color=self._color(1.0), 
                marker=self._marker[j], 
                markeredgecolor=self._color(1.0), 
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

        pathAssets = pl.Path(__file__).resolve().parent / "assets"
        pathAssets.mkdir(exist_ok=True)

        fig.savefig(pathAssets / f"plotAllocationUtilityMaximization.{format}")

    def plotAllocationIntegratedRiskManagement(self, alpha: float=0.95, beta: float=0.5, returnMin: float=0.0, returnMax: float=0.25, format: str="svg") -> None:
        symbolsStock = list(self.portfolio.symbols)
        symbolsCall = list(self.portfolio.symbolsCall)
        symbolsPut = list(self.portfolio.symbolsPut)
        
        indicesCall = list(self.portfolio.indicesCall)
        indicesPut = list(self.portfolio.indicesPut)

        d0 = len(symbolsStock)
        d1 = len(symbolsCall)
        d2 = len(symbolsPut)

        mys = np.linspace(returnMin, returnMax, self._markerNumber)

        fig, ax = plt.subplots(figsize=(7, 4.5), layout="constrained")
        for j in range(d0):

            xj = [self.allocations.allocationIntegratedRiskManagement(portfolio=self.portfolio, alpha=alpha, beta=beta, minimumReturn=my)[0][j] for my in mys]
            
            ax.plot(
                mys, 
                xj, 
                label=symbolsStock[j], 
                color=self._color(1/3), 
                marker=self._marker[j], 
                markeredgecolor=self._color(1/3), 
                markerfacecolor="white"
            )
        for j0, j in enumerate(indicesCall):

            xj = [self.allocations.allocationIntegratedRiskManagement(portfolio=self.portfolio, alpha=alpha, beta=beta, minimumReturn=my)[0][d0+j0] for my in mys]
            
            ax.plot(
                mys, 
                xj, 
                label=symbolsCall[j0], 
                color=self._color(2/3), 
                marker=self._marker[j], 
                markeredgecolor=self._color(2/3), 
                markerfacecolor="white", 
                zorder=j
            )
        for j0, j in enumerate(indicesPut):

            xj = [self.allocations.allocationIntegratedRiskManagement(portfolio=self.portfolio, alpha=alpha, beta=beta, minimumReturn=my)[0][d0+d1+j0] for my in mys]
            
            ax.plot(
                mys, 
                xj, 
                label=symbolsPut[j0], 
                color=self._color(1.0), 
                marker=self._marker[j], 
                markeredgecolor=self._color(1.0), 
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

        pathAssets = pl.Path(__file__).resolve().parent / "assets"
        pathAssets.mkdir(exist_ok=True)

        fig.savefig(pathAssets / f"plotAllocationIntegratedRiskManagement.{format}")

    def plotStackedBar(self, allocation: np.ndarray=None, minimumReturn: float=None, alpha: float=None, beta: float=None, riskAversion: float=None, format: str="svg") -> None:
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
                    label=symbols[i], 
                    color=self._color((i+1)/d)
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

            pathAssets = pl.Path(__file__).resolve().parent / "assets"
            pathAssets.mkdir(exist_ok=True)

            fig.savefig(pathAssets / f"plotStackedBar.{format}")

        if minimumReturn is not None and (alpha is None or beta is None): # Markowitz
            symbols = list(self.portfolio.symbols)
            x = self.allocations.allocationMarkowitz(portfolio=self.portfolio, minimumReturn=minimumReturn)
            d = len(x)

            fig, ax = plt.subplots(figsize=(10, 2))
            for i in range(d):
                left = (0 if i == 0 else sum(x[:i]))
                ax.barh(
                    y=[0], 
                    width=x[i], 
                    left=left, 
                    label=symbols[i], 
                    color=self._color((i+1)/d)
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

            pathAssets = pl.Path(__file__).resolve().parent / "assets"
            pathAssets.mkdir(exist_ok=True)

            fig.savefig(pathAssets / f"plotStackedBar.{format}")

        if minimumReturn is not None and alpha is not None and beta is not None: # IntegratedRiskManagement
            pass
        if riskAversion is not None: # UtilityMaximization
            pass