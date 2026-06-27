stockPrice = 33.50
strikePrice = 35.00
volatility = 0.5
riskFreeRate = 0.024

import numpy as np

from mathematics.financialMathematics import FinancialMathematics as FiMa
from portfolio.portfolioShares import PortfolioShares
from portfolio.portfolioSharesOptions import PortfolioSharesOptions

from plot.plotPortfolioShares import PlotPortfolioShares
from plot.plotPortfolioSharesOptions import PlotPortfolioSharesOptions

import datetime as dt
import matplotlib.pyplot as plt
# plt.rcParams.update({'font.size': 20})
# plt.style.use("dark_background")

import pandas_datareader as pdr

def main():
    pass

def mainGreeks():
    stockPrice = 306.31
    strikePrice = 300.00
    daysToMaturity = 17
    volatility = 0.2571
    riskFreeRate = 0.0445

    print("Price " + str(FiMa.priceOption(daysToMaturity=daysToMaturity, stockPrice=stockPrice, strikePrice=strikePrice, volatility=volatility, riskFreeRate=riskFreeRate)))
    print("Delta " + str(FiMa.delta(daysToMaturity=daysToMaturity, stockPrice=stockPrice, strikePrice=strikePrice, volatility=volatility, riskFreeRate=riskFreeRate)))
    print("Gamma " + str(FiMa.gamma(daysToMaturity=daysToMaturity, stockPrice=stockPrice, strikePrice=strikePrice, volatility=volatility, riskFreeRate=riskFreeRate)))
    print("Theta " + str(FiMa.theta(daysToMaturity=daysToMaturity, stockPrice=stockPrice, strikePrice=strikePrice, volatility=volatility, riskFreeRate=riskFreeRate)))
    print("Vega " + str(FiMa.vega(daysToMaturity=daysToMaturity, stockPrice=stockPrice, strikePrice=strikePrice, volatility=volatility, riskFreeRate=riskFreeRate)))
    print("Rho " + str(FiMa.rho(daysToMaturity=daysToMaturity, stockPrice=stockPrice, strikePrice=strikePrice, volatility=volatility, riskFreeRate=riskFreeRate)))

def mainHistoricalVolatility():
    times = [dt.datetime(year=2026, month=1, day=1) + dt.timedelta(days=d) for d in range(365)]

    S0 = 100

    my = -5
    sigma = 0.3

    tests = [i for i in range(100)]
    sigmas = []

    for _ in tests:
        stock = []
        
        for time in times:
            t = (time - times[0]) / (times[-1] - times[0])
            stock.append(S0*np.exp((my-0.5*sigma**2)*t + sigma*np.random.normal(0, t)))

        sigmas.append(FiMa.historicalVolatility(times, stock))

    fig, ax = plt.subplots()
    ax.plot(tests, sigmas)
    ax.plot(tests, [sigma]*100)
    ax.set_ylim(0, 1)
    plt.show()

def mainImpliedVolatility():
    _, optionPrice = FiMa.priceOption(daysToMaturity=17, stockPrice=306.31, strikePrice=300.00, volatility=0.2570, riskFreeRate=0.0445)
    print(optionPrice)

    sigma = FiMa.impliedVolatility(daysToMaturity=17, stockPrice=306.31, strikePrice=300.00, optionPrice=optionPrice, riskFreeRate=0.0445)
    print(sigma)

def mainTest1():
    times = [dt.datetime(year=2026, month=6, day=1) + dt.timedelta(days=d) for d in range(17)]

    S0 = 306.31
    K0 = 320.00

    my0 = 0.25
    sigma0 = 0.25
    implVola0 = 0.2456

    stock0 = [S0]
    
    for i, time in enumerate(times):
        t = (time - times[0]) / (times[-1] - times[0])

        np.random.seed(i)
        if i == len(times) - 1:
            break
        stock0.append(stock0[-1] + my0 + (1 if np.random.random() < 0.5 else -1)*sigma0*np.random.normal(0, 1))
    
    options = {
        "riskFreeRate" : 0.0445,

        "callPrices" : [2.09],
        "callIndices" : [0],
        "callStrikes" : [K0],
        "callVolatilities" : [implVola0],

        "putPrices" : [],
        "putIndices" : [],
        "putStrikes" : [],
        "putVolatilities" : []
        
    }

    portfolioSharesOptions = PortfolioSharesOptions()
    portfolioSharesOptions.setTime(times)
    portfolioSharesOptions.setStocks([stock0])
    portfolioSharesOptions.setSymbols(["Stock (steigend)"])
    portfolioSharesOptions.setOptions(options)

    plotPortfolioSharesOptions = PlotPortfolioSharesOptions(portfolioSharesOptions)
    plotPortfolioSharesOptions.plotStocks("abs")
    plotPortfolioSharesOptions.plotAllocationMarkowitz(returnMax=1)
    plotPortfolioSharesOptions.plotAllocationLinearProgramming(returnMax=1, gamma=1)

