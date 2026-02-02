import matplotlib.pyplot as plt
plt.style.use("dark_background")

class PlotPortfolio:
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

        #fig.savefig("C:/Users/j.rode/Desktop/Markowitz/plot/plot.svg")

    def plotAllocation(self):
        myMin = self.portfolio.returnMin
        myMax = self.portfolio.returnMax

        xMin = self.portfolio.allocationMin
        xMax = self.portfolio.allocationMax

        labels = self.portfolio.symbols

        fig, ax1 = plt.subplots(figsize=(15, 10))
        # ax2 = ax1.twinx()

        for i, (xStart, xEnde) in enumerate(zip(xMin, xMax), 0):
            ax1.plot([myMin, myMax], [xStart, xEnde], label=labels[i])

        ax1.set_xlabel("minimum return")
        ax1.set_ylabel("allocation")

        ax1.set_xlim(myMin, myMax)
        ax1.set_ylim(min(xMin + xMax) - 0.1, max(xMin + xMax) + 0.1)

        ax1.grid(linewidth=0.25)
        ax1.legend(loc="best")

        plt.xticks(rotation=45)
        plt.show()

        #fig.savefig("C:/Users/j.rode/Desktop/Markowitz/plot/plotAllocation.svg")