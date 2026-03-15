import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

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
            color="midnightblue", 
            label=r"$(\sigma(x^*),\mu(x^*))$"
        )
        ax1.scatter(
            x=sigmaScatter, 
            y=myScatter, 
            s=1, 
            c="dodgerblue", 
            marker=".", 
            label=r"$(\sigma(x^\epsilon),\mu(x^\epsilon))$"
        )

        ax1.set_xlabel("risk " + r"$\sigma = \mathrm{var}\,x^\top\xi$")
        ax1.set_ylabel("return " + r"$\mu = \mathrm{E}\,x^\top\xi$")

        ax1.set_xlim(0, 0.5)
        ax1.set_ylim(0, 0.5)

        ax1.set_xticks([i/10 for i in range(6)])
        ax1.set_yticks([i/10 for i in range(6)])

        ax1.grid(linewidth=0.25)

        ax1.legend(loc="best")

        plt.xticks(rotation=45)
        plt.show()

        fig.savefig("C:/Users/j.rode/Desktop/Markowitz/plot/assets/plotMeanVarianceUtilityMaximization20.svg")

    def plotMeanRiskmeasure(self, portfolio, epsilon) -> None:
        # Portfolios with noise
        # my = [i/10000 for i in range(10000)]
        my = np.linspace(0.07, 0.5, num=int(1e+4))
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
            color="midnightblue", 
            label=r"$(\rho(x^*),\mu(x^*))$"
        )
        
        ax1.scatter(
            x=objectiveScatter, 
            y=myScatter, 
            s=1, 
            c="dodgerblue", 
            marker=".", 
            label=r"$(\rho(x^\epsilon),\mu(x^\epsilon))$"
        )

        ax1.set_xlabel("risk " + r"$\rho = \mathrm{E}\,x^T\xi + \mathcal{R}_{\alpha,\gamma}(-x^T\xi)$")
        ax1.set_ylabel("return " + r"$\mu = \mathrm{E}\,x^\top\xi$")

        ax1.set_xlim(0, 0.5)
        ax1.set_ylim(0, 0.5)

        ax1.set_xticks([i/10 for i in range(6)])
        ax1.set_yticks([i/10 for i in range(6)])

        ax1.grid(linewidth=0.25)

        ax1.legend(loc="best")

        plt.xticks(rotation=45)
        plt.show()

        fig.savefig("C:/Users/j.rode/Desktop/Markowitz/plot/assets/plotMeanRiskMeasureLinearProgramming05.svg")

    def plotSensitivityElasticityMarkowitz(self, portfolio):
        my = np.linspace(0, 1, num=int(1e+2))

        sensitivity = self.analysis.sensitivity(portfolio, "markowitz")*np.ones(len(my))
        elasticity = []
        
        for m in my:
            x = FiMa.allocationBasic(
                time=portfolio.getTime(),
                stocks=portfolio.getStocks(),
                minimumReturn=m
            )
            elasticity.append(m/np.linalg.norm(x)*sensitivity[0])

        fig, ax1 = plt.subplots(figsize=(15, 10))
        # ax2 = ax1.twinx()

        ax1.plot(my, sensitivity, ".-", label="sensitivity", color="dodgerblue")
        ax1.plot(my, elasticity, ".-", label="elasticity", color="midnightblue")
        
        ax1.set_xlim(my[0], my[-1])
        ax1.set_ylim(0, 5)

        ax1.set_xlabel("parameter " + r"$\mu$")
        ax1.set_ylabel("sensitivity " + r"$\mathcal{S}\,(\mu)$" + "\nelasticity " + r"$\mathcal{E}\,(\mu)$")

        ax1.grid(linewidth=0.25)
        ax1.legend(loc="best")

        plt.show()

        fig.savefig("C:/Users/j.rode/Desktop/Markowitz/plot/assets/plotSensitivityElasticityMarkowitz.svg")

    def plotSensitivityElasticityUtilityMaximization(self, portfolio):
        kappa = [1.01**(8*i)-0.9 for i in range(1, 100)]
        # kappa = [1.01**(10*i)-0.9 for i in range(1, 100)]
        
        sensitivity = []
        elasticity = []

        for k in kappa:
            sensitivity.append(
                self.analysis.sensitivity(
                    portfolio=portfolio, 
                    method="utilityMaximization", 
                    theta=k
                )
            )
            x = np.linalg.norm(FiMa.allocationUtilityMaximization(portfolio.getTime(), portfolio.getStocks(), k))
            elasticity.append(k/x*sensitivity[-1])

        controlLine1 = []
        controlLine2 = []

        for k in kappa:
            controlLine1.append(10*k**(-1))
            controlLine2.append(10*k**(-2))

        fig, ax1 = plt.subplots(figsize=(15, 10))
        # ax2 = ax1.twinx()

        cmap    = plt.cm.get_cmap("Blues")
        colors  = cmap(np.linspace(0.2, 1.0, 3))

        ax1.plot(kappa, sensitivity, ".-", label="sensitivity", color=colors[1])
        ax1.plot(kappa, controlLine2, label=r"$\mathcal{O}(\kappa^{-2})$", color=colors[0])
        ax1.plot(kappa, elasticity, ".-", label="elasticity", color=colors[2])
        ax1.plot(kappa, controlLine1, label=r"$\mathcal{O}(\kappa^{-1})$", color=colors[0])

        ax1.set_xlim(kappa[0], kappa[-1])

        ax1.set_xlabel("parameter " + r"$\kappa$")
        ax1.set_ylabel("sensitivity " + r"$\mathcal{S}\,(\mu)$" + "\nelasticity " + r"$\mathcal{E}\,(\mu)$")

        ax1.set_xscale("log")
        ax1.set_yscale("log")

        ax1.grid(linewidth=0.25)
        ax1.legend(loc="best")

        plt.show()

        fig.savefig("C:/Users/j.rode/Desktop/Markowitz/plot/assets/plotSensitivityElasticityUtilityMaximization.svg")

    def plotElasticityUtilityMaximization(self, portfolio):
        kappa = [1.01**(10*i)-0.9 for i in range(1, 100)]
        
        sensitivityAnalysis = SensitivityAnalysis()
        sensitivity = []
        for k in kappa:
            sensitivity.append(
                sensitivityAnalysis.sensitivity(
                    portfolio, 
                    "utilityMaximization", 
                    k
                )
            )

        elasticity = []
        i = 0
        for k in kappa:
            x = np.linalg.norm(FiMa.allocationUtilityMaximization(portfolio.getTime(), portfolio.getStocks(), k))
            elasticity.append(k/x*sensitivity[i])
            i += 1

        controlLine = []
        for k in kappa:
            controlLine.append(10*k**(-1))

        fig, ax1 = plt.subplots(figsize=(15, 10))
        # ax2 = ax1.twinx()

        cmap    = plt.cm.get_cmap("Blues")
        colors  = cmap(np.linspace(0.2, 1.0, 2))

        ax1.plot(kappa, elasticity, ".-", label="elasticity", color=colors[1])
        ax1.plot(kappa, controlLine, label=r"$\mathcal{O}(\kappa^{-1})$", color=colors[0])

        ax1.set_xlim(kappa[0], kappa[-1])

        ax1.set_xlabel("parameter " + r"$\kappa$")
        ax1.set_ylabel("elasticity " + r"$\mathcal{E}\,(\kappa)$")

        ax1.set_xscale("log")
        ax1.set_yscale("log")

        ax1.grid(linewidth=0.25)
        ax1.legend(loc="best")

        plt.show()

        fig.savefig("C:/Users/j.rode/Desktop/Markowitz/plot/assets/plotElasticityUtilityMaximization.svg")

    def plotSensitivityElasticityLinearProgramming(self, portfolio):
        my = np.linspace(0.07, 1, num=int(1e+2))

        delta = 1e-3
        myDelta = my + delta

        sensitivity = []
        elasticity = []
        
        for i in range(len(my)):
            x = FiMa.allocationLinearProgramming(
                time=portfolio.getTime(),
                stocks=portfolio.getStocks(),
                minimumReturn=my[i]
            )
            xDelta = FiMa.allocationLinearProgramming(
                time=portfolio.getTime(),
                stocks=portfolio.getStocks(),
                minimumReturn=myDelta[i]
            )
            sensitivity.append(np.linalg.norm(x-xDelta)/delta)
            elasticity.append(sensitivity[-1]*my[i]/np.linalg.norm(x))

        fig, ax1 = plt.subplots(figsize=(15, 10))
        # ax2 = ax1.twinx()

        ax1.plot(my, sensitivity, ".-", label="sensitivity", color="dodgerblue")
        ax1.plot(my, elasticity, ".-", label="elasticity", color="midnightblue")
        
        ax1.set_xlim(my[0], my[-1])
        ax1.set_ylim(0, 5)

        ax1.set_xlabel("parameter " + r"$\mu$")
        ax1.set_ylabel("sensitivity " + r"$\mathcal{S}\,(\mu)$" + "\nelasticity " + r"$\mathcal{E}\,(\mu)$")

        ax1.grid(linewidth=0.25)
        ax1.legend(loc="best")

        plt.show()

        fig.savefig("C:/Users/j.rode/Desktop/Markowitz/plot/assets/plotSensitivityElasticityLinearProgramming.svg")