def mainTest2():
    times = [dt.datetime(year=2026, month=6, day=1) + dt.timedelta(days=d) for d in range(17)]

    S0 = 306.31
    K0 = 300.00

    my0 = -0.25

    sigma0 = 0.5

    implVola0 = 0.2571

    stock0 = [S0]
    
    for i, time in enumerate(times):
        t = (time - times[0]) / (times[-1] - times[0])

        np.random.seed(i)
        if i == len(times) - 1:
            break
        stock0.append(stock0[-1] + my0 + (1 if np.random.random() < 0.5 else -1)*sigma0*np.random.normal(0, 1))
    
    options = {
        "riskFreeRate" : 0.0445,

        "callPrices" : [],
        "callIndices" : [],
        "callStrikes" : [],
        "callVolatilities" : [],

        "putPrices" : [3.73],
        "putIndices" : [0],
        "putStrikes" : [K0],
        "putVolatilities" : [implVola0]
    }

    portfolioSharesOptions = PortfolioSharesOptions()
    portfolioSharesOptions.setTime(times)
    portfolioSharesOptions.setStocks([stock0])
    portfolioSharesOptions.setSymbols(["Stock (fallend)"])
    portfolioSharesOptions.setOptions(options)

    plotPortfolioSharesOptions = PlotPortfolioSharesOptions(portfolioSharesOptions)
    plotPortfolioSharesOptions.plotStocks("abs")
    plotPortfolioSharesOptions.plotAllocationMarkowitz(returnMax=1)
    plotPortfolioSharesOptions.plotAllocationLinearProgramming(returnMax=1, gamma=1)

def mainTest3():
    times = [dt.datetime(year=2026, month=6, day=1) + dt.timedelta(days=d) for d in range(17)]

    S0 = 306.31
    K0 = 300.00

    S1 = 376.37
    K1 = 350.00

    S2 = 224.36
    K2 = 220.00

    my0 = -0.05
    my1 = -0.05
    my2 = -0.05

    sigma0 = 0.5
    sigma1 = 0.5
    sigma2 = 0.5

    implVola0 = 0.2571
    implVola1 = 0.2696
    implVola2 = 0.4280

    stock0 = [S0]
    stock1 = [S1]
    stock2 = [S2]
    
    for i, time in enumerate(times):
        t = (time - times[0]) / (times[-1] - times[0])

        np.random.seed(i)
        if i == len(times) - 1:
            break
        stock0.append(stock0[-1] + my0 + (1 if np.random.random() < 0.5 else -1)*sigma0*np.random.normal(0, 1))
        stock1.append(stock1[-1] + my1 + (1 if np.random.random() < 0.5 else -1)*sigma1*np.random.normal(0, 1))
        stock2.append(stock2[-1] + my2 + (1 if np.random.random() < 0.5 else -1)*sigma2*np.random.normal(0, 1))
    
    options = {
        "riskFreeRate" : 0.0445,

        "callPrices" : [],
        "callIndices" : [],
        "callStrikes" : [],
        "callVolatilities" : [],

        "putPrices" : [3.73, 1.86, 6.05],
        "putIndices" : [0, 1, 2],
        "putStrikes" : [K0, K1, K2],
        "putVolatilities" : [implVola0, implVola1, implVola2]
    }

    portfolioSharesOptions = PortfolioSharesOptions()
    portfolioSharesOptions.setTime(times)
    portfolioSharesOptions.setStocks([stock0, stock1, stock2])
    portfolioSharesOptions.setSymbols(["Stock 0", "Stock 1", "Stock 2"])
    portfolioSharesOptions.setOptions(options)

    plotPortfolioSharesOptions = PlotPortfolioSharesOptions(portfolioSharesOptions)
    plotPortfolioSharesOptions.plotStocks("rel")
    plotPortfolioSharesOptions.plotAllocationMarkowitz(returnMax=0.01)
    plotPortfolioSharesOptions.plotAllocationLinearProgramming(returnMax=0.51, gamma=1)

