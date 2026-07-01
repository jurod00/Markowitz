import math
import numpy as np

from portfolio.portfolio import Portfolio
from mathematics.option import Option
from util.time import Time

class Return:

    def __init__(self):
        pass

    @staticmethod
    def absoluteReturn(times: list, stocks: list):
        d = len(stocks)
        n = len(times) - 1

        prob = Time.prob(times=times)

        xi = np.empty((n,d))
        for i in range(n):
            for j in range(d):
                xi[i,j] = (stocks[j][i+1] - stocks[j][i])/prob[i]

        return xi

    @staticmethod
    def relativeReturn(times: list, stocks: list):
        d = len(stocks)
        n = len(times) - 1

        prob = Time.prob(times=times)

        xi = np.empty((n,d))
        for i in range(n):
            for j in range(d):
                xi[i,j] = (stocks[j][i+1]/stocks[j][i] - 1)/prob[i]

        return xi

    @staticmethod
    def initialRelativeReturn(times: list, stocks: list):
        d = len(stocks)
        n = len(times) - 1

        prob = Time.prob(times=times)

        xi = np.empty((n,d))
        for i in range(n):
            for j in range(d):
                xi[i,j] = ((stocks[j][i+1] - stocks[j][i])/stocks[j][0])/prob[i]

        return xi

    @staticmethod
    def logReturn(times: list, stocks: list):
        d = len(stocks)
        n = len(times) - 1

        prob = Time.prob(times=times)

        xi = np.empty((n,d))
        for i in range(n):
            for j in range(d):
                xi[i,j] = math.log(stocks[j][i+1]/stocks[j][i])/prob[i]

        return xi
    
    @staticmethod
    def optionReturnCall(portfolio: Portfolio):
        d = len(portfolio.indicesCall)
        n = len(portfolio.times) - 1

        xi = np.empty((n,d))
        for j0, j in enumerate(portfolio.indicesCall):
            price = Option.priceCall(
                daysToMaturity=(portfolio.times[-1] - portfolio.times[0]).days, 
                stockPrice=portfolio.stocks[j][0], 
                strikePrice=portfolio.strikesCall[j0], 
                riskFreeRate=portfolio.riskFreeRate, 
                implVolatility=portfolio.implVolCall[j0]
            )

            for i in range(n):
                tau = (portfolio.times[-1] - portfolio.times[i]).days

                delta = Option.deltaCall(
                    daysToMaturity=tau, 
                    stockPrice=portfolio.stocks[j][i], 
                    strikePrice=portfolio.strikesCall[j0], 
                    riskFreeRate=portfolio.riskFreeRate, 
                    implVolatility=portfolio.implVolCall[j0]
                )
                gamma = Option.gamma(
                    daysToMaturity=tau, 
                    stockPrice=portfolio.stocks[j][i], 
                    strikePrice=portfolio.strikesCall[j0], 
                    riskFreeRate=portfolio.riskFreeRate, 
                    implVolatility=portfolio.implVolCall[j0]
                )
                theta = Option.thetaCall(
                    daysToMaturity=tau, 
                    stockPrice=portfolio.stocks[j][i], 
                    strikePrice=portfolio.strikesCall[j0], 
                    riskFreeRate=portfolio.riskFreeRate, 
                    implVolatility=portfolio.implVolCall[j0]
                )
                dS = portfolio.stocks[j][i+1] - portfolio.stocks[j][i]
                dt = (portfolio.times[i+1] - portfolio.times[i])/(portfolio.times[-1] - portfolio.times[0])
                dC = delta*dS + 0.5*gamma*dS**2 + theta*dt

                xi[i, j0] = dC/price/dt
        
        return xi
    
    def optionReturnPut(portfolio: Portfolio):
        d = len(portfolio.indicesPut)
        n = len(portfolio.times) - 1

        xi = np.empty((n,d))
        for j0, j in enumerate(portfolio.indicesPut):
            price = Option.pricePut(
                daysToMaturity=(portfolio.times[-1] - portfolio.times[0]).days, 
                stockPrice=portfolio.stocks[j][0], 
                strikePrice=portfolio.strikesPut[j0], 
                riskFreeRate=portfolio.riskFreeRate, 
                implVolatility=portfolio.implVolPut[j0]
            )

            for i in range(n):
                tau = (portfolio.times[-1] - portfolio.times[i]).days

                delta = Option.deltaPut(
                    daysToMaturity=tau, 
                    stockPrice=portfolio.stocks[j][i], 
                    strikePrice=portfolio.strikesPut[j0], 
                    riskFreeRate=portfolio.riskFreeRate, 
                    implVolatility=portfolio.implVolPut[j0]
                )
                gamma = Option.gamma(
                    daysToMaturity=tau, 
                    stockPrice=portfolio.stocks[j][i], 
                    strikePrice=portfolio.strikesPut[j0], 
                    riskFreeRate=portfolio.riskFreeRate, 
                    implVolatility=portfolio.implVolPut[j0]
                )
                theta = Option.thetaPut(
                    daysToMaturity=tau, 
                    stockPrice=portfolio.stocks[j][i], 
                    strikePrice=portfolio.strikesPut[j0], 
                    riskFreeRate=portfolio.riskFreeRate, 
                    implVolatility=portfolio.implVolPut[j0]
                )
                dS = portfolio.stocks[j][i+1] - portfolio.stocks[j][i]
                dt = (portfolio.times[i+1] - portfolio.times[i])/(portfolio.times[-1] - portfolio.times[0])
                dP = delta*dS + 0.5*gamma*dS**2 + theta*dt

                xi[i, j0] = dP/price/dt

        return xi