from portfolio.portfolio import Portfolio
from plot.plotAllocation import PlotAllocation
from plot.plotCorrelation import PlotCorrelation
from plot.plotDistribution import PlotDistribution
from plot.plotMeanRisk import PlotMeanRisk
from plot.plotStocks import PlotStocks
from plot.plotMatrix import PlotMatrix
from plot.plotSensitivityLocal import PlotSensitivityLocal

from mathematics.minimization import Minimization

import numpy as np

def main():
    fileName = "master.csv"

    if fileName == "lecture.csv":
        portfolio = Portfolio()
        portfolio.setStockDataFromCSV(fileName=fileName)
        
        plotStocks = PlotStocks(portfolio=portfolio)
        plotStocks.plotStocksAbs()
        plotStocks.plotStocksRel()

        plotAllocation = PlotAllocation(portfolio=portfolio)
        plotAllocation.plotAllocationMarkowitz(shortSellingAllowed=True, method="twoFund")
        plotAllocation.plotAllocationIntegratedRiskManagement(returnMax=0.25, beta=0.1)

        # plotMeanRisk = PlotMeanRisk(portfolio=portfolio)
        # plotMeanRisk.plotMeanVarianceMarkowitz(returnMax=0.5)
        # plotMeanRisk.plotMeanAVaR(returnMax=0.5)

        # plotMatrix = PlotMatrix(portfolio=portfolio)
        # plotMatrix.plotCovarianceMatrix()
        # plotMatrix.plotCorrelationMatrix()

        plotSensitivityLocal = PlotSensitivityLocal(portfolio=portfolio)
        # plotSensitivityLocal.plotSensitivityMinimumReturnMARKOWITZ(method="twoFund")
        # plotSensitivityLocal.plotSensitivityMinimumReturnIRM(returnMax=0.5)
        plotSensitivityLocal.plotSensitivityAlphaIRM()
        plotSensitivityLocal.plotSensitivityBetaIRM()

    elif fileName == "master.csv":
        portfolio = Portfolio()
        portfolio.setStockDataFromCSV(fileName=fileName)
        portfolio.setStocks(portfolio.stocks[1:])
        portfolio.setSymbols(portfolio.symbols[1:])
        symbolOptions = ["AAPL Call", "AAPL Put", "AMD Call", "AMD Put", "INTC Call", "INTC Put", "NVDA Call", "NVDA Put"]
        # rand.shuffle(symbolOptions)
        portfolio.setOptionDataFromCSV(symbolsOptions=symbolOptions)

        # plotStocks = PlotStocks(portfolio=portfolio)
        # plotStocks.plotStocksAbs()
        # plotStocks.plotStocksRel()

        plotAllocation = PlotAllocation(portfolio=portfolio)
        plotAllocation.plotAllocationMarkowitz(method="twoFund")
        plotAllocation.plotAllocationMarkowitz(shortSellingAllowed=False, method="interiorPoint")
        # plotAllocation.plotAllocationIntegratedRiskManagement(returnMax=0.5, beta=1)

        # plotMeanRisk = PlotMeanRisk(portfolio=portfolio)
        # plotMeanRisk.plotMeanVarianceMarkowitz(returnMax=0.01)
        # plotMeanRisk.plotMeanAVaR(returnMax=2.0)

        # plotMatrix = PlotMatrix(portfolio=portfolio)
        # plotMatrix.plotCovarianceMatrix()
        # plotMatrix.plotCorrelationMatrix()

        # plotCorrelation = PlotCorrelation(portfolio=portfolio)
        # plotCorrelation.plotCorrelationStockCall()
        # plotCorrelation.plotCorrelationStockPut()
        # plotCorrelation.plotCorrelationCallPut()

        plotSensitivityLocal = PlotSensitivityLocal(portfolio=portfolio)
        # plotSensitivityLocal.plotSensitivityMinimumReturnMARKOWITZ(method="twoFund")
        # plotSensitivityLocal.plotSensitivityStockMARKOWITZ(method="twoFund")
        # plotSensitivityLocal.plotSensitivityMinimumReturnIRM(returnMax=0.5)
        # plotSensitivityLocal.plotSensitivityAlphaIRM()
        # plotSensitivityLocal.plotSensitivityBetaIRM()

if __name__ == "__main__":
    main()