from portfolio.portfolio import Portfolio
from plot.plotPortfolio import PlotPortfolio

import numpy as np

def main():
    portfolio = Portfolio()
    portfolio.setSymbols(["AAPL", "MSFT", "GOOGL"])
    plotPortfolio = PlotPortfolio(portfolio=portfolio)
    plotPortfolio.plotStackedBar(allocation=np.array([0.5, 0.3, 0.2]))


if __name__ == "__main__":
    main()