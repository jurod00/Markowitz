import matplotlib.pyplot as plt
plt.style.use("dark_background")

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

    def plotAllocation(self, myStart: float=0, myEnde: float=0.25):
        my0 = self.portfolio.getMy0()
        my1 = self.portfolio.getMy1()

        x0 = self.portfolio.getX0()
        x1 = self.portfolio.getX1()

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
        ax1.legend(loc="best")

        plt.xticks(rotation=45)
        plt.show()

        fig.savefig("C:/Users/j.rode/Desktop/Markowitz/plot/assets/plotAllocation.svg")