analysis = "LinearProgrammingMeanVariancePlot"

from portfolio.portfolioShares import PortfolioShares
from mathematics.financialMathematics import FinancialMathematics as FiMa
from analysis.sensitivityAnalysis import SensitivityAnalysis as SeAn
from plot.plotSensitivityAnalysis import PlotSensitivityAnalysis
from plot.plotPortfolioShares import PlotPortfolioShares

def main():

    portfolio = PortfolioShares()
    portfolio.databasePortfolio()

    if analysis == "MarkowitzAllocation":
        plot = PlotPortfolioShares(portfolio)
        plot.plotStocks("rel")
        plot.plotAllocationMarkowitz()

    elif analysis == "MarkowitzSensitivityElasticityMy":
        plot = PlotSensitivityAnalysis("Markowitz", portfolio)
        plot.plotSensitivityElasticityMarkowitz()

    elif analysis == "MarkowitzMeanVariancePlot":
        plot = PlotSensitivityAnalysis("Markowitz", portfolio)
        plot.plotMeanVariance(0.005)

    elif analysis == "UtilityMaximizationAllocation":
        plot = PlotPortfolioShares(portfolio)
        plot.plotStocks("rel")
        plot.plotAllocationUtilityMaximization()

    elif analysis == "UtilityMaximizationSensitivityElasticityKappa":
        plot = PlotSensitivityAnalysis("UtilityMaximization", portfolio)
        plot.plotSensitivityElasticityUtilityMaximization()

    elif analysis == "UtilityMaximizationMeanVariancePlot":
        plot = PlotSensitivityAnalysis("UtilityMaximization", portfolio)
        plot.plotMeanVariance(0.005)

    elif analysis == "LinearProgrammingAllocation":
        plot = PlotPortfolioShares(portfolio)
        plot.plotAllocationLinearProgramming()

    elif analysis == "LinearProgrammingSensitivityElasticityMy":
        plot = PlotSensitivityAnalysis("LinearProgramming", portfolio)
        plot.plotSensitivityElasticityLinearProgrammingMy()

    elif analysis == "LinearProgrammingSensitivityElasticityAlpha":
        plot = PlotSensitivityAnalysis("LinearProgramming", portfolio)
        plot.plotSensitivityElasticityLinearProgrammingAlpha()

    elif analysis == "LinearProgrammingSensitivityElasticityGamma":
        plot = PlotSensitivityAnalysis("LinearProgramming", portfolio)
        plot.plotSensitivityElasticityLinearProgrammingGamma()

    elif analysis == "LinearProgrammingMeanVariancePlot":
        plot = PlotSensitivityAnalysis("LinearProgramming", portfolio)
        plot.plotMeanRiskmeasure(0.005)
    else:
        print("Analysis not available.")

if __name__ == "__main__":
    main()