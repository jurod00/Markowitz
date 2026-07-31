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
    plotStocks.plotStocksAbs()
    plotStocks.plotStocksRel()

    plotAllocation = PlotAllocation(portfolio=portfolio)
    # plotAllocation.plotAllocationMarkowitz(returnMin=0.05)
    # plotAllocation.plotAllocationMarkowitzNoShortSelling()#returnMax=2.5)
    # plotAllocation.plotAllocationUtilityMaximization()
    # plotAllocation.plotAllocationUtilityMaximizationNoShortSelling()
    plotAllocation.plotAllocationIntegratedRiskManagement(returnMax=2.5)
    # plotAllocation.plotStackedBar(np.array([0.5, 0.2, 0.18, 0.12]))

    # plotMeanRisk = PlotMeanRisk(portfolio=portfolio)
    # plotMeanRisk.plotMeanVarianceMarkowitz(returnMax=0.01)
    # plotMeanRisk.plotMeanVarianceUtilityMaximization(riskAversionMin=20)
    # plotMeanRisk.plotMeanAVaR(returnMax=2.0)

    # plotMatrix = PlotMatrix(portfolio=portfolio)
    # plotMatrix.plotCovarianceMatrix()
    # plotMatrix.plotCorrelationMatrix()

    # plotCorrelation = PlotCorrelation(portfolio=portfolio)
    # plotCorrelation.plotCorrelationStockCall()
    # plotCorrelation.plotCorrelationStockPut()
    # plotCorrelation.plotCorrelationCallPut()

    # plotDistribution = PlotDistribution(portfolio=portfolio)
    # plotDistribution.plotMarginalDistribution()

if __name__ == "__main__":
    main()