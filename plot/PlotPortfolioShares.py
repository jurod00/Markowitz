import numpy as np
import matplotlib.pyplot as plt
plt.style.use("dark_background")

from util import AuxiliaryQuantities as Aq

class PlotPortfolioShares:
    def __init__(self, portfolio):
        self.portfolio = portfolio

    def plotStocks(self, absRel):
        fig, ax1 = plt.subplots(figsize=(15,10))
        # ax2 = ax1.twinx()

        J = len(self.portfolio.symbols)

        if absRel == "abs":
            for j in range(J):
                ax1.plot(self.portfolio.time, self.portfolio.stocks[j], label=self.portfolio.symbols[j])

        if absRel == "rel":
            for j in range(J):
                stocksTemp = self.portfolio.stocks[j]

                for i in range(1, len(self.portfolio.time)):
                    stocksTemp[i] /= stocksTemp[0]

                stocksTemp[0] = 1

                ax1.plot(self.portfolio.time, stocksTemp, label=self.portfolio.symbols[j])

        ax1.grid(axis="y", linewidth=0.25)
        ax1.legend(loc="best")
        
        plt.xticks(rotation=45)
        plt.show()

        fig.savefig("C:/Users/j.rode/Desktop/Markowitz/plot/assets/plotStocks.svg")

    def plotAllocation(self, myStart: float=0.0, myEnde: float=0.25):
        my0 = self.portfolio.getMy0()
        my1 = self.portfolio.getMy1()

        x0 = self.portfolio.getX0()
        x1 = self.portfolio.getX1()

        b = self.portfolio.getB()
        c = self.portfolio.getC()

        labels = self.portfolio.getSymbols()

        fig, ax1 = plt.subplots(figsize=(15, 10))
        # ax2 = ax1.twinx()

        for j in range(len(labels)):
            m = (x1[j] - x0[j])/(my1 - my0)
            n = x0[j] - m*my0

            ax1.plot([myStart, myEnde], [m*myStart+n, m*myEnde+n], linestyle="-", label=labels[j])

        ax1.set_xlabel("minimum return")
        ax1.set_ylabel("allocation")

        ax1.set_xlim(myStart, myEnde)
        ax1.set_ylim(-0.05, 1.05)

        ax1.set_yticks([i/10 for i in range(11)])

        ax1.grid(linewidth=0.25)
        ax1.hlines(y=0, xmin=myStart, xmax=myEnde, linewidth=1.5, color="silver", zorder=-1)
        ax1.vlines(x=b/c, ymin=-0.05, ymax=1.05, linestyle=":", label="minimal risk")

        ax1.legend(loc="best")

        plt.xticks(rotation=45)
        plt.show()

        fig.savefig("C:/Users/j.rode/Desktop/Markowitz/plot/assets/plotAllocation.svg")

    def plotMeanVariance(self, sigmaStart: float=0.0, sigmaEnde: float=0.3, allocation=np.empty(0), riskFreeRate: float=0.0):
        a = self.portfolio.getA()
        b = self.portfolio.getB()
        c = self.portfolio.getC()

        r0 = riskFreeRate
        sigmaMarket = np.sqrt((a - 2*r0*b + r0**2*c)/(b - r0*c)**2)
        myMarket = (a - r0*b)/(b - r0*c)
        sharpeRatio = (myMarket - r0)/sigmaMarket

        def mean(sigma):
            return b/c + np.sqrt((a - b**2/c)*(sigma**2 - 1/c))
        
        def tangent(sigma):
            return r0 + sigma*sharpeRatio
        
        fig, ax1 = plt.subplots(figsize=(15, 10))
        # ax2 = ax1.twinx()

        sigma = np.linspace(sigmaStart, sigmaMarket + 0.1*sigmaMarket, num=int(1e+5))
        sigmaOpt = 1/np.sqrt(c)
        my = np.empty(len(sigma))
        myOpt = b/c

        for i in range(len(sigma)):
            if sigma[i]**2 > 1/c:
                my[i] = mean(sigma[i])
            else:
                my[i] = np.nan
        
        ax1.plot(sigma, my, label=r"$\mu(\sigma)$"+" mean-variance")
        ax1.plot(sigma, tangent(sigma), label="capital market line")
        ax1.plot(sigmaOpt, myOpt, "D", label="minimal-risk allocation")
        ax1.plot(sigmaMarket, myMarket, "D", label="market portfolio")

        if allocation != np.empty(0):
            aq = Aq()

            time = self.portfolio.getTime()
            stocks = self.portfolio.getStocks()

            sigmaAllocation = np.sqrt(aq.variance(time, stocks, allocation))
            myAllocation = aq.mean(time, stocks, allocation)
            
            ax1.plot(sigmaAllocation, myAllocation, ".", label="chosen allocation")

        ax1.set_xlabel("risk " + r"$\sigma$")
        ax1.set_ylabel("return " + r"$\mu$")

        ax1.set_xlim(sigmaStart, sigmaMarket + 0.1*sigmaMarket)
        ax1.set_ylim(0, myMarket + 0.1*myMarket)

        ax1.grid(linewidth=0.25)

        ax1.legend(loc="best")

        plt.xticks(rotation=45)
        plt.show()

        fig.savefig("C:/Users/j.rode/Desktop/Markowitz/plot/assets/plotMeanVariance.svg")

    def plotAllocationUtilityMaximization(self):
        kappas = self.portfolio.getKappas()
        xSet = self.portfolio.getXSet()

        labels = self.portfolio.getSymbols()

        fig, ax1 = plt.subplots(figsize=(15, 10))
        # ax2 = ax1.twinx()

        for j in range(len(xSet[0])):
            x = [xSet[i][j] for i in range(len(kappas))]
            plt.plot(kappas, x, linestyle="-", label=labels[j])

        ax1.set_xlabel("kappa")
        ax1.set_ylabel("allocation")

        ax1.set_xlim(kappas[0], kappas[-1])
        ax1.set_ylim(-0.05, 1.05)

        ax1.set_xscale("log")
        ax1.set_yticks([i/10 for i in range(11)])

        ax1.grid(linewidth=0.25)
        ax1.hlines(y=0, xmin=kappas[0], xmax=kappas[-1], linewidth=1.5, color="silver", zorder=-1)

        ax1.legend(loc="best")

        plt.xticks(rotation=45)
        plt.show()

        fig.savefig("C:/Users/j.rode/Desktop/Markowitz/plot/assets/plotAllocation.svg")

    def plotAllocationLinearProgram(self):
        mySet = self.portfolio.getMySet()
        xSet = self.portfolio.getXSet()

        # b = self.portfolio.getB()
        # c = self.portfolio.getC()

        labels = self.portfolio.getSymbols()

        fig, ax1 = plt.subplots(figsize=(15, 10))
        # ax2 = ax1.twinx()

        for j in range(len(xSet[0])):
            x = [xSet[i][j] for i in range(len(mySet))]
            plt.plot(mySet, x, marker='o', label=labels[j])

        ax1.set_xlabel("kappa")
        ax1.set_ylabel("allocation")

        ax1.set_xlim(mySet[0], mySet[-1])
        ax1.set_ylim(-0.05, 1.05)

        ax1.set_yticks([i/10 for i in range(11)])

        ax1.grid(linewidth=0.25)
        ax1.hlines(y=0, xmin=mySet[0], xmax=mySet[-1], linewidth=1.5, color="silver", zorder=-1)
        # ax1.vlines(x=b/c, ymin=-0.05, ymax=1.05, linestyle=":", label="minimal risk")

        ax1.legend(loc="best")

        plt.xticks(rotation=45)
        plt.show()

        fig.savefig("C:/Users/j.rode/Desktop/Markowitz/plot/assets/plotAllocation.svg")