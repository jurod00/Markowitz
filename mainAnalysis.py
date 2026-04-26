analysis = "LinearProgrammingAllocation"

from portfolio.portfolioShares import PortfolioShares
from mathematics.financialMathematics import FinancialMathematics as FiMa
from analysis.sensitivityAnalysis import SensitivityAnalysis
from plot.plotSensitivityAnalysis import PlotSensitivityAnalysis
from plot.plotPortfolioShares import PlotPortfolioShares

def main():

    portfolio = PortfolioShares()
    portfolio.databasePortfolio()

    sensitivityAnalysis = SensitivityAnalysis()

    if analysis == "MarkowitzAllocation":
        plot = PlotPortfolioShares(portfolio)
        plot.plotStocks("rel")
        plot.plotAllocationMarkowitz()

    elif analysis == "MarkowitzSensitivityElasticityMy":
        plot = PlotSensitivityAnalysis(portfolio, sensitivityAnalysis)
        plot.plotSensitivityElasticityMarkowitz()

    elif analysis == "MarkowitzMeanVariancePlot":
        plot = PlotSensitivityAnalysis("Markowitz", portfolio, sensitivityAnalysis)
        plot.plotMeanVariance(0.02)

    elif analysis == "UtilityMaximizationAllocation":
        plot = PlotPortfolioShares(portfolio)
        plot.plotStocks("rel")
        plot.plotAllocationUtilityMaximization()

    elif analysis == "UtilityMaximizationSensitivityElasticityKappa":
        plot = PlotSensitivityAnalysis("UtilityMaximization", portfolio, sensitivityAnalysis)
        plot.plotSensitivityElasticityUtilityMaximization()

    elif analysis == "UtilityMaximizationMeanVariancePlot":
        plot = PlotSensitivityAnalysis("UtilityMaximization", portfolio, sensitivityAnalysis)
        plot.plotMeanVariance(0.005)

    elif analysis == "LinearProgrammingAllocation":
        plot = PlotPortfolioShares(portfolio)
        plot.plotAllocationLinearProgramming()

    elif analysis == "LinearProgrammingSensitivityElasticityMy":
        plot = PlotSensitivityAnalysis("LinearProgramming", portfolio, sensitivityAnalysis)
        plot.plotSensitivityElasticityLinearProgrammingMy()

    elif analysis == "LinearProgrammingSensitivityElasticityAlpha":
        plot = PlotSensitivityAnalysis("LinearProgramming", portfolio, sensitivityAnalysis)
        plot.plotSensitivityElasticityLinearProgrammingAlpha()

    elif analysis == "LinearProgrammingSensitivityElasticityGamma":
        plot = PlotSensitivityAnalysis("LinearProgramming", portfolio, sensitivityAnalysis)
        plot.plotSensitivityElasticityLinearProgrammingGamma()

    elif analysis == "LinearProgrammingMeanVariancePlot":
        plot = PlotSensitivityAnalysis("LinearProgramming", portfolio, sensitivityAnalysis)
        plot.plotMeanRiskmeasure(0.02)
    else:
        print("Analysis not available.")
    # 0.005, 0.01, 0.015, 0.02
    # 0.5%, 1.0%, 1.5%, 2.0%
    # eps = 0.005

    # portfolio = PortfolioShares()
    # portfolio.databasePortfolio()

    # sensitivityAnalysis = SensitivityAnalysis()
    # allocations = sensitivityAnalysis.allocationsNoisy(portfolio, eps, "markowitz")

    # plot = PlotSensitivityAnalysis()
    # # plot.plotMeanVariance(portfolio, allocations)

    # # allocations = sensitivityAnalysis.allocationsNoisy(portfolio, eps, "utilityMaximization")
    # # plot.plotMeanVariance(portfolio, allocations)

    # # allocations = sensitivityAnalysis.allocationsNoisy(portfolio, eps, "linearProgramming")
    # # plot.plotMeanVariance(portfolio, allocations)

    # plot.plotMeanRiskmeasure(portfolio, eps)

    # # print(sensitivityAnalysis.sensitivity(portfolio, "markowitz"))

    # plt = PlotPortfolioShares(portfolio)
    # # plt.plotStocks("rel")

    # # portfolio.calculateAllocationBasic()
    # # plt.plotAllocation()

    # # plot.plotSensitivityElasticityUtilityMaximization(portfolio)
    # # plot.plotElasticityUtilityMaximization(portfolio)

    # # plt.plotAllocationLinearProgramming()

    # # plot.plotSensitivityElasticityMarkowitz(portfolio)
    # # plot.plotSensitivityElasticityLinearProgramming(portfolio)

if __name__ == "__main__":
    main()