def mainTest4():
    times = [dt.datetime(year=2026, month=6, day=1) + dt.timedelta(days=d) for d in range(17)]

    S0 = 306.31
    Kcall0 = 320.00
    Kput0 = 300.00

    S1 = 376.37
    Kcall1 = 400.00
    Kput1 = 350.00

    S2 = 224.36
    Kcall2 = 230.00
    Kput2 = 220.00

    my0 = -0.1
    my1 = -0.1
    my2 = -0.1

    sigma0 = 0.5
    sigma1 = 0.5
    sigma2 = 0.5

    implVolaCall0 = 0.2456
    implVolaPut0 = 0.2571

    implVolaCall1 = 0.3872
    implVolaPut1 = 0.2696

    implVolaCall2 = 0.4313
    implVolaPut2 = 0.4280

    stock0 = [S0]
    stock1 = [S1]
    stock2 = [S2]
    
    for i, time in enumerate(times):
        t = (time - times[0]) / (times[-1] - times[0])

        np.random.seed(i)
        if i == len(times) - 1:
            break
        stock0.append(stock0[-1] + my0 + (1 if np.random.random() < 0.5 else -1)*sigma0*np.random.normal(0, 1))
        stock1.append(stock1[-1] + my1 + (1 if np.random.random() < 0.5 else -1)*sigma1*np.random.normal(0, 1))
        stock2.append(stock2[-1] + my2 + (1 if np.random.random() < 0.5 else -1)*sigma2*np.random.normal(0, 1))

    options = {
        "riskFreeRate" : 0.0445,

        "callPrices" : [2.09, 3.07, 6.03],
        "callIndices" : [0, 1, 2],
        "callStrikes" : [Kcall0, Kcall1, Kcall2],
        "callVolatilities" : [implVolaCall0, implVolaCall1, implVolaCall2],

        "putPrices" : [3.73, 1.86, 6.05],
        "putIndices" : [0, 1, 2],
        "putStrikes" : [Kput0, Kput1, Kput2],
        "putVolatilities" : [implVolaPut0, implVolaPut1, implVolaPut2]
    }

    portfolioSharesOptions = PortfolioSharesOptions()
    portfolioSharesOptions.setTime(times)
    portfolioSharesOptions.setStocks([stock0, stock1, stock2])
    portfolioSharesOptions.setSymbols(["Stock 0", "Stock 1", "Stock 2"])
    portfolioSharesOptions.setOptions(options)

    plotPortfolioSharesOptions = PlotPortfolioSharesOptions(portfolioSharesOptions)
    plotPortfolioSharesOptions.plotStocks("rel")
    plotPortfolioSharesOptions.plotAllocationMarkowitz(returnMax=0.01)
    plotPortfolioSharesOptions.plotAllocationLinearProgramming(returnMax=0.52, gamma=1)

