from mathematics.covariance import Covariance
from mathematics.returns import Returns
from mathematics.minimization import Minimization
from portfolio.portfolio import Portfolio
from util.util import Util

import numpy as np
import scipy.linalg as lina

from scipy.optimize import linprog
from scipy.optimize import minimize

class Allocations:

    def __init__(self, returns: Returns=None, covariance: Covariance=None, minimization: Minimization=None):
        # Optional Dependency Injection
        self.returns = returns if returns is not None else Returns()
        self.covariance = covariance if covariance is not None else Covariance()
        self.minimization = minimization if minimization is not None else Minimization()
        # Memory flag
        self.memorizedIRM: bool=False
        self.memorizedTwoFund: bool=False
        self.memorizedInteriorPoint: bool=False
        self.memorizedDefault: bool=False

    # ------------------------------------------------------------------------------------------------------------------------------------------------------------
    #                                                                           Cache
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------

    def cacheIRM(self, portfolio: Portfolio, alpha: float, beta: float) -> None:
        self.d = len(portfolio.stocks) + len(portfolio.indicesCall) + len(portfolio.indicesPut)
        self.n = len(portfolio.times) - 1

        prob = np.array(Util.prob(times=portfolio.times))
        r = self.returns.expectedReturn(portfolio=portfolio)
        print(r)

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

    def cacheTwoFund(self, portfolio: Portfolio) -> None:
        d = len(portfolio.stocks) + len(portfolio.indicesCall) + len(portfolio.indicesPut)
        r = self.returns.expectedReturn(portfolio=portfolio)

        ones = np.ones(d)
        sigma = self.covariance.covariance(portfolio=portfolio)

        precisionR = np.linalg.solve(sigma, r)
        precisionOnes = np.linalg.solve(sigma, ones)

        a = r.dot(precisionR)
        b = r.dot(precisionOnes)
        c = ones.dot(precisionOnes)
        det = a*c - b**2

        self.slopeVector = c/det*precisionR - b/det*precisionOnes
        self.shiftVector = a/det*precisionOnes - b/det*precisionR

    def cacheInteriorPoint(self, portfolio: Portfolio) -> None:
        d = len(portfolio.stocks) + len(portfolio.indicesCall) + len(portfolio.indicesPut)
        r = self.returns.expectedReturn(portfolio=portfolio)

        ones = np.ones(d)
        sigma = self.covariance.covariance(portfolio=portfolio)

        self.Q = sigma
        self.A = np.block([[r], [ones]])
        self.c = np.zeros(d)

    def cacheDefault(self, portfolio: Portfolio) -> None:
        self.d = len(portfolio.stocks) + len(portfolio.indicesCall) + len(portfolio.indicesPut)
        self.r = self.returns.expectedReturn(portfolio=portfolio)
        self.sigma = self.covariance.covariance(portfolio=portfolio)

    # ------------------------------------------------------------------------------------------------------------------------------------------------------------
    #                                                                           Allocation
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------

    def allocationIntegratedRiskManagement(self, portfolio: Portfolio, alpha: float, beta: float, minimumReturn: float) -> tuple:
        if not self.memorizedIRM:
            self.cacheIRM(portfolio=portfolio, alpha=alpha, beta=beta)
            self.memorizedIRM = True
    
        self.b_ub[0] = -minimumReturn
    
        solution = linprog(
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

    def allocationMarkowitz(self, portfolio: Portfolio, minimumReturn: float, shortSellingAllowed: bool=True, method: str="default") -> np.ndarray:

        if shortSellingAllowed and method == "twoFund":
            if not self.memorizedTwoFund:
                self.cacheTwoFund(portfolio=portfolio)
                self.memorizedTwoFund = True

            return minimumReturn*self.slopeVector + self.shiftVector

        elif not shortSellingAllowed and method == "interiorPoint":
            if not self.memorizedInteriorPoint:
                self.cacheInteriorPoint(portfolio=portfolio)
                self.memorizedInteriorPoint = True

            x = self.minimization.quadraticProgramming(Q=self.Q, A=self.A, b=np.array([minimumReturn, 1]), c=self.c)
            return x

        elif method == "default":
            if not self.memorizedDefault:
                self.cacheDefault(portfolio=portfolio)
                self.memorizedDefault = True

            def fun(x: np.ndarray) -> float:
                return x.T @ self.sigma @ x

            if not shortSellingAllowed:
                bounds = self.d*[(0, None)]
            else:
                bounds = self.d*[(None, None)]

            constraints = [
                {'type': 'eq', 'fun': lambda x: x.T @ self.r - minimumReturn}, 
                {'type': 'eq', 'fun': lambda x: sum(x) - 1}
            ]

            result = minimize(fun=fun, x0=np.ones(self.d)/self.d, method="SLSQP", bounds=bounds, constraints=constraints)
            return result.x

        return None

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

        result = minimize(fun=fun, x0=x0, bounds=bounds, constraints=constraints)
        return result.x