from portfolio.portfolio import Portfolio
from plot.plotAllocation import PlotAllocation
from plot.plotCorrelation import PlotCorrelation
from plot.plotDistribution import PlotDistribution
from plot.plotMeanRisk import PlotMeanRisk
from plot.plotStocks import PlotStocks
from plot.plotMatrix import PlotMatrix

import numpy as np

def main():
    portfolio = Portfolio()
    portfolio.setStockDataFromCSV(fileName="master.csv")
    portfolio.setStocks(portfolio.stocks[1:])
    portfolio.setSymbols(portfolio.symbols[1:])
    # symbolOptions = ["GOOGL Call", "GOOGL Put", "AAPL Call", "AAPL Put", "AMD Call", "AMD Put", "INTC Call", "INTC Put", "NVDA Call", "NVDA Put"]
    symbolOptions = ["AAPL Call", "AAPL Put", "AMD Call", "AMD Put", "INTC Call", "INTC Put", "NVDA Call", "NVDA Put"]
    # rand.shuffle(symbolOptions)
    # print(symbolOptions)
    portfolio.setOptionDataFromCSV(symbolsOptions=symbolOptions)

    plotStocks = PlotStocks(portfolio=portfolio)
    # plotStocks.plotStocksAbs(format="png")
    plotStocks.plotStocksRel(format="png")

    plotAllocation = PlotAllocation(portfolio=portfolio)
    plotAllocation.plotAllocationMarkowitz(format="png")
    plotAllocation.plotAllocationMarkowitzNoShortSelling(format="png")
    # plotAllocation.plotAllocationUtilityMaximization(format="png")
    # plotAllocation.plotAllocationIntegratedRiskManagement(returnMax=2.5, format="png")
    # plotAllocation.plotStackedBar(np.array([0.5, 0.2, 0.18, 0.12]), format="png")

    plotMeanRisk = PlotMeanRisk(portfolio=portfolio)
    # plotMeanRisk.plotMeanVarianceMarkowitz(returnMax=0.01, format="png")
    # plotMeanRisk.plotMeanVarianceUtilityMaximization(riskAversionMin=20, format="png")
    # plotMeanRisk.plotMeanAVaR(returnMax=2.0, format="png")

    # plotMatrix = PlotMatrix(portfolio=portfolio)
    # plotMatrix.plotCovarianceMatrix(format="png")
    # plotMatrix.plotCorrelationMatrix(format="png")

    # plotCorrelation = PlotCorrelation(portfolio=portfolio)
    # plotCorrelation.plotCorrelationStockCall(format="png")
    # plotCorrelation.plotCorrelationStockPut(format="png")
    # plotCorrelation.plotCorrelationCallPut(format="png")

    # plotDistribution = PlotDistribution(portfolio=portfolio)
    # plotDistribution.plotMarginalDistribution(format="png")

if __name__ == "__main__":
    main()