import numpy as np
import pathlib as pl
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 20})
# plt.style.use("dark_background")

from mathematics.financialMathematics import FinancialMathematics as FiMa

class PlotPortfolioShares:
    def __init__(self, portfolio):
        self.portfolio = portfolio

        self.alphaDefault = 0.95
        self.gammaDefault = 0.5
        self.myDefault = 0.25 # 0.07

    def plotStocks(self, absRel) -> None:
        fig, ax1 = plt.subplots(figsize=(15,10))
        # ax2 = ax1.twinx()

        time = self.portfolio.getTime()
        stocks = self.portfolio.getStocks()
        symbols = self.portfolio.getSymbols()

        J = len(stocks)

        cmap    = plt.cm.get_cmap("Blues")
        colors  = cmap(np.linspace(0.2, 1.0, J))

        if absRel == "abs":
            for j in range(J):
                ax1.plot(
                    time, 
                    stocks[j], 
                    label=symbols[j], 
                    color=colors[j]
                )

        if absRel == "rel":
            for j in range(J):
                stocksTemp = stocks[j]

                for i in range(1, len(time)):
                    stocksTemp[i] /= stocksTemp[0]

                stocksTemp[0] = 1

                ax1.plot(
                    time, 
                    stocksTemp, 
                    label=symbols[j], 
                    color=colors[j]
                )

        ax1.grid(axis="y", linewidth=0.25)
        ax1.legend(loc="best")

        ax1.set_ylabel("relative stock prices " + r"$S_t\,/\,S_0$" + "\n")

        ax1.set_xlim(time[0], time[-1])
        
        plt.xticks(rotation=45)

        # plt.show()

        pathDirectory = pl.Path(__file__).resolve().parent
        pathAssets = pathDirectory / "assets"
        pathAssets.mkdir(exist_ok=True)

        fig.savefig(pathAssets / "plotStocksNew.svg")


    def plotAllocationMarkowitz(self, returnMin: float=0.0, returnMax: float=0.25) -> None:
        fig, ax1 = plt.subplots(figsize=(15, 10))
        # ax2 = ax1.twinx()

        time = self.portfolio.getTime()
        stocks = self.portfolio.getStocks()
        symbols = self.portfolio.getSymbols()

        J = len(symbols)

        x0 = FiMa.allocationBasic(time=time, stocks=stocks, minimumReturn=returnMin)
        x1 = FiMa.allocationBasic(time=time, stocks=stocks, minimumReturn=returnMax)

        _, b, c, _ = FiMa.abcd(time=time, stocks=stocks)

        cmap    = plt.cm.get_cmap("Blues")
        colors  = cmap(np.linspace(0.2, 1.0, J))

        for j in range(J):
            m = (x1[j] - x0[j])/(returnMax - returnMin)
            n = x0[j] - m*returnMin

            ax1.plot(
                [returnMin, returnMax], 
                [m*returnMin + n, m*returnMax + n], 
                linestyle="-", 
                #color=colors[j], 
                label=symbols[j]
            )

        ax1.set_xlabel("\n" + "minimum return " + r"$\mu$")
        ax1.set_ylabel("allocation " + r"$x^*(\mu)$" + "\n")

        ax1.set_xlim(returnMin, returnMax)
        #ax1.set_ylim(-0.05, 1.05)

        ax1.set_yticks([i/10 for i in range(11)])

        ax1.grid(linewidth=0.25)

        ax1.hlines(
            y=0, 
            xmin=returnMin, 
            xmax=returnMax, 
            linewidth=1.5, 
            color="silver", 
            zorder=-1
        )

        ax1.vlines(
            x=b/c, 
            ymin=-0.05, 
            ymax=1.05, 
            linestyle=":", 
            label="minimal risk"
        )

        ax1.legend(loc="best")

        # plt.show()

        pathDirectory = pl.Path(__file__).resolve().parent
        pathAssets = pathDirectory / "assets"
        pathAssets.mkdir(exist_ok=True)

        fig.savefig(pathAssets / "plotAllocationMarkowitzNew.svg")

    # TODO: Verbessern oder weg!
    # def plotMeanVariance(self, sigmaStart: float=0.0, sigmaEnde: float=0.3, allocation=np.empty(0), riskFreeRate: float=0.0) -> None:
    #     fig, ax1 = plt.subplots(figsize=(15, 10))
    #     # ax2 = ax1.twinx()

    #     time = self.portfolio.getTime()
    #     stocks = self.portfolio.getStocks()

    #     a, b, c, _ = FiMa.abcd(time=time, stocks=stocks)

    #     r0 = riskFreeRate
    #     sigmaMarket = np.sqrt((a - 2*r0*b + r0**2*c)/(b - r0*c)**2)
    #     myMarket = (a - r0*b)/(b - r0*c)
    #     sharpeRatio = (myMarket - r0)/sigmaMarket

    #     def mean(sigma):
    #         return b/c + np.sqrt((a - b**2/c)*(sigma**2 - 1/c))
        
    #     def tangent(sigma):
    #         return r0 + sigma*sharpeRatio
        
        

    #     sigma = np.linspace(sigmaStart, sigmaMarket + 0.1*sigmaMarket, num=int(1e+5))
    #     sigmaOpt = 1/np.sqrt(c)
    #     my = np.empty(len(sigma))
    #     myOpt = b/c

    #     for i in range(len(sigma)):
    #         if sigma[i]**2 > 1/c:
    #             my[i] = mean(sigma[i])
    #         else:
    #             my[i] = np.nan
        
    #     ax1.plot(sigma, my, label=r"$\mu(\sigma)$"+" mean-variance")
    #     ax1.plot(sigma, tangent(sigma), label="capital market line")
    #     ax1.plot(sigmaOpt, myOpt, "D", label="minimal-risk allocation")
    #     ax1.plot(sigmaMarket, myMarket, "D", label="market portfolio")

    #     if allocation != np.empty(0):
    #         time = self.portfolio.getTime()
    #         stocks = self.portfolio.getStocks()
            
    #         sigmaAllocation = np.sqrt(FiMa.variance(time=time, stocks=stocks, allocation=allocation))
    #         myAllocation = FiMa.mean(time=time, stocks=stocks, allocation=allocation)
            
    #         ax1.plot(sigmaAllocation, myAllocation, ".", label="chosen allocation")

    #     ax1.set_xlabel("risk " + r"$\sigma$")
    #     ax1.set_ylabel("return " + r"$\mu$")

    #     ax1.set_xlim(sigmaStart, sigmaMarket + 0.1*sigmaMarket)
    #     ax1.set_ylim(0, myMarket + 0.1*myMarket)

    #     ax1.grid(linewidth=0.25)

    #     ax1.legend(loc="best")

    #     plt.xticks(rotation=45)
    #     plt.show()

    #     fig.savefig("C:/Users/j.rode/Desktop/Markowitz/plot/assets/plotMeanVariance.svg")

    def plotAllocationUtilityMaximization(self, riskAversionMin: float=0.1, riskAversionMax: float=float(1e+3)) -> None:
        fig, ax1 = plt.subplots(figsize=(15, 10))
        # ax2 = ax1.twinx()

        time = self.portfolio.getTime()
        stocks = self.portfolio.getStocks()
        symbols = self.portfolio.getSymbols()

        J = len(symbols)

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

        allocations = []
        for kappa in kappas:
            x = FiMa.allocationUtilityMaximization(time=time, stocks=stocks, kappa=kappa)
            allocations.append(x)

        
        cmap    = plt.cm.get_cmap("Blues")
        colors  = cmap(np.linspace(0.2, 1.0, J))

        for j in range(J):
            y = [allocations[i][j] for i in range(len(kappas))]

            ax1.plot(
                kappas, 
                y, 
                linestyle="-",
                label=symbols[j], 
                color=colors[j]
            )

        ax1.set_xlabel("\n" + "risk aversion " + r"$\kappa$")
        ax1.set_ylabel("allocation " + r"$x^*(\kappa)$" + "\n")

        ax1.set_xlim(kappas[0], kappas[-1])
        ax1.set_ylim(-0.05, 1.05)

        ax1.set_xscale("log")
        ax1.set_yticks([0.1*i for i in range(11)])

        ax1.grid(linewidth=0.25)

        ax1.hlines(
            y=0, 
            xmin=kappas[0], 
            xmax=kappas[-1], 
            linewidth=1.5, 
            color="silver", 
            zorder=-1
        )

        ax1.legend(loc="best")

        # plt.show()

        pathDirectory = pl.Path(__file__).resolve().parent
        pathAssets = pathDirectory / "assets"
        pathAssets.mkdir(exist_ok=True)

        fig.savefig(pathAssets / "plotAllocationUtilityMaximizationNew.svg")

    def plotAllocationLinearProgramming(self, alpha: float=0.95, gamma: float=0.5, returnMin: float=0.0, returnMax: float=0.25) -> None:
        fig, ax1 = plt.subplots(figsize=(15, 10))
        # ax2 = ax1.twinx()

        time = self.portfolio.getTime()
        stocks = self.portfolio.getStocks()
        symbols = self.portfolio.getSymbols()

        J = len(symbols)

        mys = np.linspace(returnMin, returnMax, num=int(1e+3))

        if alpha != self.alphaDefault:
            print("Warning: alpha = " + str(alpha) + " != " + str(self.alphaDefault) + " = alphaDefault")
        if gamma != self.gammaDefault:
            print("Warning: gamma = " + str(gamma) + " != " + str(self.gammaDefault) + " = gammaDefault")

        allocations = []
        for my in mys:
            x = FiMa.allocationLinearProgramming(
                time=time,
                stocks=stocks,
                alpha=alpha,
                gamma=gamma,
                minimumReturn=my
            )
            allocations.append(x)

        cmap    = plt.cm.get_cmap("Blues")
        colors  = cmap(np.linspace(0.2, 1.0, J))

        for j in range(J):
            y = [allocations[i][j] for i in range(len(mys))]

            ax1.plot(
                mys, 
                y, 
                linestyle="-",
                label=symbols[j], 
                color=colors[j]
            )

        ax1.set_xlabel("\n" + "minimum return " + r"$\mu$")
        ax1.set_ylabel("allocation " + r"$x^*(\mu)$" + "\n")

        ax1.set_xlim(mys[0], mys[-1])
        ax1.set_ylim(-0.05, 1.05)

        ax1.set_yticks([i/10 for i in range(11)])

        ax1.grid(linewidth=0.25)
        ax1.hlines(y=0, xmin=mys[0], xmax=mys[-1], linewidth=1.5, color="silver", zorder=-1)

        ax1.legend(loc="best")

        # plt.show()

        pathDirectory = pl.Path(__file__).resolve().parent
        pathAssets = pathDirectory / "assets"
        pathAssets.mkdir(exist_ok=True)

        fig.savefig(pathAssets / "plotAllocationLinearProgrammingNew.svg")