from portfolio import PortfolioShares
from portfolio import FinancialMathematics as FiMa
from analysis import SensitivityAnalysis
from plot import PlotSensitivityAnalysis
from plot import PlotPortfolioShares

def main():
    # 0.005, 0.01, 0.015, 0.02
    # 0.5%, 1.0%, 1.5%, 2.0%
    eps = 0.005

    portfolio = PortfolioShares()
    portfolio.databasePortfolio()

    sensitivityAnalysis = SensitivityAnalysis()
    allocations = sensitivityAnalysis.allocationsNoisy(portfolio, eps, "markowitz")

    plot = PlotSensitivityAnalysis()
    # plot.plotMeanVariance(portfolio, allocations)

    # allocations = sensitivityAnalysis.allocationsNoisy(portfolio, eps, "utilityMaximization")
    # plot.plotMeanVariance(portfolio, allocations)

    # allocations = sensitivityAnalysis.allocationsNoisy(portfolio, eps, "linearProgramming")
    # plot.plotMeanVariance(portfolio, allocations)

    plot.plotMeanRiskmeasure(portfolio, eps)

    # print(sensitivityAnalysis.sensitivity(portfolio, "markowitz"))

    plt = PlotPortfolioShares(portfolio)
    # plt.plotStocks("rel")

    # portfolio.calculateAllocationBasic()
    # plt.plotAllocation()

    # plot.plotSensitivityElasticityUtilityMaximization(portfolio)
    # plot.plotElasticityUtilityMaximization(portfolio)

    # plt.plotAllocationLinearProgramming()

    # plot.plotSensitivityElasticityMarkowitz(portfolio)
    # plot.plotSensitivityElasticityLinearProgramming(portfolio)

if __name__ == "__main__":
    main()