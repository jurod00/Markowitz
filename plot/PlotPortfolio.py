import matplotlib.pyplot as plt
plt.style.use("dark_background")

class PlotPortfolio:
    def __init__(self, portfolio):
        self.portfolio = portfolio

    def plotStocks(self, absRel):
        fig, ax1 = plt.subplots(figsize=(15,10))
        #ax2 = ax1.twinx()

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
        ax1.legend()
        plt.xticks(rotation=45)
        plt.show()

        #fig.savefig("C:/Users/j.rode/Desktop/Markowitz/plot/plot.svg")

    def plotAllocation(self):

        #myMin, myMax = 0, 0.25
        myMin = self.portfolio.returnMin
        myMax = self.portfolio.returnMax

        xMin = self.portfolio.allocationMin
        xMax = self.portfolio.allocationMax

        #xMin = [0.8, 0.15, 0.1]
        #xMax = [0.2, 0.15, -0.1]

        fig, ax = plt.subplots(figsize=(15, 10))

        for xStart, xEnde in zip(xMin, xMax):
            ax.plot([myMin, myMax], [xStart, xEnde])

        ax.set_xlabel("minimum return")
        ax.set_ylabel("allocation")

        ax.set_xlim(myMin, myMax)
        ax.set_ylim(min(xMin + xMax) - 0.1, max(xMin + xMax) + 0.1)

        ax.grid(linewidth=0.25)
        ax.legend()

        plt.xticks(rotation=45)
        plt.show()