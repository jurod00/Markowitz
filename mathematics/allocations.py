import numpy as np
import scipy.optimize as opt

from mathematics.returns import Returns
from mathematics.stochastics import Stochastics
from portfolio.portfolio import Portfolio
from util.time import Time

class Allocations:

    def __init__(self):
        pass

    @staticmethod
    def allocationMarkowitz(portfolio: Portfolio, minimumReturn: float):
        d = len(portfolio.stocks) + len(portfolio.indicesCall) + len(portfolio.indicesPut)
        r = Stochastics.expectation(portfolio=portfolio)
        prec = Stochastics.precision(portfolio=portfolio)
        ones = np.ones(d)

        a = r.dot(prec.dot(r))
        b = r.dot(prec.dot(ones))
        c = ones.dot(prec.dot(ones))
        d = a*c - b**2

        slopeVector = c/d*prec.dot(r) - b/d*prec.dot(ones)
        shiftVector = a/d*prec.dot(ones) - b/d*prec.dot(r)

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
        
        prob = Time.prob(times=portfolio.times)
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