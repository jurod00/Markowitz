import numpy as np
import matplotlib.pyplot as plt

from mathematics.financialMathematics import FinancialMathematics as FiMa

class PlotSensitivityAnalysis:
    def __init__(self, model, portfolio, sensitivityAnalysis):
        self.model = model
        self.portfolio = portfolio
        self.sensitivityAnalysis = sensitivityAnalysis

        self.alphaDefault = 0.95
        self.gammaDefault = 0.5
        self.myDefault = 0.07

    def plotMeanVariance(self, epsilon: float) -> None:
        fig, ax1 = plt.subplots(figsize=(15, 10))
        # ax2 = ax1.twinx()

        a, b, c, _ = FiMa.abcd(
            time=self.portfolio.getTime(), 
            stocks=self.portfolio.getStocks()
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
        allocations = self.sensitivityAnalysis.allocationsNoisy(portfolio=self.portfolio, epsilon=epsilon, model=self.model)
        myScatter, sigmaScatter = self.sensitivityAnalysis.meanVarianceScatterData(portfolio=self.portfolio, allocations=allocations)

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

        ax1.set_xlabel("risk " + r"$\sigma = \sqrt{\mathrm{var}\,x^\top\xi}$")
        ax1.set_ylabel("return " + r"$\mu = \mathrm{E}\,x^\top\xi$")

        ax1.set_xlim(0, 0.5)
        ax1.set_ylim(0, 0.5)

        ax1.set_xticks([i/10 for i in range(6)])
        ax1.set_yticks([i/10 for i in range(6)])

        ax1.grid(linewidth=0.25)

        ax1.legend(loc="best")

        plt.xticks(rotation=45)
        plt.show()

        fig.savefig("C:/Users/j.rode/Desktop/Markowitz/plot/assets/plotMeanVariance" + self.model + str(epsilon*1000)[:2] + ".svg")

    def plotMeanRiskmeasure(self, epsilon: float) -> None:
        # Portfolios with noise
        # my = [i/10000 for i in range(10000)]
        my = np.linspace(0.07, 0.5, num=int(1e+4))
        riskMeasure = []

        for m in my:
            objTemp = FiMa.objectiveLinearProgramming(
                time=self.portfolio.getTime(),
                stocks=self.portfolio.getStocks(),
                alpha=self.alphaDefault,
                gamma=self.gammaDefault,
                minimumReturn=m
            )
            riskMeasure.append(objTemp)

        allocations = self.sensitivityAnalysis.allocationsNoisy(self.portfolio, epsilon, "linearProgramming")
        myScatter, objectiveScatter = self.sensitivityAnalysis.meanObjectiveScatterData(self.portfolio, allocations, self.alphaDefault, self.gammaDefault)

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

        fig.savefig("C:/Users/j.rode/Desktop/Markowitz/plot/assets/plotMeanRiskMeasureLinearProgramming" + str(epsilon*1000)[:2] + ".svg")

    def plotSensitivityElasticityMarkowitz(self) -> None:
        my = np.linspace(0, 1, num=int(1e+2))

        sensitivity = self.sensitivityAnalysis.sensitivity(self.portfolio, "markowitz")*np.ones(len(my))
        elasticity = []
        
        for m in my:
            x = FiMa.allocationBasic(
                time=self.portfolio.getTime(),
                stocks=self.portfolio.getStocks(),
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

    def plotSensitivityElasticityUtilityMaximization(self) -> None:
        kappas = [1.01**(8*i)-0.9 for i in range(1, 100)]
        # kappa = [1.01**(10*i)-0.9 for i in range(1, 100)]
        
        sensitivity = []
        elasticity = []

        for kappa in kappas:
            sensitivity.append(
                self.sensitivityAnalysis.sensitivity(
                    portfolio=self.portfolio, 
                    model=self.model, 
                    theta=kappa
                )
            )
            x = np.linalg.norm(FiMa.allocationUtilityMaximization(self.portfolio.getTime(), self.portfolio.getStocks(), kappa))
            elasticity.append(kappa/x*sensitivity[-1])

        controlLine1 = []
        controlLine2 = []

        for kappa in kappas:
            controlLine1.append(10*kappa**(-1))
            controlLine2.append(10*kappa**(-2))

        fig, ax1 = plt.subplots(figsize=(15, 10))
        # ax2 = ax1.twinx()

        cmap    = plt.cm.get_cmap("Blues")
        colors  = cmap(np.linspace(0.2, 1.0, 3))

        ax1.plot(kappas, sensitivity, ".-", label="sensitivity", color=colors[1])
        ax1.plot(kappas, controlLine2, label=r"$\mathcal{O}(\kappa^{-2})$", color=colors[0])
        ax1.plot(kappas, elasticity, ".-", label="elasticity", color=colors[2])
        ax1.plot(kappas, controlLine1, label=r"$\mathcal{O}(\kappa^{-1})$", color=colors[0])

        ax1.set_xlim(kappas[0], kappas[-1])

        ax1.set_xlabel("parameter " + r"$\kappa$")
        ax1.set_ylabel("sensitivity " + r"$\mathcal{S}\,(\mu)$" + "\nelasticity " + r"$\mathcal{E}\,(\mu)$")

        ax1.set_xscale("log")
        ax1.set_yscale("log")

        ax1.grid(linewidth=0.25)
        ax1.legend(loc="best")

        plt.show()

        fig.savefig("C:/Users/j.rode/Desktop/Markowitz/plot/assets/plotSensitivityElasticityUtilityMaximization.svg")

    def plotElasticityUtilityMaximization(self, portfolio) -> None:
        kappa = [1.01**(10*i)-0.9 for i in range(1, 100)]
        
        #sensitivityAnalysis = SensitivityAnalysis()
        sensitivity = []
        for k in kappa:
            sensitivity.append(
                self.sensitivityAnalysis.sensitivity(
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

    def plotSensitivityElasticityLinearProgrammingMy(self) -> None:
        mys = np.linspace(0.07, 1, num=int(1e+2))

        sensitivity = []
        elasticity = []
        
        for my in mys:
            x = FiMa.allocationLinearProgramming(
                time=self.portfolio.getTime(),
                stocks=self.portfolio.getStocks(),
                alpha=self.alphaDefault,
                gamma=self.gammaDefault,
                minimumReturn=my
            )
            sensitivity.append(self.sensitivityAnalysis.sensitivityNew("LinearProgramming", "my", self.portfolio, my))
            elasticity.append(sensitivity[-1]*my/np.linalg.norm(x))

        fig, ax1 = plt.subplots(figsize=(15, 10))
        # ax2 = ax1.twinx()

        ax1.plot(mys, sensitivity, ".-", label="sensitivity", color="dodgerblue")
        ax1.plot(mys, elasticity, ".-", label="elasticity", color="midnightblue")
        
        ax1.set_xlim(mys[0], mys[-1])
        ax1.set_ylim(0, 5)

        ax1.set_xlabel("parameter " + r"$\mu$")
        ax1.set_ylabel("sensitivity " + r"$\mathcal{S}\,(\mu)$" + "\nelasticity " + r"$\mathcal{E}\,(\mu)$")

        ax1.grid(linewidth=0.25)
        ax1.legend(loc="best")

        plt.show()

        fig.savefig("C:/Users/j.rode/Desktop/Markowitz/plot/assets/plotSensitivityElasticityLinearProgrammingMy.svg")

    def plotSensitivityElasticityLinearProgrammingAlpha(self) -> None:
        alphas = np.linspace(0.9, 0.99, num=int(1e+2))

        sensitivity = []
        
        for alpha in alphas:
            sensitivity.append(self.sensitivityAnalysis.sensitivityNew("LinearProgramming", "alpha", self.portfolio, alpha))

        fig, ax1 = plt.subplots(figsize=(15, 10))
        # ax2 = ax1.twinx()

        ax1.plot(alphas, sensitivity, ".-", label="sensitivity", color="dodgerblue")
        
        ax1.set_xlim(alphas[0], alphas[-1])
        ax1.set_ylim(-0.05, 1)

        ax1.set_xlabel("parameter " + r"$\alpha$")
        ax1.set_ylabel("sensitivity " + r"$\mathcal{S}\,(\alpha)$")

        ax1.grid(linewidth=0.25)
        ax1.legend(loc="best")

        plt.show()

        fig.savefig("C:/Users/j.rode/Desktop/Markowitz/plot/assets/plotSensitivityElasticityLinearProgrammingAlpha.svg")

    def plotSensitivityElasticityLinearProgrammingGamma(self) -> None:
        gammas = np.linspace(0.4, 0.99, num=int(1e+2))

        sensitivity = []
        elasticity = []
        
        for gamma in gammas:
            x = FiMa.allocationLinearProgramming(
                time=self.portfolio.getTime(),
                stocks=self.portfolio.getStocks(),
                alpha=self.alphaDefault,
                gamma=gamma,
                minimumReturn=self.myDefault
            )
            sensitivity.append(self.sensitivityAnalysis.sensitivityNew("LinearProgramming", "gamma", self.portfolio, gamma))
            elasticity.append(sensitivity[-1]*gamma/np.linalg.norm(x))

        fig, ax1 = plt.subplots(figsize=(15, 10))
        # ax2 = ax1.twinx()

        ax1.plot(gammas, sensitivity, ".-", label="sensitivity", color="dodgerblue")
        #ax1.plot(gammas, elasticity, ".-", label="elasticity", color="midnightblue")
        
        ax1.set_xlim(gammas[0], gammas[-1])
        # ax1.set_ylim(0, 5)

        ax1.set_xlabel("parameter " + r"$\gamma$")
        ax1.set_ylabel("sensitivity " + r"$\mathcal{S}\,(\gamma)$" + "\nelasticity " + r"$\mathcal{E}\,(\gamma)$")

        ax1.grid(linewidth=0.25)
        ax1.legend(loc="best")

        plt.show()

        fig.savefig("C:/Users/j.rode/Desktop/Markowitz/plot/assets/plotSensitivityElasticityLinearProgrammingGamma.svg")