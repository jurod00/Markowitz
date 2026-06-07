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
#plt.rcParams.update({'font.size': 20})
plt.style.use("dark_background")

import pandas_datareader as pdr

def main():

    # Erste Vorgehensweise (log-returns je Timestamp):
    # xi = 1/(t_{i+1}-t_i)\log(V-v(T-t_{i+1})/(V-v(T-t_i)))

    # Zweite Vorgehensweise (konstant über gesamte Laufzeit):
    # xi = 1/T*\log(V-v(T))

    portfolio = PortfolioShares()
    portfolio.databasePortfolio()

    # time = [dt.datetime(year=2026, month=1, day=1) + dt.timedelta(days=d) for d in range(365)]
    # T = FiMa.duration(time)

    # stock1 = [100*(1+0.001)**t + 0.01*np.random.normal(0, 1) for t in range(365)]
    # # print(stock1)
    # stock2 = [100*(1-0.001)**t + 0.01*np.random.normal(0, 1) for t in range(365)]
    # # print(stock2)

    # K1 = 1.05*stock1[0]
    # xi = np.log(stock1[-1]/K1)
    # call1 = []
    # for i, t in enumerate(time):
    #     call1.append(K1*np.exp((t-time[0])/T)*xi + 0.01*np.random.normal(0,1))

    # K2 = 0.95*stock2[0]
    # xi = np.log(stock2[-1]/K2)
    # put2 = []
    # for t in time:
    #     put2.append(K2/np.exp((t-time[0])/T)*xi)

    # stocks = [stock1, stock2, call1, put2]

    # portfolio.setTime(time)
    # portfolio.setStocks(stocks)
    # portfolio.setSymbols(["steigende Aktie", "fallende Aktie", "call steigende Aktie", "put fallende Aktie"])

    plot = PlotPortfolioShares(portfolio)
    plot.plotStocks("rel")
    plot.plotAllocationMarkowitz()

    # Sigma = FiMa.covariance(time, stocks)
    # print(Sigma)

def mainNew():
    time = [dt.datetime(year=2026, month=1, day=1) + dt.timedelta(days=d) for d in range(365)]

    stock1 = []
    stock2 = []

    S0 = 100
    my1 = 0.5
    my2 = -0.5
    sigma = 0.5

    for t in range(365):
        stock1.append(S0*np.exp((my1-0.5*sigma**2)*t/365 + sigma*np.random.normal(0, t/365)))
        stock2.append(S0*np.exp((my2-0.5*sigma**2)*t/365 + sigma*np.random.normal(0, t/365)))

    callStrike1 = 1.01*stock1[0]
    putStrike1 = 0.99*stock1[0]
    volatility1 = FiMa.volatilityEstimator(time, stock1)*float(1e+4)
    volatility1 = np.sqrt(0.02)

    callStrike2 = 1.01*stock2[0]
    putStrike2 = 0.99*stock2[0]
    volatility2 = FiMa.volatilityEstimator(time, stock2)*float(1e+4)
    volatility2 = np.sqrt(0.02)

    options = {
        "riskFreeRate" : 0.05,

        "callIndices" : [0, 1],
        "callStrikes" : [callStrike1, callStrike2],

        "putIndices" : [0, 1],
        "putStrikes" : [putStrike1, putStrike2],

        "volatilities" : [sigma, sigma]
    }

    options = {
        "riskFreeRate" : 0.05,

        "callIndices" : [],
        "callStrikes" : [],

        "putIndices" : [],
        "putStrikes" : [],

        "volatilities" : []
    }

    symbols = ["Aktie /", "Aktie \\", "Call /", "Call \\", "Put /", "Put \\"]

    symbols = ["Aktie /", "Aktie \\"]

    portfolioSharesOptions = PortfolioSharesOptions()
    portfolioSharesOptions.setTime(time)
    portfolioSharesOptions.setStocks([stock1, stock2])
    portfolioSharesOptions.setOptions(options)
    portfolioSharesOptions.setSymbols(symbols)

    plot = PlotPortfolioSharesOptions(portfolioSharesOptions)
    plot.plotAllocationMarkowitz(returnMax=1)
    plot.plotAllocationLinearProgramming(returnMax=1)

    plt = PlotPortfolioShares(portfolioSharesOptions)
    plt.plotStocks("abs")

    print(FiMa.volatilityEstimator(time, stock1))
    print(FiMa.volatilityEstimator(time, stock2))

