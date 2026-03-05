from portfolio import PortfolioShares
from analysis import SensitivityAnalysis
from plot import PlotSensitivityAnalysis

def main():
    # 0.005, 0.01, 0.015, 0.02
    # 0.5%, 1.0%, 1.5%, 2.0%
    eps = 0

    portfolio = PortfolioShares()
    portfolio.databasePortfolio()

    sensitivityAnalysis = SensitivityAnalysis()
    allocations = sensitivityAnalysis.allocationsNoisy(portfolio, eps, "markowitz")

    plot = PlotSensitivityAnalysis()
    # plot.plotMeanVariance(portfolio, allocations)

    # allocations = sensitivityAnalysis.allocationsNoisy(portfolio, eps, "utilityMaximization")
    # plot.plotMeanVariance(portfolio, allocations)

    allocations = sensitivityAnalysis.allocationsNoisy(portfolio, eps, "linearProgramming")
    plot.plotMeanVariance(portfolio, allocations)

if __name__ == "__main__":
    main()