from mathematics.covariance import Covariance
from mathematics.returns import Returns
from portfolio.portfolio import Portfolio
from util.util import Util

import numpy as np
import scipy.linalg as lina
import scipy.optimize as opt

class Allocations:

    def __init__(self, returns: Returns=None, covariance: Covariance=None):
        # Optional Dependency Injection
        self.returns = returns if returns is not None else Returns()
        self.covariance = covariance if covariance is not None else Covariance()
        # Access Memory
        self.memory: bool=False

    def saveMemory(self, portfolio: Portfolio):
        self.d = len(portfolio.stocks) + len(portfolio.indicesCall) + len(portfolio.indicesPut)
        self.r = self.returns.expectedReturn(portfolio=portfolio)

        self.ones = np.ones(self.d)
        self.sigma = self.covariance.covariance(portfolio=portfolio)

        y1 = lina.solve(self.sigma, self.r)
        y2 = lina.solve(self.sigma, self.ones)

        self.a = self.r.dot(y1)
        self.b = self.r.dot(y2)
        self.c = self.ones.dot(y2)
        self.d = self.a*self.c - self.b**2

        self.slopeVector = self.c/self.d*y1 - self.b/self.d*y2
        self.shiftVector = self.a/self.d*y2 - self.b/self.d*y1

        self.memory = True

    def allocationMarkowitz(self, portfolio: Portfolio, minimumReturn: float, shortSellingAllowed: bool=True) -> np.ndarray:
        if not self.memory:
            self.saveMemory(portfolio=portfolio)

        if not shortSellingAllowed:
            pass

        return minimumReturn*self.slopeVector + self.shiftVector

    def allocationUtilityMaximization(self, portfolio: Portfolio, riskAversion: float) -> np.ndarray:
        if not self.memory:
            self.saveMemory(portfolio=portfolio)

        return 1/riskAversion*lina.solve(self.sigma, self.r + (riskAversion-self.b)/self.c*self.ones)

    def allocationIntegratedRiskManagement(self, portfolio: Portfolio, alpha: float, beta: float, minimumReturn: float) -> tuple:
        d = len(portfolio.stocks) + len(portfolio.indicesCall) + len(portfolio.indicesPut)
        n = len(portfolio.times) - 1
        
        prob = np.array(Util.prob(times=portfolio.times))
        r = self.returns.expectedReturn(portfolio=portfolio)

        xiStocks = self.returns.initialRelativeReturn(portfolio=portfolio)
        xiCall = self.returns.optionReturnCall(portfolio=portfolio)
        xiPut = self.returns.optionReturnPut(portfolio=portfolio)

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