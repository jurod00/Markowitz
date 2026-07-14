from mathematics.returns import Returns
from mathematics.returns import RateOfReturn
from mathematics.covariance import Covariance
from mathematics.stochastics import Stochastics
from portfolio.portfolio import Portfolio
from util.util import Time
from util.util import Util

import numpy as np
import scipy.linalg as lina
import scipy.optimize as opt

class Allocations:

    def __init__(self):
        pass

    @staticmethod
    def allocationMarkowitz(portfolio: Portfolio, minimumReturn: float, shortSelling: bool=True):
        d = len(portfolio.stocks) + len(portfolio.indicesCall) + len(portfolio.indicesPut)
        r = Stochastics.expectation(portfolio=portfolio)
        # prec = Stochastics.precision(portfolio=portfolio)
        ones = np.ones(d)

        # np.set_printoptions(linewidth=np.inf)
        # print(prec)

        sigma = Stochastics.covariance(portfolio=portfolio)

        ya = lina.solve(sigma, r)
        yb = lina.solve(sigma, ones)
        yc = yb

        a = r.dot(ya)
        b = r.dot(yb)
        c = ones.dot(yc)
        d = a*c - b**2

        slopeVector = c/d*ya - b/d*yb
        shiftVector = a/d*yb - b/d*ya

        # a = r.dot(prec.dot(r))
        # b = r.dot(prec.dot(ones))
        # c = ones.dot(prec.dot(ones))
        # d = a*c - b**2

        # slopeVector = c/d*prec.dot(r) - b/d*prec.dot(ones)
        # shiftVector = a/d*prec.dot(ones) - b/d*prec.dot(r)

        if not shortSelling:
            pass

        return minimumReturn*slopeVector + shiftVector

    @staticmethod
    def allocationUtilityMaximization(portfolio: Portfolio, riskAversion: float):
        d = len(portfolio.stocks) + len(portfolio.indicesCall) + len(portfolio.indicesPut)
        r = Stochastics.expectation(portfolio=portfolio)
        prec = Stochastics.precision(portfolio=portfolio)
        ones = np.ones(d)

        return 1/riskAversion*np.matmul(prec, r + (riskAversion - ones.dot(prec.dot(r)))/ones.dot(prec.dot(ones))*ones)

    @staticmethod
    def allocationIntegratedRiskManagement(portfolio: Portfolio, alpha: float, beta: float, minimumReturn: float):
        d = len(portfolio.stocks) + len(portfolio.indicesCall) + len(portfolio.indicesPut)
        n = len(portfolio.times) - 1
        
        prob = np.array(Time.prob(times=portfolio.times))
        r = Stochastics.expectation(portfolio=portfolio)

        xiStocks = Returns.initialRelativeReturn(portfolio=portfolio)
        xiCall = Returns.optionReturnCall(portfolio=portfolio)
        xiPut = Returns.optionReturnPut(portfolio=portfolio)

        xi = np.hstack((xiStocks, xiCall, xiPut))

        c = np.empty(d+n+1)
        c[:d] = -(1-beta)*r
        c[d] = beta
        c[d+1:] = beta/(1-alpha)*prob

        A_ub = np.empty((n+1, d+n+1))
        A_ub[0,:d] = -r
        A_ub[0,d:] = 0

        for i in range(n):
            A_ub[i+1,:d] = -xi[i,:]
            A_ub[i+1, d] = -1
            A_ub[i+1,d+1:] = 0
            A_ub[i+1,d+1+i] = -1

        b_ub = np.empty(n+1)
        b_ub[0] = -minimumReturn
        b_ub[1:] = 0
        
        A_eq = np.empty((1, d+n+1))
        A_eq[0,:d] = 1
        A_eq[0,d:] = 0

        b_eq = np.empty(1)
        b_eq[0] = 1

        bounds = d*[(0, None)] + [(None, None)] + n*[(0, None)]

        solution = opt.linprog(
            c=c, 
            A_ub=A_ub, 
            b_ub=b_ub, 
            A_eq=A_eq, 
            b_eq=b_eq, 
            bounds=bounds, 
            method="highs"
        )

        if not solution.success:
            return d*[None], None
        
        return solution.x[:d], solution.fun
    
