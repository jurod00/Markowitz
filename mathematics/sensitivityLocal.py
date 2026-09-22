from mathematics.allocations import Allocations
from portfolio.portfolio import Portfolio

import math
import numpy as np

class SensitivityLocal:

    def __init__(self, allocations: Allocations=None):
        # Optional Dependency Injection
        self.allocations = allocations if allocations is not None else Allocations()
        # Step size
        self.h = float(1e-3)

    def minimumReturnMARKOWITZ(self, portfolio: Portfolio, minimumReturn: float, shortSellingAllowed: bool, method: str):
        allocationLeft = self.allocations.allocationMarkowitz(portfolio=portfolio, minimumReturn=minimumReturn-self.h, shortSellingAllowed=shortSellingAllowed, method=method)
        allocationRight = self.allocations.allocationMarkowitz(portfolio=portfolio, minimumReturn=minimumReturn+self.h, shortSellingAllowed=shortSellingAllowed, method=method)

        return (allocationRight - allocationLeft)/(2*self.h)

    def minimumReturnIRM(self, portfolio: Portfolio, alpha: float, beta: float, minimumReturn: float, shortSellingAllowed: bool=False, method: str="default"):
        allocationLeft, _ = self.allocations.allocationIntegratedRiskManagement(portfolio=portfolio, alpha=alpha, beta=beta, minimumReturn=minimumReturn-self.h, shortSellingAllowed=shortSellingAllowed, method=method)
        allocationRight, _ = self.allocations.allocationIntegratedRiskManagement(portfolio=portfolio, alpha=alpha, beta=beta, minimumReturn=minimumReturn+self.h, shortSellingAllowed=shortSellingAllowed, method=method)

        return (allocationRight - allocationLeft)/(2*self.h)

    def stockMARKOWITZ(self, h: float, portfolio: Portfolio, minimumReturn: float, shortSellingAllowed: bool, method: str):
        portfolioLeft = portfolio
        portfolioRight = portfolio

        d = len(portfolio.stocks)
        n = len(portfolio.stocks[0])

        direction = np.ones((d, n))

        stocksLeft = []
        stocksRight = []

        stockLeft = []
        stockRight = []

        for j in range(d):
            for i in range(n):
                stockLeft.append(portfolio.stocks[j][i]*math.exp(-h*direction[j,i]))
                stockRight.append(portfolio.stocks[j][i]*math.exp(h*direction[j,i]))
                
            stocksLeft.append(stockLeft)
            stocksRight.append(stockRight)

        portfolioLeft.setStocks(stocksLeft)
        portfolioRight.setStocks(stocksRight)

        allocationLeft = self.allocations.allocationMarkowitz(portfolio=portfolioLeft, minimumReturn=minimumReturn, shortSellingAllowed=shortSellingAllowed, method=method)
        allocationRight = self.allocations.allocationMarkowitz(portfolio=portfolioRight, minimumReturn=minimumReturn, shortSellingAllowed=shortSellingAllowed, method=method)

        return (allocationRight - allocationLeft)/2*h
    
    def stockIRM(self):
        pass

    def alphaIRM(self, portfolio: Portfolio, alpha: float, beta: float, minimumReturn: float, shortSellingAllowed: bool=False, method: str="default"):
        h = 0.01

        allocationLeft, _ = self.allocations.allocationIntegratedRiskManagement(portfolio=portfolio, alpha=alpha-h, beta=beta, minimumReturn=minimumReturn, shortSellingAllowed=shortSellingAllowed, method=method, useCache=False)
        allocationRight, _ = self.allocations.allocationIntegratedRiskManagement(portfolio=portfolio, alpha=alpha+h, beta=beta, minimumReturn=minimumReturn, shortSellingAllowed=shortSellingAllowed, method=method, useCache=False)
        
        return (allocationRight - allocationLeft)/(2*self.h)

    def betaIRM(self, portfolio: Portfolio, alpha: float, beta: float, minimumReturn: float, shortSellingAllowed: bool=False, method: str="default"):
        h = 0.01

        allocationLeft, _ = self.allocations.allocationIntegratedRiskManagement(portfolio=portfolio, alpha=alpha, beta=beta-h, minimumReturn=minimumReturn, shortSellingAllowed=shortSellingAllowed, method=method, useCache=False)
        allocationRight, _ = self.allocations.allocationIntegratedRiskManagement(portfolio=portfolio, alpha=alpha, beta=beta+h, minimumReturn=minimumReturn, shortSellingAllowed=shortSellingAllowed, method=method, useCache=False)

        return (allocationRight - allocationLeft)/(2*self.h)