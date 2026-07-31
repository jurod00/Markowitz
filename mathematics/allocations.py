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

        precisionR = lina.solve(self.sigma, self.r)
        precisionOnes = lina.solve(self.sigma, self.ones)

        self.a = self.r.dot(precisionR)
        self.b = self.r.dot(precisionOnes)
        self.c = self.ones.dot(precisionOnes)
        det = self.a*self.c - self.b**2

        self.slopeVector = self.c/det*precisionR - self.b/det*precisionOnes
        self.shiftVector = self.a/det*precisionOnes - self.b/det*precisionR

        A = np.empty((self.d+2, self.d+2))
        A[0, 0] = self.a
        A[0, 1] = self.b
        A[0, 2:] = precisionR
        A[1, 0] = self.b
        A[1, 1] = self.c
        A[1, 2:] = precisionOnes
        A[2:, 0] = precisionR
        A[2:, 1] = precisionOnes
        A[2:, 2:] = self.covariance.precision(portfolio=portfolio)

        self.lu, self.piv = lina.lu_factor(A)

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

    def allocationMarkowitz(self, portfolio: Portfolio, minimumReturn: float, shortSellingAllowed: bool=True, method: str="") -> np.ndarray:
        if not self.memoryMarkowitz:
            self.saveMemoryMarkowitz(portfolio=portfolio)

        if method == "lecture": # depricated
            return minimumReturn*self.slopeVector + self.shiftVector

        if method == "LU": # depricated
            pass

        def fun(x: np.ndarray) -> float:
            return x.dot(self.sigma.dot(x))

        x0 = np.ones(self.d)/self.d

        if not shortSellingAllowed:
            bounds = self.d*[(0, None)]
        else:
            bounds = self.d*[(None, None)]

        constraints = [
            {'type': 'ineq', 'fun': lambda x: x @ self.r - minimumReturn}, 
            {'type': 'eq',   'fun': lambda x: sum(x) - 1}
        ]

        result = opt.minimize(fun=fun, x0=x0, method="SLSQP", bounds=bounds, constraints=constraints)
        return result.x

    def allocationUtilityMaximization(self, portfolio: Portfolio, riskAversion: float, shortSellingAllowed: bool=True, method: str="") -> np.ndarray:
        if not self.memoryMarkowitz:
            self.saveMemoryMarkowitz(portfolio=portfolio)

        if method == "lecture": # depricated
            return 1/riskAversion*lina.solve(self.sigma, self.r + (riskAversion-self.b)/self.c*self.ones)

        def fun(x: np.ndarray) -> float:
            return 0.5*riskAversion*x.dot(self.sigma.dot(x)) - x.dot(self.r)

        x0 = np.ones(self.d)/self.d

        if not shortSellingAllowed:
            bounds = self.d*[(0, None)]
        else:
            bounds = self.d*[(None, None)]
        
        constraints = [{'type': 'eq', 'fun': lambda x: sum(x) - 1}]

        result = opt.minimize(fun=fun, x0=x0, bounds=bounds, constraints=constraints)
        return result.x

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