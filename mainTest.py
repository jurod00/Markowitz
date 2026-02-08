skript = "AuxiliaryQuantities.py"

import numpy as np
import datetime as dt

from iO import Input

from plot import PlotPortfolioShares

from portfolio import PortfolioShares

from simulation import GeometricBrownianMotion as Gbm

from util import Time
from util import AuxiliaryQuantities as Aq

# iO
if skript == "Input.py":
    input = Input()

    symbols = ["ADS.DE", "AMZN", "MCD"]

    input.downloadShares(symbols, dt.datetime(2025,11,28), dt.datetime(2025,12,23))

    print(input.getStocks())

    time = input.getTime()
    stocks = input.getStocks()

    portfolio = PortfolioShares()
    portfolio.setTime(time)
    portfolio.setStocks(stocks)
    portfolio.setSymbols(symbols)

    plt = PlotPortfolioShares(portfolio)
    plt.plotStocks("rel")
# plot
elif skript == "PlotPortfolioShares.py":
    portfolio = PortfolioShares()
    portfolio.databasePortfolio()
    # portfolio.addRiskFreeAsset()
    portfolio.calculateAllocationBasic()

    # portfolio.calculateAllocationUtilityMaximization([i for i in range(1, 50)])
    
    plt = PlotPortfolioShares(portfolio)
    plt.plotStocks("rel")
    # plt.plotAllocation()
    plt.plotMeanVariance(sigmaStart=0, sigmaEnde=0.3, allocation=np.array([0.05, 0.05, 0.05, 0.05, 0.8]), riskFreeRate=0.0)
    # plt.plotAllocationUtilityMaximization()

    # Neues simuliertes Portfolio
    # s0 = [100.0, 100.0, 100.0]
    # drift = [0.1, 0.1, 0.1]
    # volatility = [0.1, 0.1, 0.1]

    # time = Time(dt.datetime(2026, 1, 1), dt.datetime(2026, 2, 1))

    # portfolioNew = PortfolioShares()
    # portfolioNew.setSymbols(["a", "b", "c"])
    # portfolioNew.setTime(time.getTime())
    # portfolioNew.simulatePortfolio(s0, drift, volatility)
    # portfolioNew.calculateAllocationBasic()

    # pltNew = PlotPortfolioShares(portfolioNew)
    # pltNew.plotStocks("abs")
    # pltNew.plotAllocation()
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

    np.set_printoptions(formatter={'float': lambda x: "{0:0.4f}".format(x)}, linewidth=200)
    print(aq.constraintsLeftHandSide(time, stocks))
    print(aq.constraintsRightHandSide(0.25, time))
    print(aq.constraintsBounds(time, stocks))
    print("p = " + str(aq.prob(time)))
    print(aq.objectiveCostVector(time, stocks, 0, 1))
# default
else:
    print("Skript nicht gefunden!")