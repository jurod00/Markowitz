from portfolio.portfolio import Portfolio
from plot.plotAllocation import PlotAllocation

def main():
    portfolio = Portfolio()
    portfolio.setStockDataFromCSV()
    portfolio.setStocks(portfolio.stocks[1:])
    portfolio.setSymbols(portfolio.symbols[1:])
    symbolOptions = ["GOOGL Call", "GOOGL Put", "AAPL Call", "AAPL Put", "AMD Call", "AMD Put", "INTC Call", "INTC Put", "NVDA Call", "NVDA Put"]
    symbolOptions = ["AAPL Call", "AAPL Put", "AMD Call", "AMD Put", "INTC Call", "INTC Put", "NVDA Call", "NVDA Put"]
    # rand.shuffle(symbolOptions)
    # print(symbolOptions)
    # portfolio.setOptionDataFromCSV(symbolsOptions=symbolOptions)

    # print(portfolio.times)
    # print(portfolio.stocks)
    # print(portfolio.symbols)

    # print(portfolio.riskFreeRate)

    # print(portfolio.premiumCall)
    # print(portfolio.strikesCall)
    # print(portfolio.implVolCall)
    # print(portfolio.indicesCall)
    # print(portfolio.symbolsCall)

    # print(portfolio.premiumPut)
    # print(portfolio.strikesPut)
    # print(portfolio.implVolPut)
    # print(portfolio.indicesPut)
    # print(portfolio.symbolsPut)

    plotPortfolio = PlotAllocation(portfolio=portfolio)
    # plotPortfolio.plotStocks()
    plotPortfolio.plotAllocationMarkowitz()
    # plotPortfolio.plotAllocationUtilityMaximization()
    # plotPortfolio.plotAllocationIntegratedRiskManagement(returnMax=2.5, beta=1)
    # plotPortfolio.plotStackedBar(minimumReturn=0.1)
    # plotPortfolio.plotCovarianceMatrix()
    # plotPortfolio.plotCorrelationMatrix()
    # plotPortfolio.plotCorrelation("callPut")

if __name__ == "__main__":
    main()