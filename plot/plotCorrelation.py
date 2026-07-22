from portfolio.portfolio import Portfolio
from mathematics.returns import Returns

import pathlib as pl
import matplotlib.pyplot as plt

class PlotCorrelation:

    def __init__(self, portfolio: Portfolio, returns: Returns=None):
        # Memory
        self.portfolio = portfolio
        # Optional Dependency Injection
        self.returns = returns if returns is not None else Returns()

    def plotCorrelationStockCall(self, format: str="svg"):
        r = self.returns.expectedReturn(portfolio=self.portfolio)

        x = []
        y = []

        i0 = len(self.portfolio.symbols)

        for j0, j in enumerate(self.portfolio.indicesCall):
            x.append(r[j])
            y.append(r[i0+j0])

        fig, ax = plt.subplots()
        ax.scatter(x=x, y=y)

        pathAssets = pl.Path(__file__).resolve().parent / "assets"
        pathAssets.mkdir(exist_ok=True)

        fig.savefig(pathAssets / f"plotCorrelationStockCall.{format}")

    def plotCorrelationStockPut(self, format: str="svg"):
        r = self.returns.expectedReturn(portfolio=self.portfolio)

        x = []
        y = []

        i0 = len(self.portfolio.symbols) + len(self.portfolio.symbolsCall)

        for j0, j in enumerate(self.portfolio.indicesPut):
            x.append(r[j])
            y.append(r[i0+j0])

        fig, ax = plt.subplots()
        ax.scatter(x=x, y=y)

        pathAssets = pl.Path(__file__).resolve().parent / "assets"
        pathAssets.mkdir(exist_ok=True)

        fig.savefig(pathAssets / f"plotCorrelationStockPut.{format}")

    def plotCorrelationCallPut(self, format: str="svg"):
        pass

    def plotCorrelationStockCallPut(self, format: str="svg"):
        # 3D Plot
        pass