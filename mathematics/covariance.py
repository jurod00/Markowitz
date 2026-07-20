from mathematics.returns import Returns
from portfolio.portfolio import Portfolio
from util.util import Util

import numpy as np

class Covariance:

    def __init__(self, returns: Returns=None):
        self.returns = returns if returns is not None else Returns()

    def covariance(self, portfolio: Portfolio) -> np.ndarray:
        prob = np.array(Util.prob(times=portfolio.times))
        diag = np.diag(prob)

        xiStocks = self.returns.initialRelativeReturn(portfolio=portfolio)
        xiCall = self.returns.optionReturnCall(portfolio=portfolio)
        xiPut = self.returns.optionReturnPut(portfolio=portfolio)

        xi = np.hstack((xiStocks, xiCall, xiPut))
        r = self.returns.expectedReturn(portfolio=portfolio)

        return xi.transpose().dot(diag.dot(xi)) - np.outer(r, r)

    def precision(self, portfolio: Portfolio) -> np.ndarray:
        sigma = self.covariance(portfolio=portfolio)
        return np.linalg.inv(sigma)