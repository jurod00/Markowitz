# Python-Skript welches getestet werden soll
skript = "ReadDataBase.py"

import datetime as dt

from iO import Input
from iO.database import ReadDatabase

from simulation import GeometricBrownianMotion as Gbm
from util import Time
from util import AuxiliaryQuantities as Aq
from portfolio import PortfolioShares

from plot import PlotStock
from plot import PlotPortfolio

# Ordner iO
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
    plotPortfolio.plot()

elif skript == "ReadDataBase.py":
    readDatabase = ReadDatabase()
    data = readDatabase.getData()
    print(data)

    time = readDatabase.getTime()
    stocks = readDatabase.getStocks()
    symbols = readDatabase.getSymbols()
    
    portfolioShares = PortfolioShares(time, symbols)
    portfolioShares.setStocks(stocks)

    plotPortfolio = PlotPortfolio(portfolioShares)
    plotPortfolio.plot("rel")

elif skript == "GeometricBrownianMotion.py":

    s0 = 100
    time = [dt.datetime(2025, 12, 17), dt.datetime(2025, 12, 18), dt.datetime(2025, 12, 19)]
    drift = 0.1
    volatility = 0.1

    gbm = Gbm(s0, time, drift, volatility)
    gbm.simulate()
    print(gbm.getStock())

elif skript == "Time.py":
    time = Time(dt.datetime(2025, 12, 17), dt.datetime(2025, 12, 19))
    print(time.getTime())

elif skript == "AuxiliaryQuantities.py":
    time = [dt.datetime(2025, 12, 17), dt.datetime(2025, 12, 18), dt.datetime(2025, 12, 19)]

    aq = Aq()
    print(aq.duration(time))
    print(aq.n(time))
    print(aq.p(time))

elif skript == "PortfolioShares.py":
    time = [dt.datetime(2025, 12, 17), dt.datetime(2025, 12, 18), dt.datetime(2025, 12, 19)]
    symbols = ["A", "B", "C", "D", "E"]

    portfolio = PortfolioShares(time, symbols)

    s0 = [100,100,100,100,100]
    drift = [0.1,0.1,0.1,0.1,0.1]
    volatility = [0.1,0.1,0.1,0.1,0.1]

    portfolio.simulatePortfolio(s0, drift, volatility)
    print(portfolio.getStocks())

elif skript == "PlotPortfolio.py":
    time = Time(dt.datetime(2025,12,1), dt.datetime(2025,12,29))
    symbols = ["A", "B", "C", "D", "E"]

    portfolio = PortfolioShares(time.getTime(), symbols)

    s0 = [100,100,100,100,100]
    drift = [0.1,0.1,0.1,0.1,0.1]
    volatility = [0.1,0.1,0.1,0.1,0.1]

    portfolio.simulatePortfolio(s0, drift, volatility)

    plt = PlotPortfolio(portfolio)
    plt.plot()

else:
    print("Skript nicht gefunden!")