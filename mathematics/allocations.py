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
        self.memoryMarkowitz: bool=False
        self.memoryIRM: bool=False

    def saveMemoryMarkowitz(self, portfolio: Portfolio):
        self.d = len(portfolio.stocks) + len(portfolio.indicesCall) + len(portfolio.indicesPut)
        self.n = len(portfolio.times) - 1

        self.r = self.returns.expectedReturn(portfolio=portfolio)

        self.ones = np.ones(self.d)
        self.sigma = self.covariance.covariance(portfolio=portfolio)

        y1 = lina.solve(self.sigma, self.r)
        y2 = lina.solve(self.sigma, self.ones)

        self.a = self.r.dot(y1)
        self.b = self.r.dot(y2)
        self.c = self.ones.dot(y2)
        det = self.a*self.c - self.b**2

        self.slopeVector = self.c/det*y1 - self.b/det*y2
        self.shiftVector = self.a/det*y2 - self.b/det*y1

        self.memoryMarkowitz = True

    def saveMemoryIRM(self, portfolio: Portfolio, alpha: float, beta: float):
        self.d = len(portfolio.stocks) + len(portfolio.indicesCall) + len(portfolio.indicesPut)
        self.n = len(portfolio.times) - 1

        prob = np.array(Util.prob(times=portfolio.times))
        r = self.returns.expectedReturn(portfolio=portfolio)

        xiStocks = self.returns.initialRelativeReturn(portfolio=portfolio)
        xiCall = self.returns.optionReturnCall(portfolio=portfolio)
        xiPut = self.returns.optionReturnPut(portfolio=portfolio)

        xi = np.hstack((xiStocks, xiCall, xiPut))

        self.cost = np.empty(self.d+self.n+1)
        self.cost[:self.d] = -(1-beta)*r
        self.cost[self.d] = beta
        self.cost[self.d+1:] = beta/(1-alpha)*prob

        self.A_ub = np.empty((self.n+1, self.d+self.n+1))
        self.A_ub[0,:self.d] = -r
        self.A_ub[0,self.d:] = 0

        for i in range(self.n):
            self.A_ub[i+1,:self.d] = -xi[i,:]
            self.A_ub[i+1, self.d] = -1
            self.A_ub[i+1,self.d+1:] = 0
            self.A_ub[i+1,self.d+1+i] = -1

        self.b_ub = np.zeros(self.n+1)
        
        self.A_eq = np.empty((1, self.d+self.n+1))
        self.A_eq[0,:self.d] = 1
        self.A_eq[0,self.d:] = 0

        self.b_eq = np.empty(1)
        self.b_eq[0] = 1

        self.bounds = self.d*[(0, None)] + [(None, None)] + self.n*[(0, None)]

        self.memoryIRM = True

    def allocationMarkowitz(self, portfolio: Portfolio, minimumReturn: float, shortSellingAllowed: bool=True) -> np.ndarray:
        if not self.memoryMarkowitz:
            self.saveMemoryMarkowitz(portfolio=portfolio)

        if not shortSellingAllowed:
            pass

        return minimumReturn*self.slopeVector + self.shiftVector

    def allocationUtilityMaximization(self, portfolio: Portfolio, riskAversion: float) -> np.ndarray:
        if not self.memoryMarkowitz:
            self.saveMemoryMarkowitz(portfolio=portfolio)

        return 1/riskAversion*lina.solve(self.sigma, self.r + (riskAversion-self.b)/self.c*self.ones)

    def allocationIntegratedRiskManagement(self, portfolio: Portfolio, alpha: float, beta: float, minimumReturn: float) -> tuple:
        if not self.memoryIRM:
            self.saveMemoryIRM(portfolio=portfolio, alpha=alpha, beta=beta)

        self.b_ub[0] = -minimumReturn

        solution = opt.linprog(
            c=self.cost, 
            A_ub=self.A_ub, 
            b_ub=self.b_ub, 
            A_eq=self.A_eq, 
            b_eq=self.b_eq, 
            bounds=self.bounds, 
            method="highs"
        )

        if not solution.success:
            return self.d*[None], None
        
        return solution.x[:self.d], solution.fun