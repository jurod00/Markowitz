skript = "AuxiliaryQuantities.py"

import datetime as dt

from iO import Input

from plot import PlotPortfolio

from portfolio import PortfolioShares

from simulation import GeometricBrownianMotion as Gbm

from util import Time
from util import AuxiliaryQuantities as Aq

# iO
if skript == "Input.py":
    input = Input()
    # input.downloadShare("ADS.DE", dt.datetime(2025,12,1), dt.datetime(2025,12,10))

    # print(input.getData())  # .index.tolist() und tolist()

    # Plt = PlotStock(input.getTime(), input.getStock())
    # Plt.plot()

    input.downloadShares(["ADS.DE", "AMZN", "MCD"], dt.datetime(2025,11,28), dt.datetime(2025,12,23))

    print(input.getStocks())

    time = input.getTime()

    portfolio = PortfolioShares(time, ["ADS.DE", "AMZN", "MCD"])
    portfolio.downloadPortfolio()

    print(portfolio.getStocks())
    print(portfolio.time)

    plotPortfolio = PlotPortfolio(portfolio)
    plotPortfolio.plot("abs")
# plot
elif skript == "PlotPortfolio.py":
    # time = Time(dt.datetime(2025,12,1), dt.datetime(2025,12,29))
    # symbols = ["A", "B", "C", "D", "E"]

    # portfolio = PortfolioShares(time.getTime(), symbols)

    # s0 = [100,100,100,100,100]
    # drift = [0.1,0.1,0.1,0.1,0.1]
    # volatility = [0.1,0.1,0.1,0.1,0.1]

    # portfolio.simulatePortfolio(s0, drift, volatility)

    # plt = PlotPortfolio(portfolio)
    # plt.plotStocks("abs")

    # plt.plotAllocation()

    portfolio = PortfolioShares()
    portfolio.databasePortfolio()
    portfolio.calculateAllocationBasic()
    
    plt = PlotPortfolio(portfolio)
    plt.plotStocks("rel")
    plt.plotAllocation()
# portfolio
elif skript == "PortfolioShares.py":
    time = [dt.datetime(2025, 12, 17), dt.datetime(2025, 12, 18), dt.datetime(2025, 12, 19)]
    symbols = ["A", "B", "C", "D", "E"]

    portfolio = PortfolioShares(time, symbols)

    s0 = [100,100,100,100,100]
    drift = [0.1,0.1,0.1,0.1,0.1]
    volatility = [0.1,0.1,0.1,0.1,0.1]

    portfolio.simulatePortfolio(s0, drift, volatility)
    print(portfolio.getStocks())
# simulation
elif skript == "GeometricBrownianMotion.py":
    s0 = 100
    time = [dt.datetime(2025, 12, 17), dt.datetime(2025, 12, 18), dt.datetime(2025, 12, 19)]
    drift = 0.1
    volatility = 0.1

    gbm = Gbm(time)
    gbm.setS0(s0)
    gbm.setDrift(drift)
    gbm.setVolatility(volatility)
    gbm.simulate()
    print(gbm.getStock())
# util
elif skript == "Time.py":
    time = Time(dt.datetime(2025, 12, 17), dt.datetime(2025, 12, 19))
    print(time.getTime())
# util
elif skript == "AuxiliaryQuantities.py":
    aq = Aq()
    
    portfolio = PortfolioShares()
    portfolio.databasePortfolio()

    time = portfolio.time
    stocks = portfolio.stocks

    print(aq.duration(time))
    print(aq.numberTimestamps(time))
    print(aq.numberStocks(stocks))
    print(aq.prob(time))

    print(aq.annualizedReturn(time, stocks))
    print(aq.expectedReturn(time, stocks))
    print(aq.expectedReturnPercent(time, stocks))
    print(aq.covariance(time, stocks))
    print(aq.precision(time, stocks))
    print(aq.allocationBasic(time, stocks, 0.07))
    print(aq.allocationBasic(time, stocks, 0.07, "%"))
# default
else:
    print("Skript nicht gefunden!")