import math
import numpy as np

from portfolio.portfolio import Portfolio
from mathematics.options import Options
from util.time import Time

class Returns:

    def __init__(self):
        pass

    @staticmethod
    def absoluteReturn(portfolio: Portfolio) -> np.ndarray:
        d = len(portfolio.stocks)
        n = len(portfolio.times) - 1

        prob = Time.prob(times=portfolio.times)

        xi = np.empty((n,d))
        for i in range(n):
            for j in range(d):
                xi[i,j] = (portfolio.stocks[j][i+1] - portfolio.stocks[j][i])/prob[i]

        return xi

    @staticmethod
    def relativeReturn(portfolio: Portfolio) -> np.ndarray:
        d = len(portfolio.stocks)
        n = len(portfolio.times) - 1

        prob = Time.prob(times=portfolio.times)

        xi = np.empty((n,d))
        for i in range(n):
            for j in range(d):
                xi[i,j] = (portfolio.stocks[j][i+1]/portfolio.stocks[j][i] - 1)/prob[i]

        return xi

    @staticmethod
    def initialRelativeReturn(portfolio: Portfolio) -> np.ndarray:
        d = len(portfolio.stocks)
        n = len(portfolio.times) - 1

        prob = Time.prob(times=portfolio.times)

        xi = np.empty((n,d))
        for i in range(n):
            for j in range(d):
                xi[i,j] = ((portfolio.stocks[j][i+1] - portfolio.stocks[j][i])/portfolio.stocks[j][0])/prob[i]

        return xi

    @staticmethod
    def logReturn(portfolio: Portfolio) -> np.ndarray:
        d = len(portfolio.stocks)
        n = len(portfolio.times) - 1

        prob = Time.prob(times=portfolio.times)

        xi = np.empty((n,d))
        for i in range(n):
            for j in range(d):
                xi[i,j] = math.log(portfolio.stocks[j][i+1]/portfolio.stocks[j][i])/prob[i]

        return xi
    
    @staticmethod
    def optionReturnCall(portfolio: Portfolio) -> np.ndarray:
        if not portfolio.indicesCall:
            return np.empty(0) 
        
        d = len(portfolio.indicesCall)
        n = len(portfolio.times) - 1

        xi = np.empty((n,d))
        for j0, j in enumerate(portfolio.indicesCall):
            price = Options.priceCall(
                daysToMaturity=(portfolio.times[-1] - portfolio.times[0]).days, 
                stockPrice=portfolio.stocks[j][0], 
                strikePrice=portfolio.strikesCall[j0], 
                riskFreeRate=portfolio.riskFreeRate, 
                implVolatility=portfolio.implVolCall[j0]
            )

            for i in range(n):
                tau = (portfolio.times[-1] - portfolio.times[i]).days

                delta = Options.deltaCall(
                    daysToMaturity=tau, 
                    stockPrice=portfolio.stocks[j][i], 
                    strikePrice=portfolio.strikesCall[j0], 
                    riskFreeRate=portfolio.riskFreeRate, 
                    implVolatility=portfolio.implVolCall[j0]
                )
                gamma = Options.gamma(
                    daysToMaturity=tau, 
                    stockPrice=portfolio.stocks[j][i], 
                    strikePrice=portfolio.strikesCall[j0], 
                    riskFreeRate=portfolio.riskFreeRate, 
                    implVolatility=portfolio.implVolCall[j0]
                )
                theta = Options.thetaCall(
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
    
    def optionReturnPut(portfolio: Portfolio) -> np.ndarray:
        if not portfolio.indicesPut:
            return np.empty(0)
        
        d = len(portfolio.indicesPut)
        n = len(portfolio.times) - 1

        xi = np.empty((n,d))
        for j0, j in enumerate(portfolio.indicesPut):
            price = Options.pricePut(
                daysToMaturity=(portfolio.times[-1] - portfolio.times[0]).days, 
                stockPrice=portfolio.stocks[j][0], 
                strikePrice=portfolio.strikesPut[j0], 
                riskFreeRate=portfolio.riskFreeRate, 
                implVolatility=portfolio.implVolPut[j0]
            )

            for i in range(n):
                tau = (portfolio.times[-1] - portfolio.times[i]).days

                delta = Options.deltaPut(
                    daysToMaturity=tau, 
                    stockPrice=portfolio.stocks[j][i], 
                    strikePrice=portfolio.strikesPut[j0], 
                    riskFreeRate=portfolio.riskFreeRate, 
                    implVolatility=portfolio.implVolPut[j0]
                )
                gamma = Options.gamma(
                    daysToMaturity=tau, 
                    stockPrice=portfolio.stocks[j][i], 
                    strikePrice=portfolio.strikesPut[j0], 
                    riskFreeRate=portfolio.riskFreeRate, 
                    implVolatility=portfolio.implVolPut[j0]
                )
                theta = Options.thetaPut(
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