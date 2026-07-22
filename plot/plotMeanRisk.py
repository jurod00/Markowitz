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

    def plotMeanVarianceMarkowitz(self, returnMin: float=0.0, returnMax: float=0.25, format: str="svg"):
        mys = np.linspace(returnMin, returnMax, self._markerNumber)

        mean = []
        sd = []

        for my in mys:
            allocation = self.allocations.allocationMarkowitz(portfolio=self.portfolio, minimumReturn=my)

            mean.append(self.riskMeasures.mean(portfolio=self.portfolio, allocation=allocation))
            sd.append(math.sqrt(self.riskMeasures.variance(portfolio=self.portfolio, allocation=allocation)))

        fig, ax = plt.subplots()

        ax.scatter(x=sd, y=mean)

        pathAssets = pl.Path(__file__).resolve().parent / "assets"
        pathAssets.mkdir(exist_ok=True)

        fig.savefig(pathAssets / f"plotMeanVarianceMarkowitz.{format}")

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

        fig, ax = plt.subplots()

        ax.scatter(x=sd, y=mean)

        pathAssets = pl.Path(__file__).resolve().parent / "assets"
        pathAssets.mkdir(exist_ok=True)

        fig.savefig(pathAssets / f"plotMeanVarianceUtilityMaximization.{format}")

    def plotMeanAVaR(self, returnMin: float=0.0, returnMax: float=0.25, format: str="svg"):
        alpha = 0.95
        beta = 1.0

        # mys = np.linspace(returnMin, returnMax, self._markerNumber)
        mys = np.linspace(returnMin, returnMax, 100)

        mean = []
        avar = []

        for my in mys:
            allocation, _ = self.allocations.allocationIntegratedRiskManagement(portfolio=self.portfolio, alpha=alpha, beta=beta, minimumReturn=my)

            mean.append(self.riskMeasures.mean(portfolio=self.portfolio, allocation=allocation))
            avar.append(self.riskMeasures.averageValueAtRisk(portfolio=self.portfolio, alpha=alpha, allocation=allocation))

        fig, ax = plt.subplots()

        ax.scatter(x=avar, y=mean)

        pathAssets = pl.Path(__file__).resolve().parent / "assets"
        pathAssets.mkdir(exist_ok=True)

        fig.savefig(pathAssets / f"plotMeanAVaR.{format}")