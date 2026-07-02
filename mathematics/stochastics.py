import numpy as np

from util.time import Time
from mathematics.returns import Returns
from portfolio.portfolio import Portfolio

class Stochastics:

    def __init__(self):
        pass

    @staticmethod
    def expectation(portfolio: Portfolio) -> np.ndarray:
        prob = np.array(Time.prob(times=portfolio.times))

        xiStocks = Returns.initialRelativeReturn(portfolio=portfolio)
        xiCall = Returns.optionReturnCall(portfolio=portfolio)
        xiPut = Returns.optionReturnPut(portfolio=portfolio)

        xi = np.hstack((xiStocks, xiCall, xiPut))
        return np.matmul(prob, xi)

    @staticmethod
    def covariance(portfolio: Portfolio) -> np.ndarray:
        prob = np.array(Time.prob(times=portfolio.times))
        diag = np.diag(prob)

        xiStocks = Returns.initialRelativeReturn(portfolio=portfolio)
        xiCall = Returns.optionReturnCall(portfolio=portfolio)
        xiPut = Returns.optionReturnPut(portfolio=portfolio)

        xi = np.hstack((xiStocks, xiCall, xiPut))
        r = Stochastics.expectation(portfolio=portfolio)

        return xi.transpose().dot(diag.dot(xi)) - np.outer(r, r)
        

    @staticmethod
    def precision(portfolio: Portfolio) -> np.ndarray:
        sigma = Stochastics.covariance(portfolio=portfolio)

        return np.linalg.inv(sigma)

    @staticmethod
    def meanVariance(portfolio: Portfolio, allocation: np.ndarray) -> tuple:
        r = Stochastics.expectation(portfolio=portfolio)
        sigma = Stochastics.covariance(portfolio=portfolio)

        mean = r.dot(allocation)
        variance = allocation.dot(sigma.dot(allocation))

        return mean, variance
    
    @staticmethod
    def averageValueAtRisk(portfolio: Portfolio, alpha: float, beta: float, allocation: np.ndarray) -> float:
        pass