from mathematics.options import Options
from portfolio.portfolio import Portfolio
from util.util import Util

import math
import numpy as np

class Returns:

    def __init__(self, options: Options=None):
        self.options = options if options is not None else Options()

    def absoluteReturn(self, portfolio: Portfolio) -> np.ndarray:
        d = len(portfolio.stocks)
        n = len(portfolio.times) - 1

        prob = Util.prob(times=portfolio.times)

        xi = np.empty((n,d))
        for i in range(n):
            for j in range(d):
                xi[i,j] = (portfolio.stocks[j][i+1] - portfolio.stocks[j][i])/prob[i]

        return xi

    def relativeReturn(self, portfolio: Portfolio) -> np.ndarray:
        d = len(portfolio.stocks)
        n = len(portfolio.times) - 1

        prob = Util.prob(times=portfolio.times)

        xi = np.empty((n,d))
        for i in range(n):
            for j in range(d):
                xi[i,j] = (portfolio.stocks[j][i+1]/portfolio.stocks[j][i] - 1)/prob[i]

        return xi

    def initialRelativeReturn(self, portfolio: Portfolio) -> np.ndarray:
        d = len(portfolio.stocks)
        n = len(portfolio.times) - 1

        prob = Util.prob(times=portfolio.times)

        xi = np.empty((n,d))
        for i in range(n):
            for j in range(d):
                xi[i,j] = ((portfolio.stocks[j][i+1] - portfolio.stocks[j][i])/portfolio.stocks[j][0])/prob[i]

        return xi

    def logReturn(self, portfolio: Portfolio) -> np.ndarray:
        d = len(portfolio.stocks)
        n = len(portfolio.times) - 1

        prob = Util.prob(times=portfolio.times)

        xi = np.empty((n,d))
        for i in range(n):
            for j in range(d):
                xi[i,j] = math.log(portfolio.stocks[j][i+1]/portfolio.stocks[j][i])/prob[i]

        return xi
    
    def optionReturnCall(self, portfolio: Portfolio) -> np.ndarray:
        d = len(portfolio.indicesCall)
        n = len(portfolio.times) - 1

        if d == 0:
            return np.empty((n, 0))

        xi = np.empty((n, d))
        for j0, j in enumerate(portfolio.indicesCall):
            price = self.options.priceOptionCall(
                daysToMaturity=(portfolio.times[-1] - portfolio.times[0]).days, 
                stockPrice=portfolio.stocks[j][0], 
                strikePrice=portfolio.strikesCall[j0], 
                riskFreeRate=portfolio.riskFreeRate, 
                implVolatility=portfolio.implVolCall[j0]
            )

            for i in range(n):
                tau = (portfolio.times[-1] - portfolio.times[i]).days

                delta = self.options.deltaCall(
                    daysToMaturity=tau, 
                    stockPrice=portfolio.stocks[j][i], 
                    strikePrice=portfolio.strikesCall[j0], 
                    riskFreeRate=portfolio.riskFreeRate, 
                    implVolatility=portfolio.implVolCall[j0]
                )
                gamma = self.options.gamma(
                    daysToMaturity=tau, 
                    stockPrice=portfolio.stocks[j][i], 
                    strikePrice=portfolio.strikesCall[j0], 
                    riskFreeRate=portfolio.riskFreeRate, 
                    implVolatility=portfolio.implVolCall[j0]
                )
                theta = self.options.thetaCall(
                    daysToMaturity=tau, 
                    stockPrice=portfolio.stocks[j][i], 
                    strikePrice=portfolio.strikesCall[j0], 
                    riskFreeRate=portfolio.riskFreeRate, 
                    implVolatility=portfolio.implVolCall[j0]
                )
                dS = portfolio.stocks[j][i+1] - portfolio.stocks[j][i]
                dt = (portfolio.times[i+1] - portfolio.times[i])/(portfolio.times[-1] - portfolio.times[0])
                dC = delta*dS + 0.5*gamma*dS**2 + theta*dt

                xi[i,j0] = dC/price/dt
        
        return xi
    
    def optionReturnPut(self, portfolio: Portfolio) -> np.ndarray:
        d = len(portfolio.indicesPut)
        n = len(portfolio.times) - 1

        if d == 0:
            return np.empty((n, 0))

        xi = np.empty((n, d))
        for j0, j in enumerate(portfolio.indicesPut):
            price = self.options.priceOptionPut(
                daysToMaturity=(portfolio.times[-1] - portfolio.times[0]).days, 
                stockPrice=portfolio.stocks[j][0], 
                strikePrice=portfolio.strikesPut[j0], 
                riskFreeRate=portfolio.riskFreeRate, 
                implVolatility=portfolio.implVolPut[j0]
            )

            for i in range(n):
                tau = (portfolio.times[-1] - portfolio.times[i]).days

                delta = self.options.deltaPut(
                    daysToMaturity=tau, 
                    stockPrice=portfolio.stocks[j][i], 
                    strikePrice=portfolio.strikesPut[j0], 
                    riskFreeRate=portfolio.riskFreeRate, 
                    implVolatility=portfolio.implVolPut[j0]
                )
                gamma = self.options.gamma(
                    daysToMaturity=tau, 
                    stockPrice=portfolio.stocks[j][i], 
                    strikePrice=portfolio.strikesPut[j0], 
                    riskFreeRate=portfolio.riskFreeRate, 
                    implVolatility=portfolio.implVolPut[j0]
                )
                theta = self.options.thetaPut(
                    daysToMaturity=tau, 
                    stockPrice=portfolio.stocks[j][i], 
                    strikePrice=portfolio.strikesPut[j0], 
                    riskFreeRate=portfolio.riskFreeRate, 
                    implVolatility=portfolio.implVolPut[j0]
                )
                dS = portfolio.stocks[j][i+1] - portfolio.stocks[j][i]
                dt = (portfolio.times[i+1] - portfolio.times[i])/(portfolio.times[-1] - portfolio.times[0])
                dP = delta*dS + 0.5*gamma*dS**2 + theta*dt

                xi[i,j0] = dP/price/dt

        return xi
    
    def expectedReturn(self, portfolio: Portfolio) -> np.ndarray:
        prob = np.array(Util.prob(times=portfolio.times))

        xiStocks = self.initialRelativeReturn(portfolio=portfolio)
        xiCall = self.optionReturnCall(portfolio=portfolio)
        xiPut = self.optionReturnPut(portfolio=portfolio)

        xi = np.hstack((xiStocks, xiCall, xiPut))
        return np.matmul(prob, xi)