def mainGreeks():
    stockPrice = 123
    strikePrice = 120
    daysToMaturity = 30
    volatility = 0.255
    riskFreeRate = 0.055

    print("Delta " + str(FiMa.delta(daysToMaturity=daysToMaturity, stockPrice=stockPrice, strikePrice=strikePrice, volatility=volatility, riskFreeRate=riskFreeRate)))
    print("Gamma " + str(FiMa.gamma(daysToMaturity=daysToMaturity, stockPrice=stockPrice, strikePrice=strikePrice, volatility=volatility, riskFreeRate=riskFreeRate)))
    print("Theta " + str(FiMa.theta(daysToMaturity=daysToMaturity, stockPrice=stockPrice, strikePrice=strikePrice, volatility=volatility, riskFreeRate=riskFreeRate)))

def mainEstimator():
    times = [dt.datetime(year=2026, month=1, day=1) + dt.timedelta(days=d) for d in range(365)]

    S0 = 100

    my1 = 0.5
    my2 = -0.5

    sigma1 = 0.5
    sigma2 = 0.5

    tests = [i for i in range(100)]
    sigmas = []

    for _ in tests:

        stock1 = []
        stock2 = []
        
        for time in times:
            t = (time - times[0]) / (times[-1] - times[0]) # (Vergangene Zeit seit t0) geteilt durch (Gesamtzeit)

            stock1.append(S0*np.exp((my1-0.5*sigma1**2)*t + sigma1*np.random.normal(0, t)))
            stock2.append(S0*np.exp((my2-0.5*sigma2**2)*t + sigma2*np.random.normal(0, t)))
        
        # print("sigma1 = " + str(FiMa.volatilityEstimator(times, stock1, "rel")))
        # print("sigma2 = " + str(FiMa.volatilityEstimator(times, stock2, "rel")))

        sigmas.append(FiMa.volatilityEstimator(times, stock1))

    fig, ax = plt.subplots()
    ax.plot(tests, sigmas)
    ax.plot(tests, [sigma1]*100)
    ax.set_ylim(0, 1)
    plt.show()


    myHat1 = 0
    for i in range(len(times)-1):
        deltaT = (times[i+1] - times[i]) / (times[-1] - times[0])
        myHat1 += np.log(stock1[i+1]/stock1[i]) * deltaT

    sTemp = 0
    for i in range(len(times)-1):
        deltaT = (times[i+1] - times[i]) / (times[-1] - times[0])
        sTemp += (np.log(stock1[i+1]/stock1[i]) - myHat1)**2 * deltaT

    sigmaHat1 = np.sqrt(sTemp)

    print("sigma1 = " + str(sigmaHat1))

    myHat2 = 0
    for i in range(len(times)-1):
        deltaT = (times[i+1] - times[i]) / (times[-1] - times[0])
        myHat2 += np.log(stock2[i+1]/stock2[i]) * deltaT

    sTemp = 0
    for i in range(len(times)-1):
        deltaT = (times[i+1] - times[i]) / (times[-1] - times[0])
        sTemp += (np.log(stock2[i+1]/stock2[i]) - myHat2)**2 * deltaT

    sigmaHat2 = np.sqrt(sTemp)

    print("sigma2 = " + str(sigmaHat2))

def mainImpliedVolatility():
    optionPrice = FiMa.priceOption(daysToMaturity=17, stockPrice=306.31, strikePrice=300.00, volatility=0.2571, riskFreeRate=0.0445)
    print(optionPrice)

    sigma = FiMa.impliedVolatility(optionPrice=3.73, daysToMaturity=17, stockPrice=306.31, strikePrice=300.00, riskFreeRate=0.0445)
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
    portfolioSharesOptions.setSymbols(["Stock /", "Call /"])
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
    portfolioSharesOptions.setSymbols(["Stock \\", "Put \\"])
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
    portfolioSharesOptions.setSymbols(["Stock 0", "Stock 1", "Stock 2", "Put 0", "Put 1", "Put 2"])
    portfolioSharesOptions.setOptions(options)

    plotPortfolioSharesOptions = PlotPortfolioSharesOptions(portfolioSharesOptions)
    plotPortfolioSharesOptions.plotStocks("abs")
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

    my0 = -0.05
    my1 = -0.05
    my2 = -0.05

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
    portfolioSharesOptions.setSymbols(["Stock 0", "Stock 1", "Stock 2", "Call 0", "Call 1", "Call 2", "Put 0", "Put 1", "Put 2"])
    portfolioSharesOptions.setOptions(options)

    plotPortfolioSharesOptions = PlotPortfolioSharesOptions(portfolioSharesOptions)
    plotPortfolioSharesOptions.plotStocks("abs")
    plotPortfolioSharesOptions.plotAllocationMarkowitz(returnMax=0.01)
    plotPortfolioSharesOptions.plotAllocationLinearProgramming(returnMax=1, gamma=1)

if __name__ == "__main__":
    mainTest4()