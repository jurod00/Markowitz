from portfolio.portfolio import Portfolio

import pathlib as pl
import matplotlib.dates as date
import matplotlib.pyplot as plt

class PlotStocks:

    def __init__(self, portfolio: Portfolio):
        # Memory Property
        self.portfolio = portfolio
        # Design
        self._color = plt.get_cmap("Greens")

    def plotStocksAbs(self):
        times = list(self.portfolio.times)
        stocks = list(self.portfolio.stocks)
        symbols = list(self.portfolio.symbols)

        d = len(stocks)

        fig, ax = plt.subplots()
        
        for j, stock in enumerate(stocks):
            ax.plot(
                times, 
                stock, 
                label=symbols[j], 
                color=self._color((j+1)/d)
            )

        ax.set_ylabel("absolute stock prices " + r"$S_t$")
        ax.xaxis.set_major_formatter(date.DateFormatter(r"%m-%d"))
        
        ax.legend(loc="upper center", ncol=d, frameon=False)
        ax.set_xlim(times[0], times[-1])

        plt.xticks(rotation=45)
        # plt.show()

        pathAssets = pl.Path(__file__).resolve().parent / "assets"
        pathAssets.mkdir(exist_ok=True)

        fig.savefig(pathAssets / "plotStocksAbs.svg")

    def plotStocksRel(self):
        times = list(self.portfolio.times)
        stocks = list(self.portfolio.stocks)
        symbols = list(self.portfolio.symbols)

        d = len(stocks)

        fig, ax = plt.subplots()
        
        for j, stock in enumerate(stocks):
            stocksRel = [stock[i]/stock[0] for i in range(len(times))]
            ax.plot(
                times, 
                stocksRel, 
                label=symbols[j], 
                color=self._color((j+1)/d)
            )

        ax.set_ylabel("relative stock prices " + r"$S_t\,/\,S_0$")
        ax.xaxis.set_major_formatter(date.DateFormatter(r"%m-%d"))
        
        ax.legend(loc="upper center", ncol=d, frameon=False)
        ax.set_xlim(times[0], times[-1])

        plt.xticks(rotation=45)
        # plt.show()

        pathAssets = pl.Path(__file__).resolve().parent / "assets"
        pathAssets.mkdir(exist_ok=True)

        fig.savefig(pathAssets / "plotStocksRel.svg")