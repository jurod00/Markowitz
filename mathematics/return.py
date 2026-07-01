import math
import numpy as np

from portfolio.portfolio import Portfolio
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
    def optionReturn(portfolio: Portfolio):
        d = len(portfolio)
        n = len(portfolio.times) - 1

        prob = Time.prob(times=portfolio.times)