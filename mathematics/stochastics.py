import numpy as np
import scipy.optimize as opt

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
    def averageValueAtRisk(portfolio: Portfolio, alpha: float, allocation: np.ndarray) -> float:
        n = len(portfolio.times) - 1

        prob = np.array(Time.prob(times=portfolio.times))

        xiStocks = Returns.initialRelativeReturn(portfolio=portfolio)
        xiCall = Returns.optionReturnCall(portfolio=portfolio)
        xiPut = Returns.optionReturnPut(portfolio=portfolio)

        xi = np.hstack((xiStocks, xiCall, xiPut))

        c = np.empty(n+1)
        c[0] = 1
        c[1:] = 1/(1-alpha)*prob

        A_ub = np.empty((n, n+1))
        for i in range(n):
            A_ub[i, 0] = -1
            A_ub[i,1:] = 0
            A_ub[i,1+i] = -1
        
        b_ub = np.empty(n)
        for i in range(n):
            b_ub[i] = allocation.dot(xi[i,:])

        bounds = [(None, None)] + n*[(0, None)]

        solution = opt.linprog(
            c=c, 
            A_ub=A_ub, 
            b_ub=b_ub, 
            bounds=bounds, 
            method="highs"
        )

        return solution.fun