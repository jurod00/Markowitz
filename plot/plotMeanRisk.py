from mathematics.allocations import Allocations
from mathematics.riskMeasures import RiskMeasures
from portfolio.portfolio import Portfolio

import math
import numpy as np
import pathlib as pl
import matplotlib.pyplot as plt

class PlotMeanRisk:

    def __init__(self, portfolio: Portfolio, allocations=None, riskMeasures=None):
        # Memory
        self.portfolio = portfolio
        # Optional Dependency Injection
        self.allocations = allocations if allocations is not None else Allocations()
        self.riskMeasures = riskMeasures if riskMeasures is not None else RiskMeasures()
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

    def plotMeanVarianceMarkowitz(self, returnMin: float=0.0, returnMax: float=0.25, format: str="svg"):
        mys = np.linspace(returnMin, returnMax, self._markerNumber)

        mean = []
        sd = []

        for my in mys:
            allocation = self.allocations.allocationMarkowitz(portfolio=self.portfolio, minimumReturn=my)

            mean.append(self.riskMeasures.mean(portfolio=self.portfolio, allocation=allocation))
            sd.append(math.sqrt(self.riskMeasures.variance(portfolio=self.portfolio, allocation=allocation)))

        fig, ax = plt.subplots(figsize=(7, 4.5), layout="constrained")

        ax.plot(sd, mean, color="forestgreen")

        ax.set_xlabel(r"Risk $\sigma = \sqrt{\operatorname{var}x^\top\xi}$")
        ax.set_ylabel(r"Return $\mu = \operatorname{E}x^\top\xi$")

        pathAssets = pl.Path(__file__).resolve().parent / "assets"
        pathAssets.mkdir(exist_ok=True)

        fig.savefig(pathAssets / f"plotMeanVarianceMarkowitz.{format}", bbox_inches="tight", pad_inches=0.05)

    def plotMeanVarianceUtilityMaximization(self, riskAversionMin: float=float(1e-1), riskAversionMax: float=float(1e+6), format: str="svg"):
        base = 10
        start = np.log(riskAversionMin)/np.log(base)
        stop = np.log(riskAversionMax)/np.log(base)

        kappas = np.logspace(start=start, stop=stop, num=self._markerNumber, endpoint=True, base=base)

        mean = []
        sd = []

        for kappa in kappas:
            allocation = self.allocations.allocationUtilityMaximization(portfolio=self.portfolio, riskAversion=kappa)

            mean.append(self.riskMeasures.mean(portfolio=self.portfolio, allocation=allocation))
            sd.append(math.sqrt(self.riskMeasures.variance(portfolio=self.portfolio, allocation=allocation)))

        fig, ax = plt.subplots(figsize=(7, 4.5), layout="constrained")

        ax.scatter(sd, mean, color="forestgreen")

        ax.set_xlabel(r"Risk $\sigma = \sqrt{\operatorname{var}x^\top\xi}$")
        ax.set_ylabel(r"Return $\mu = \operatorname{E}x^\top\xi$")

        pathAssets = pl.Path(__file__).resolve().parent / "assets"
        pathAssets.mkdir(exist_ok=True)

        fig.savefig(pathAssets / f"plotMeanVarianceUtilityMaximization.{format}", bbox_inches="tight", pad_inches=0.05)

    def plotMeanAVaR(self, returnMin: float=0.0, returnMax: float=0.25, format: str="svg"):
        mys = np.linspace(returnMin, returnMax, 100)

        mean = []
        avar = []

        for my in mys:
            allocation, _ = self.allocations.allocationIntegratedRiskManagement(portfolio=self.portfolio, alpha=0.95, beta=1.0, minimumReturn=my)

            mean.append(self.riskMeasures.mean(portfolio=self.portfolio, allocation=allocation))
            avar.append(self.riskMeasures.averageValueAtRisk(portfolio=self.portfolio, alpha=0.95, allocation=allocation))

        fig, ax = plt.subplots(figsize=(7, 4.5), layout="constrained")

        ax.plot(avar, mean, color="forestgreen")

        ax.set_xlabel(r"Risk $\sigma = \operatorname{AVaR}_{0.95}(-x^\top\xi)$")
        ax.set_ylabel(r"Return $\mu = \operatorname{E}x^\top\xi$")

        pathAssets = pl.Path(__file__).resolve().parent / "assets"
        pathAssets.mkdir(exist_ok=True)

        fig.savefig(pathAssets / f"plotMeanAVaR.{format}", bbox_inches="tight", pad_inches=0.05)