from util.util import Util
from portfolio.portfolio import Portfolio
from mathematics.returns import RateOfReturn
from mathematics.covariance import Covariance

import numpy as np
import scipy.optimize as opt

class RiskMeasures:

    def __init__(self):
        self.rateOfReturn = RateOfReturn()
        self.covariance = Covariance()

    def mean(self, portfolio: Portfolio, allocation: np.ndarray) -> float:
        r = self.rateOfReturn.expectedReturn(portfolio=portfolio)
        return r.dot(allocation)
    
    def variance(self, portfolio: Portfolio, allocation: np.ndarray) -> float:
        sigma = self.covariance.covariance(portfolio=portfolio)
        return allocation.dot(sigma.dot(allocation))
    
    def averageValueAtRisk(self, portfolio: Portfolio, alpha: float, allocation: np.ndarray) -> float:
        n = len(portfolio.times) - 1

        prob = np.array(Util.prob(times=portfolio.times))

        xiStocks = self.rateOfReturn.initialRelativeReturn(portfolio=portfolio)
        xiCall = self.rateOfReturn.optionReturnCall(portfolio=portfolio)
        xiPut = self.rateOfReturn.optionReturnPut(portfolio=portfolio)

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