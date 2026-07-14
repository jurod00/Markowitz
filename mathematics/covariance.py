from util.util import Util
from portfolio.portfolio import Portfolio
from mathematics.returns import RateOfReturn

import numpy as np

class Covariance:

    def __init__(self):
        self.rateOfReturn = RateOfReturn()

    def covariance(self, portfolio: Portfolio) -> np.ndarray:
        prob = np.array(Util.prob(times=portfolio.times))
        diag = np.diag(prob)

        xiStocks = self.rateOfReturn.initialRelativeReturn(portfolio=portfolio)
        xiCall = self.rateOfReturn.optionReturnCall(portfolio=portfolio)
        xiPut = self.rateOfReturn.optionReturnPut(portfolio=portfolio)

        xi = np.hstack((xiStocks, xiCall, xiPut))
        r = self.rateOfReturn.expectedReturn(portfolio=portfolio)

        return xi.transpose().dot(diag.dot(xi)) - np.outer(r, r)

    def precision(self, portfolio: Portfolio) -> np.ndarray:
        sigma = self.covariance(portfolio=portfolio)
        return np.linalg.inv(sigma)