def mainMaster():
    portfolioSharesOptions = PortfolioSharesOptions()
    portfolioSharesOptions.databasePortfolio()

    # Calls
    GOOGLcallPrice = 3.07
    GOOGLcallStrike = 400
    GOOGLcallVolatility = 0.3872

    AAPLcallPrice = 2.09
    AAPLcallStrike = 320
    AAPLcallVolatility = 0.2456

    AMDcallPrice = 23.42
    AMDcallStrike = 530
    AMDcallVolatility = 0.7154

    INTCcallPrice = 8.00
    INTCcallStrike = 110
    INTCcallVolatility = 0.899

    NVIDIAcallPrice = 6.03
    NVIDIAcallStrike = 230
    NVIDIAcallVolatility = 0.4313

    # Puts
    GOOGLputPrice = 1.86
    GOOGLputStrike = 350
    GOOGLputVolatility = 0.2696

    AAPLputPrice = 3.73
    AAPLputStrike = 300
    AAPLputVolatility = 0.2571

    AMDputPrice = 21.40
    AMDputStrike = 490
    AMDputVolatility = 0.7185

    INTCputPrice = 5.90
    INTCputStrike = 105
    INTCputVolatility = 0.8465

    NVIDIAputPrice = 6.05
    NVIDIAputStrike = 220
    NVIDIAputVolatility = 0.4280

    options = {
        "riskFreeRate" : 0.0445,

        "callPrices" : [GOOGLcallPrice, AAPLcallPrice, AMDcallPrice, INTCcallPrice, NVIDIAcallPrice],
        "callIndices" : [0,1,2,3,4],
        "callStrikes" : [GOOGLcallStrike, AAPLcallStrike, AMDcallStrike, INTCcallStrike, NVIDIAcallStrike],
        "callVolatilities" : [GOOGLcallVolatility, AAPLcallVolatility, AMDcallVolatility, INTCcallVolatility, NVIDIAcallVolatility],

        "putPrices" : [GOOGLputPrice, AAPLputPrice, AMDputPrice, INTCputPrice, NVIDIAputPrice],
        "putIndices" : [0,1,2,3,4],
        "putStrikes" : [GOOGLputStrike, AAPLputStrike, AMDputStrike, INTCputStrike, NVIDIAputStrike],
        "putVolatilities" : [GOOGLputVolatility, AAPLputVolatility, AMDputVolatility, INTCputVolatility, NVIDIAputVolatility]
    }

    portfolioSharesOptions.setOptions(options)

    plotPortfolioSharesOptions = PlotPortfolioSharesOptions(portfolioSharesOptions)
    plotPortfolioSharesOptions.plotStocks("rel")
    plotPortfolioSharesOptions.plotAllocationMarkowitz()
    plotPortfolioSharesOptions.plotAllocationLinearProgramming(gamma=1)

def mainMasterOhneGoogle():
    portfolioSharesOptions = PortfolioSharesOptions()
    portfolioSharesOptions.databasePortfolio()

    stocks = portfolioSharesOptions.getStocks()
    symbols = portfolioSharesOptions.getSymbols()

    portfolioSharesOptions.setStocks(stocks[1:])
    portfolioSharesOptions.setSymbols(symbols[1:])

    # Calls
    AAPLcallPrice = 2.09
    AAPLcallStrike = 320
    AAPLcallVolatility = 0.2456

    AMDcallPrice = 23.42
    AMDcallStrike = 530
    AMDcallVolatility = 0.7154

    INTCcallPrice = 8.00
    INTCcallStrike = 110
    INTCcallVolatility = 0.899

    NVIDIAcallPrice = 6.03
    NVIDIAcallStrike = 230
    NVIDIAcallVolatility = 0.4313

    # Puts
    AAPLputPrice = 3.73
    AAPLputStrike = 300
    AAPLputVolatility = 0.2571

    AMDputPrice = 21.40
    AMDputStrike = 490
    AMDputVolatility = 0.7185

    INTCputPrice = 5.90
    INTCputStrike = 105
    INTCputVolatility = 0.8465

    NVIDIAputPrice = 6.05
    NVIDIAputStrike = 220
    NVIDIAputVolatility = 0.4280

    options = {
        "riskFreeRate" : 0.0445,

        "callPrices" : [AAPLcallPrice, AMDcallPrice, INTCcallPrice, NVIDIAcallPrice],
        "callIndices" : [0,1,2,3],
        "callStrikes" : [AAPLcallStrike, AMDcallStrike, INTCcallStrike, NVIDIAcallStrike],
        "callVolatilities" : [AAPLcallVolatility, AMDcallVolatility, INTCcallVolatility, NVIDIAcallVolatility],

        "putPrices" : [AAPLputPrice, AMDputPrice, INTCputPrice, NVIDIAputPrice],
        "putIndices" : [0,1,2,3],
        "putStrikes" : [AAPLputStrike, AMDputStrike, INTCputStrike, NVIDIAputStrike],
        "putVolatilities" : [AAPLputVolatility, AMDputVolatility, INTCputVolatility, NVIDIAputVolatility]
    }

    portfolioSharesOptions.setOptions(options)

    plotPortfolioSharesOptions = PlotPortfolioSharesOptions(portfolioSharesOptions)
    plotPortfolioSharesOptions.plotStocks("rel")
    plotPortfolioSharesOptions.plotAllocationMarkowitz()
    plotPortfolioSharesOptions.plotAllocationLinearProgramming(gamma=1, returnMax=2.5)

if __name__ == "__main__":
    mainMasterOhneGoogle()