class AssetAllocation:

    def __init__(self, rateOfReturn=None, covariance=None):
        # Optional Dependency Injection
        self.rateOfReturn = rateOfReturn if rateOfReturn is not None else RateOfReturn()
        self.covariance = covariance if covariance is not None else Covariance()
        
        # Markowitz Access Memory
        self.slopeVector: np.ndarray=None
        self.shiftVector: np.ndarray=None

        # Utility Maximization Access Memory
        # TODO

        # Integrated Risk Management Access Memory
        # TODO

    def allocationMarkowitz(self, portfolio: Portfolio, minimumReturn: float, shortSellingAllowed: bool=True) -> np.ndarray:
        if self.slopeVector is not None and self.shiftVector is not None:
            return minimumReturn*self.slopeVector + self.shiftVector

        d = len(portfolio.stocks) + len(portfolio.indicesCall) + len(portfolio.indicesPut)
        r = self.rateOfReturn.expectedReturn(portfolio=portfolio)
        
        ones = np.ones(d)
        sigma = self.covariance.covariance(portfolio=portfolio)

        ya = lina.solve(sigma, r)
        yb = lina.solve(sigma, ones)

        a = r.dot(ya)
        b = r.dot(yb)
        c = ones.dot(yb)
        d = a*c - b**2

        self.slopeVector = c/d*ya - b/d*yb
        self.shiftVector = a/d*yb - b/d*ya

        if not shortSellingAllowed:
            pass

        return minimumReturn*self.slopeVector + self.shiftVector

    def allocationUtilityMaximization(self, portfolio: Portfolio, riskAversion: float) -> np.ndarray:
        d = len(portfolio.stocks) + len(portfolio.indicesCall) + len(portfolio.indicesPut)
        r = self.rateOfReturn.expectedReturn(portfolio=portfolio)

        prec = self.covariance.precision(portfolio=portfolio) # Todo: auf precision verzichten und kontrollieren, ob danach dasselbe herauskommt
        ones = np.ones(d)

        return 1/riskAversion*np.matmul(prec, r + (riskAversion - ones.dot(prec.dot(r)))/ones.dot(prec.dot(ones))*ones)

    def allocationIntegratedRiskManagement(self, portfolio: Portfolio, alpha: float, beta: float, minimumReturn: float) -> tuple:
        d = len(portfolio.stocks) + len(portfolio.indicesCall) + len(portfolio.indicesPut)
        n = len(portfolio.times) - 1
        
        prob = np.array(Util.prob(times=portfolio.times))
        r = self.rateOfReturn.expectedReturn(portfolio=portfolio)

        xiStocks = self.rateOfReturn.initialRelativeReturn(portfolio=portfolio)
        xiCall = self.rateOfReturn.optionReturnCall(portfolio=portfolio)
        xiPut = self.rateOfReturn.optionReturnPut(portfolio=portfolio)

        xi = np.hstack((xiStocks, xiCall, xiPut))

        c = np.empty(d+n+1)
        c[:d] = -(1-beta)*r
        c[d] = beta
        c[d+1:] = beta/(1-alpha)*prob

        A_ub = np.empty((n+1, d+n+1))
        A_ub[0,:d] = -r
        A_ub[0,d:] = 0

        for i in range(n):
            A_ub[i+1,:d] = -xi[i,:]
            A_ub[i+1, d] = -1
            A_ub[i+1,d+1:] = 0
            A_ub[i+1,d+1+i] = -1

        b_ub = np.empty(n+1)
        b_ub[0] = -minimumReturn
        b_ub[1:] = 0
        
        A_eq = np.empty((1, d+n+1))
        A_eq[0,:d] = 1
        A_eq[0,d:] = 0

        b_eq = np.empty(1)
        b_eq[0] = 1

        bounds = d*[(0, None)] + [(None, None)] + n*[(0, None)]

        solution = opt.linprog(
            c=c, 
            A_ub=A_ub, 
            b_ub=b_ub, 
            A_eq=A_eq, 
            b_eq=b_eq, 
            bounds=bounds, 
            method="highs"
        )

        if not solution.success:
            return d*[None], None
        
        return solution.x[:d], solution.fun