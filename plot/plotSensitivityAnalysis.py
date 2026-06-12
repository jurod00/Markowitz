import numpy as np
import pathlib as pl
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 20})
# plt.style.use("dark_background")

from mathematics.financialMathematics import FinancialMathematics as FiMa
from analysis.sensitivityAnalysis import SensitivityAnalysis as SeAn

class PlotSensitivityAnalysis:
    def __init__(self, model, portfolio):
        self.model = model
        self.portfolio = portfolio

        self.alphaDefault = 0.95
        self.gammaDefault = 0.5
        self.myDefault = 0.25 # 0.07

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
        allocations = SeAn.allocationsNoisy(portfolio=self.portfolio, epsilon=epsilon, model=self.model)
        myScatter, sigmaScatter = SeAn.meanVarianceScatterData(portfolio=self.portfolio, allocations=allocations)

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
        ax1.set_ylabel("return " + r"$\mu = \mathrm{E}\,x^\top\xi$" + "\n")

        ax1.set_xlim(0, 0.5)
        ax1.set_ylim(0, 0.5)

        ax1.set_xticks([0.1*i for i in range(0, 6)])
        ax1.set_yticks([0.1*i for i in range(1, 6)])

        ax1.grid(linewidth=0.25)

        ax1.legend(loc="best")

        # plt.show()

        pathDirectory = pl.Path(__file__).resolve().parent
        pathAssets = pathDirectory / "assets"
        pathAssets.mkdir(exist_ok=True)

        fig.savefig(pathAssets / ("C:/Users/j.rode/Desktop/Markowitz/plot/assets/plotMeanVariance" + self.model + str(epsilon*1000)[:2] + "New.svg"))

    def plotMeanRiskmeasure(self, epsilon: float) -> None:
        fig, ax1 = plt.subplots(figsize=(15, 10))
        # ax2 = ax1.twinx()

        mys = np.linspace(0, 1, num=int(1e+4))
        riskMeasure = []

        for my in mys:
            objTemp = FiMa.objectiveLinearProgramming(
                time=self.portfolio.getTime(),
                stocks=self.portfolio.getStocks(),
                alpha=self.alphaDefault,
                gamma=self.gammaDefault,
                minimumReturn=my
            )
            riskMeasure.append(objTemp)

        allocations = SeAn.allocationsNoisy(self.portfolio, epsilon, "LinearProgramming")
        myScatter, objectiveScatter = SeAn.meanObjectiveScatterData(self.portfolio, allocations, self.alphaDefault, self.gammaDefault)

        ax1.plot(
            riskMeasure, 
            mys, 
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

        ax1.set_xlabel("\n" + "risk " + r"$\rho = (1-\gamma)\,\mathrm{E}(-x^\top\xi) + \gamma\,\mathrm{AVaR}_\alpha(-x^\top\xi)$")
        ax1.set_ylabel("return " + r"$\mu = \mathrm{E}\,x^\top\xi$" + "\n")

        ax1.set_xlim(0, 0.5)
        ax1.set_ylim(0, 0.5)

        ax1.set_xticks([0.1*i for i in range(0, 6)])
        ax1.set_yticks([0.1*i for i in range(1, 6)])

        ax1.grid(linewidth=0.25)

        ax1.legend(loc="best")

        # plt.show()

        pathDirectory = pl.Path(__file__).resolve().parent
        pathAssets = pathDirectory / "assets"
        pathAssets.mkdir(exist_ok=True)

        fig.savefig(pathAssets / ("plotMeanRiskMeasureLinearProgramming" + str(epsilon*1000)[:2] + "New.svg"))

    def plotSensitivityElasticityMarkowitz(self) -> None:
        mys = np.linspace(0, 1, num=int(1e+2))

        sensitivity = []
        elasticity = []
        
        for my in mys:
            x = FiMa.allocationBasic(
                time=self.portfolio.getTime(),
                stocks=self.portfolio.getStocks(),
                minimumReturn=my
            )
            sensitivity.append(SeAn.sensitivityNew("Markowitz", "my", self.portfolio, my))
            elasticity.append(sensitivity[-1]*my/np.linalg.norm(x))

        fig, ax1 = plt.subplots(figsize=(15, 10))
        # ax2 = ax1.twinx()

        ax1.plot(mys, sensitivity, "-", label="sensitivity", color="dodgerblue")
        ax1.plot(mys, elasticity, "--", label="elasticity", color="midnightblue")
        
        ax1.set_xlim(mys[0], mys[-1])

        ax1.set_yticks(ticks=[i for i in range(6)])

        ax1.set_xlabel("\n" + "parameter " + r"$\mu$")
        ax1.set_ylabel("sensitivity " + r"$\mathcal{S}\,(\mu)$" + "\nelasticity " + r"$\mathcal{E}\,(\mu)$" + "\n")

        ax1.grid(linewidth=0.25)
        ax1.legend(loc="best")

        # plt.show()

        pathDirectory = pl.Path(__file__).resolve().parent
        pathAssets = pathDirectory / "assets"
        pathAssets.mkdir(exist_ok=True)

        fig.savefig(pathAssets / "plotSensitivityElasticityMarkowitzNew.svg")

    def plotSensitivityElasticityUtilityMaximization(self, riskAversionMin: float=0.1, riskAversionMax: float=float(1e+3)) -> None:
        # kappas = [1.01**(8*i)-0.9 for i in range(1, 100)]
        # kappa = [1.01**(10*i)-0.9 for i in range(1, 100)]

        time = self.portfolio.getTime()
        stocks = self.portfolio.getStocks()

        base = 10
        start = np.log(riskAversionMin)/np.log(base)
        stop = np.log(riskAversionMax)/np.log(base)

        kappas = np.logspace(
            start=start, 
            stop=stop, 
            num=int(1e+3), 
            endpoint=True, 
            base=base
        )
        
        sensitivity = []
        elasticity = []

        for kappa in kappas:
            x = np.linalg.norm(
                FiMa.allocationUtilityMaximization(
                time=time, 
                stocks=stocks, 
                kappa=kappa
                )
            )
            sensitivity.append(
                SeAn.sensitivityNew(
                    model="UtilityMaximization", 
                    parameter="kappa", 
                    portfolio=self.portfolio, 
                    theta=kappa
                )
            )
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

        ax1.plot(kappas, sensitivity, "-", label="sensitivity", color=colors[1], zorder=3)
        ax1.plot(kappas, controlLine2, "-", label=r"$\mathcal{O}(\kappa^{-2})$", color=colors[0], zorder=1)
        ax1.plot(kappas, elasticity, "--", label="elasticity", color=colors[2], zorder=4)
        ax1.plot(kappas, controlLine1, "--", label=r"$\mathcal{O}(\kappa^{-1})$", color=colors[0], zorder=2)

        ax1.set_xlim(kappas[0], kappas[-1])

        ax1.set_xlabel("\n" + "parameter " + r"$\kappa$")
        ax1.set_ylabel("sensitivity " + r"$\mathcal{S}\,(\kappa)$" + "\nelasticity " + r"$\mathcal{E}\,(\kappa)$" + "\n")

        ax1.set_xscale("log")
        ax1.set_yscale("log")

        ax1.grid(linewidth=0.25)
        ax1.legend(loc="best")

        # plt.show()

        pathDirectory = pl.Path(__file__).resolve().parent
        pathAssets = pathDirectory / "assets"
        pathAssets.mkdir(exist_ok=True)

        fig.savefig(pathAssets / "plotSensitivityElasticityUtilityMaximizationNew.svg")

    def plotSensitivityElasticityLinearProgrammingMy(self) -> None:
        mys = np.linspace(0, 0.4, num=int(1e+2))

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
            sensitivity.append(SeAn.sensitivityNew("LinearProgramming", "my", self.portfolio, my))

            if sensitivity[-1] == None:
                elasticity.append(None)
            else:
                elasticity.append(sensitivity[-1]*my/np.linalg.norm(x))

        fig, ax1 = plt.subplots(figsize=(15, 10))
        # ax2 = ax1.twinx()

        ax1.plot(mys, sensitivity, "-", label="sensitivity", color="dodgerblue", zorder=1)
        ax1.plot(mys, elasticity, "--", label="elasticity", color="midnightblue", zorder=2)
        
        ax1.set_xlim(mys[0], mys[-1])

        ax1.set_xlabel("\n" + "parameter " + r"$\mu$")
        ax1.set_ylabel("sensitivity " + r"$\mathcal{S}\,(\mu)$" + "\nelasticity " + r"$\mathcal{E}\,(\mu)$" + "\n")

        ax1.grid(linewidth=0.25)
        ax1.legend(loc="best")

        # plt.show()

        pathDirectory = pl.Path(__file__).resolve().parent
        pathAssets = pathDirectory / "assets"
        pathAssets.mkdir(exist_ok=True)

        fig.savefig(pathAssets / "plotSensitivityElasticityLinearProgrammingMy.svg")

    def plotSensitivityElasticityLinearProgrammingAlpha(self) -> None:
        alphas = np.linspace(0, 0.98, num=int(1e4))

        sensitivity = []
        elasticity = []
        
        for alpha in alphas:
            x = FiMa.allocationLinearProgramming(
                time=self.portfolio.getTime(),
                stocks=self.portfolio.getStocks(),
                alpha=alpha,
                gamma=self.gammaDefault,
                minimumReturn=self.myDefault
            )
            sensitivity.append(SeAn.sensitivityNew("LinearProgramming", "alpha", self.portfolio, alpha))
            elasticity.append(sensitivity[-1]*alpha/np.linalg.norm(x))

        alphas = np.append(alphas, [1])
        sensitivity.append(0)
        elasticity.append(0)

        fig, ax1 = plt.subplots(figsize=(15, 10))
        # ax2 = ax1.twinx()

        ax1.plot(alphas, sensitivity, "-", label="sensitivity", color="dodgerblue", zorder=1)
        ax1.plot(alphas, elasticity, "--", label="elasticity", color="midnightblue", zorder=2)
        
        ax1.set_xlim(alphas[0], alphas[-1])

        ax1.set_xlabel("\n" + "parameter " + r"$\alpha$")
        ax1.set_ylabel("sensitivity " + r"$\mathcal{S}\,(\alpha)$" + "\nelasticity " + r"$\mathcal{E}\,(\alpha)$" + "\n")

        ax1.set_xticks([0.1*i for i in range(11)])

        ax1.grid(linewidth=0.25)
        ax1.legend(loc="best")

        # plt.show()

        pathDirectory = pl.Path(__file__).resolve().parent
        pathAssets = pathDirectory / "assets"
        pathAssets.mkdir(exist_ok=True)

        fig.savefig(pathAssets / "plotSensitivityElasticityLinearProgrammingAlpha.svg")

    def plotSensitivityElasticityLinearProgrammingGamma(self) -> None:
        gammas = np.linspace(0, 1, num=int(1e+4))

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
            sensitivity.append(SeAn.sensitivityNew("LinearProgramming", "gamma", self.portfolio, gamma))
            elasticity.append(sensitivity[-1]*gamma/np.linalg.norm(x))

        fig, ax1 = plt.subplots(figsize=(15, 10))
        # ax2 = ax1.twinx()

        ax1.plot(gammas, sensitivity, "-", label="sensitivity", color="dodgerblue", zorder=1)
        ax1.plot(gammas, elasticity, "--", label="elasticity", color="midnightblue", zorder=2)
        
        ax1.set_xlim(gammas[0], gammas[-1])

        ax1.set_xlabel("\n" + "parameter " + r"$\gamma$")
        ax1.set_ylabel("sensitivity " + r"$\mathcal{S}\,(\gamma)$" + "\nelasticity " + r"$\mathcal{E}\,(\gamma)$" + "\n")

        ax1.grid(linewidth=0.25)
        ax1.legend(loc="best")

        # plt.show()

        pathDirectory = pl.Path(__file__).resolve().parent
        pathAssets = pathDirectory / "assets"
        pathAssets.mkdir(exist_ok=True)

        fig.savefig(pathAssets / "plotSensitivityElasticityLinearProgrammingGamma.svg")