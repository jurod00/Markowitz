import numpy as np
import pathlib as pl
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 20})
# plt.style.use("dark_background")

from mathematics.financialMathematics import FinancialMathematics as FiMa

class PlotPortfolioSharesOptions:
    def __init__(self, portfolio):
        self.portfolio = portfolio

        self.alphaDefault = 0.95
        self.gammaDefault = 0.5
        self.myDefault = 0.25 # 0.07

    def colors(self):
        stocks = self.portfolio.getStocks()
        options = self.portfolio.getOptions()

        if len(options["callIndices"]) == 0 and len(options["putIndices"]) == 0:
            colors = len(stocks)*["darkseagreen"]
        elif len(options["callIndices"]) != 0 and len(options["putIndices"]) == 0:
            colors = len(stocks)*["darkseagreen"] + len(stocks)*["limegreen"]
        elif len(options["callIndices"]) == 0 and len(options["putIndices"]) != 0:
            colors = len(stocks)*["darkseagreen"] + len(stocks)*["limegreen"]
        elif len(options["callIndices"]) != 0 and len(options["putIndices"]) != 0:
            colors = len(stocks)*["darkseagreen"] + len(stocks)*["limegreen"] + len(stocks)*["forestgreen"]

        return colors
    
    def markers(self):
        stocks = self.portfolio.getStocks()
        options = self.portfolio.getOptions()

        if len(stocks) == 1:
            stockMarkers = ["o"]
        elif len(stocks) == 2:
            stockMarkers = ["o", "^"]
        elif len(stocks) == 3:
            stockMarkers = ["o", "^", "s"]
        elif len(stocks) == 4:
            stockMarkers = ["o", "^", "s", "*"]
        elif len(stocks) == 5:
            stockMarkers = ["o", "^", "s", "*", "P"]

        if len(options["callIndices"]) == 0 and len(options["putIndices"]) == 0:
            markers = stockMarkers
        elif len(options["callIndices"]) != 0 and len(options["putIndices"]) == 0:
            markers = 2*stockMarkers
        elif len(options["callIndices"]) == 0 and len(options["putIndices"]) != 0:
            markers = 2*stockMarkers
        elif len(options["callIndices"]) != 0 and len(options["putIndices"]) != 0:
            markers = 3*stockMarkers

        return markers

    def plotStocks(self, absRel) -> None:
        fig, ax1 = plt.subplots(figsize=(15,10))
        # ax2 = ax1.twinx()

        time = self.portfolio.getTime()
        stocks = self.portfolio.getStocks()
        symbols = self.portfolio.getSymbols()

        colors = ["lightgreen", "limegreen", "forestgreen", "darkgreen"]
        markers = self.markers()

        J = len(stocks)

        if absRel == "abs":
            for j in range(J):
                ax1.plot(
                    time, 
                    stocks[j], 
                    color=colors[j], 
                    label=symbols[j], 
                    marker=markers[j], 
                    markeredgecolor=colors[j],
                    markerfacecolor="white"
                )

        if absRel == "rel":
            for j in range(J):
                stocksRel = [stocks[j][i]/stocks[j][0] for i in range(len(time))]

                ax1.plot(
                    time, 
                    stocksRel, 
                    color=colors[j], 
                    label=symbols[j], 
                    marker=markers[j], 
                    markeredgecolor=colors[j],
                    markerfacecolor="white"
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

        fig.savefig(pathAssets / "plotStocks.svg")

    def plotAllocationMarkowitz(self, returnMin: float=0.0, returnMax: float=0.25) -> None:
        fig, ax1 = plt.subplots(figsize=(15, 10))
        # ax2 = ax1.twinx()

        time = self.portfolio.getTime()
        stocks = self.portfolio.getStocks()
        options = self.portfolio.getOptions()
        symbols = self.portfolio.getSymbols()

        J = len(symbols)

        x0 = FiMa.allocationBasic(time=time, stocks=stocks, minimumReturn=returnMin, options=options)
        x1 = FiMa.allocationBasic(time=time, stocks=stocks, minimumReturn=returnMax, options=options)

        _, b, c, _ = FiMa.abcd(time=time, stocks=stocks, options=options)

        colors = self.colors()
        markers = self.markers()

        for j in range(J):
            m = (x1[j] - x0[j])/(returnMax - returnMin)
            n = x0[j] - m*returnMin

            mys = np.linspace(returnMin, returnMax, 50)
            y = m*np.linspace(returnMin, returnMax, 50) + n
            
            ax1.plot(
                mys, 
                y, 
                color=colors[j], 
                label=symbols[j], 
                marker=markers[j], 
                markeredgecolor=colors[j], 
                markerfacecolor="white"
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

        fig.savefig(pathAssets / "plotAllocationMarkowitz.svg")

    def plotAllocationLinearProgramming(self, alpha: float=0.95, gamma: float=0.5, returnMin: float=0.0, returnMax: float=0.25) -> None:
        fig, ax1 = plt.subplots(figsize=(15, 10))
        # ax2 = ax1.twinx()

        time = self.portfolio.getTime()
        stocks = self.portfolio.getStocks()
        options = self.portfolio.getOptions()
        symbols = self.portfolio.getSymbols()

        J = len(symbols)

        mys = np.linspace(returnMin, returnMax, num=int(5e+1))

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
                minimumReturn=my,
                options=options
            )
            allocations.append(x)

        colors = self.colors()
        markers = self.markers()

        for j in range(J):
            y = [allocations[i][j] for i in range(len(mys))]
            
            ax1.plot(
                mys, 
                y, 
                color=colors[j], 
                label=symbols[j], 
                marker=markers[j], 
                markeredgecolor=colors[j], 
                markerfacecolor="white"
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

        fig.savefig(pathAssets / "plotAllocationLinearProgramming.svg")