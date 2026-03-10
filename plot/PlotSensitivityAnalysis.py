import numpy as np
import matplotlib.pyplot as plt

from analysis import SensitivityAnalysis
from portfolio import FinancialMathematics as FiMa

from portfolio import PortfolioShares

class PlotSensitivityAnalysis:
    def __init__(self):
        self.analysis = SensitivityAnalysis()

    def plotMeanVariance(self, portfolio, allocations) -> None:
        # Mean-Variance-Graph
        a, b, c, _ = FiMa.abcd(
            time=portfolio.getTime(), 
            stocks=portfolio.getStocks()
        )

        def mean(stdDev):
            return b/c + np.sqrt((a - b**2/c)*(stdDev**2 - 1/c))
        
        sigma = np.linspace(start=0, stop=0.5, num=int(1e+5))
        my = np.empty(len(sigma))

        for i in range(len(sigma)):
            if sigma[i]**2 > 1/c:
                my[i] = mean(sigma[i])
            else:
                my[i] = np.nan
        
        # Portfolios with noise
        myScatter, sigmaScatter = self.analysis.meanVarianceScatterData(portfolio=portfolio, allocations=allocations)

        # Plot
        fig, ax1 = plt.subplots(figsize=(15, 10))
        # ax2 = ax1.twinx()

        ax1.plot(
            sigma, 
            my, 
            linewidth=1, 
            color="black", 
            label=r"$\mu(\sigma)$"
        )
        ax1.scatter(
            x=sigmaScatter, 
            y=myScatter, 
            s=1, 
            c="black", 
            marker=".", 
            label=r"$(\sigma(x^*),\mu(x^*))$"
        )

        ax1.set_xlabel("risk " + r"$\sigma$")
        ax1.set_ylabel("return " + r"$\mu$")

        ax1.set_xlim(0, 0.5)
        ax1.set_ylim(0, 0.5)

        ax1.set_xticks([i/10 for i in range(6)])
        ax1.set_yticks([i/10 for i in range(6)])

        ax1.grid(linewidth=0.25)

        ax1.legend(loc="best")

        plt.xticks(rotation=45)
        plt.show()

    def plotMeanRiskmeasure(self, portfolio, epsilon) -> None:
        # Portfolios with noise
        my = [i/10000 for i in range(10000)]
        riskMeasure = []

        for m in my:
            objTemp = FiMa.objectiveLinearProgramming(
                time=portfolio.getTime(),
                stocks=portfolio.getStocks(),
                minimumReturn=m
            )
            riskMeasure.append(objTemp)

        allocations = self.analysis.allocationsNoisy(portfolio, epsilon, "linearProgramming")
        myScatter, objectiveScatter = self.analysis.meanObjectiveScatterData(portfolio, allocations)

        # Plot
        fig, ax1 = plt.subplots(figsize=(15, 10))
        # ax2 = ax1.twinx()

        ax1.plot(
            riskMeasure, 
            my, 
            linewidth=1, 
            color="black", 
            label=r"$\mu(\sigma)$"
        )
        
        ax1.scatter(
            x=objectiveScatter, 
            y=myScatter, 
            s=1, 
            c="black", 
            marker=".", 
            label=r"$\left(\rho(x^*),\mu(x^*)\right)$"
        )

        ax1.set_xlabel("risk " + r"$\rho = Ex^T\xi + \mathcal{R}_{\alpha,\gamma}(-x^T\xi)$")
        ax1.set_ylabel("return " + r"$\mu$")

        ax1.set_xlim(0, 0.5)
        ax1.set_ylim(0, 0.5)

        ax1.set_xticks([i/10 for i in range(6)])
        ax1.set_yticks([i/10 for i in range(6)])

        ax1.grid(linewidth=0.25)

        ax1.legend(loc="best")

        plt.xticks(rotation=45)
        plt.show()