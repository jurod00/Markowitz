import numpy as np
import databento as db

from portfolio.portfolioShares import PortfolioShares
from plot.plotPortfolioShares import PlotPortfolioShares

def main():
    portfolioShares = PortfolioShares()
    portfolioShares.databasePortfolio()

    plotPortfolioShares = PlotPortfolioShares(portfolioShares)
    plotPortfolioShares.plotStocks("rel")
    plotPortfolioShares.plotAllocationMarkowitz()
    plotPortfolioShares.plotAllocationLinearProgramming()



if __name__ == "__main__":
    main()