from portfolio.portfolio import Portfolio

import pathlib as pl
import matplotlib.dates as mdates
import matplotlib.ticker as mtick
import matplotlib.pyplot as plt

plt.rcParams.update(
    {
        "font.size": 16,
        "axes.titlesize": 14,
        "axes.labelsize": 14,
        "xtick.labelsize": 12,
        "ytick.labelsize": 16,
        "legend.fontsize": 14,
    }
)

class PlotStocks:

    def __init__(self, portfolio: Portfolio):
        # Memory
        self.portfolio = portfolio
        # Design
        self._color = plt.get_cmap("Greens")

    def plotStocksAbs(self, format: str="svg"):
        times = list(self.portfolio.times)
        stocks = list(self.portfolio.stocks)
        symbols = list(self.portfolio.symbols)

        d = len(stocks)

        fig, ax = plt.subplots(figsize=(7, 4.5), layout="constrained")
        
        for j, stock in enumerate(stocks):
            ax.plot(
                times, 
                stock, 
                label=symbols[j], 
                color=self._color((j+1)/d)
            )

        # x-axis
        plt.xticks(rotation=45)
        ax.set_xlim(times[0], times[-1])
        ax.xaxis.set_major_formatter(mdates.DateFormatter(r"%B %d"))
        
        # y-axis
        ax.set_ylabel("absolute stock prices " + r"$S_t$ in $\$$")

        # legend
        ax.legend(loc="upper center", ncol=d, frameon=False)
        
        pathAssets = pl.Path(__file__).resolve().parent / "assets"
        pathAssets.mkdir(exist_ok=True)

        fig.savefig(pathAssets / f"plotStocksAbs.{format}", bbox_inches="tight", pad_inches=0.05)

    def plotStocksRel(self, format: str="svg"):
        times = list(self.portfolio.times)
        stocks = list(self.portfolio.stocks)
        symbols = list(self.portfolio.symbols)

        d = len(stocks)

        fig, ax = plt.subplots(figsize=(7, 4.5), layout="constrained")
        
        for j, stock in enumerate(stocks):
            stocksRel = [stock[i]/stock[0] for i in range(len(times))]
            ax.plot(
                times, 
                stocksRel, 
                label=symbols[j], 
                color=self._color((j+1)/d)
            )
        
        # x-axis
        plt.xticks(rotation=45)
        ax.set_xlim(times[0], times[-1])
        ax.xaxis.set_major_formatter(mdates.DateFormatter(r"%B %d"))

        # y-axis
        ax.set_ylabel("relative stock prices " + r"$S_t\,/\,S_0$")
        ax.yaxis.set_major_formatter(mtick.FormatStrFormatter("%.1f"))
        ax.yaxis.set_major_locator(mtick.MultipleLocator(0.1))

        # legend
        ax.legend(loc="upper center", ncol=d, frameon=False)
        
        pathAssets = pl.Path(__file__).resolve().parent / "assets"
        pathAssets.mkdir(exist_ok=True)

        fig.savefig(pathAssets / f"plotStocksRel.{format}", bbox_inches="tight", pad_inches=0.05)