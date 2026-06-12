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
        options = self.portfolio.getOptions()
        symbols = self.portfolio.getSymbols()

        J = len(symbols)

        x0 = FiMa.allocationBasic(time=time, stocks=stocks, minimumReturn=returnMin, options=options)
        x1 = FiMa.allocationBasic(time=time, stocks=stocks, minimumReturn=returnMax, options=options)

        _, b, c, _ = FiMa.abcd(time=time, stocks=stocks, options=options)

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
            # print(my)
            x = FiMa.allocationLinearProgramming(
                time=time,
                stocks=stocks,
                alpha=alpha,
                gamma=gamma,
                minimumReturn=my,
                options=options
            )
            allocations.append(x)

        if len(stocks) == 1:
            lineStocks = ["o-"]
        elif len(stocks) == 2:
            lineStocks = ["o-", "s-"]
        elif len(stocks) == 3:
            lineStocks = ["o-", "s-", "^-"]
        elif len(stocks) == 4:
            lineStocks = ["o-", "s-", "^-", "*-"]
        elif len(stocks) == 5:
            lineStocks = ["o-", "s-", "^-", "*-", "P-"]

        cmap = plt.cm.get_cmap("Greens")

        if len(options["callIndices"]) == 0 and len(options["putIndices"]) == 0:
            linestyles = lineStocks
            colors = cmap(len(stocks)*[0.3])
        elif len(options["callIndices"]) != 0 and len(options["putIndices"]) == 0:
            linestyles = 2*lineStocks
            colors = cmap(len(stocks)*[0.3] + len(stocks)*[0.6])
        elif len(options["callIndices"]) == 0 and len(options["putIndices"]) != 0:
            linestyles = 2*lineStocks
            colors = cmap(len(stocks)*[0.3] + len(stocks)*[0.6])
        elif len(options["callIndices"]) != 0 and len(options["putIndices"]) != 0:
            linestyles = 3*lineStocks
            colors = cmap(len(stocks)*[0.3] + len(stocks)*[0.6] + len(stocks)*[0.9])

        # linestyles = ["o-", "s-", "^-", "o-", "s-", "^-", "o-", "s-", "^-"]

        # cmap    = plt.cm.get_cmap("Greens")
        # colors  = cmap(np.linspace(0.2, 1.0, J))

        # colors = cmap([0.3, 0.3, 0.3, 0.6, 0.6, 0.6, 0.9, 0.9, 0.9])

        for j in range(J):
            y = [allocations[i][j] for i in range(len(mys))]
            
            ax1.plot(
                mys, 
                y, 
                linestyles[j],
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