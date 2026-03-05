import numpy as np

from portfolio import FinancialMathematics as FiMa

class SensitivityAnalysis:
    def __init__(self):
        pass

    def conditionNumber(self, Sigma):
        return np.linalg.cond(Sigma)
    
    def setSeed(self, s) -> None:
        np.random.seed(s)

    def addUniformNoise(self, stocks, epsilon):
        n = len(stocks[0])

        stocksNoisy = []
        for stock in stocks:
            noise = stock[0]*epsilon*np.random.uniform(0, 1, n)
            stocksNoisy.append(list(stock + noise))

        return stocksNoisy
    
    def addNormalNoise(self, stocks, epsilon):
        n = len(stocks[0])

        stocksNoisy = []
        for stock in stocks:
            noise = stock[0]*epsilon*np.random.normal(0, 1, n)
            stocksNoisy.append(list(stock + noise))
        
        return stocksNoisy

    def err(self, x, y):
        difference = np.array(x) - np.array(y)
        return np.linalg.norm(difference)
    
    def meanVarianceScatterData(self, portfolio, allocations):
        my, sigma = [], []

        for allocation in allocations:
            myTemp = FiMa.mean(
                time=portfolio.getTime(), 
                stocks=portfolio.getStocks(), 
                allocation=allocation
            )
            my.append(myTemp)

            sigmaTemp = np.sqrt(FiMa.variance(
                time=portfolio.getTime(), 
                stocks=portfolio.getStocks(), 
                allocation=allocation
            ))
            sigma.append(sigmaTemp)
        
        return my, sigma
    
    def allocationsNoisy(self, portfolio, epsilon, method):
        allocations = []

        if method == "markowitz":
            my = np.linspace(0, 0.3, num=int(3e+3))

            for m in my:
                stocksNoisy = self.addNormalNoise(portfolio.getStocks(), epsilon)
                x = FiMa.allocationBasic(portfolio.getTime(), stocksNoisy, m)
                allocations.append(x)
        elif method == "utilityMaximization":
            kappa = np.linspace(1.5, 1000, num=int(3e+3))

            for k in kappa:
                stocksNoisy = self.addNormalNoise(portfolio.getStocks(), epsilon)
                x = FiMa.allocationUtilityMaximization(portfolio.getTime(), stocksNoisy, k)
                allocations.append(x)
        elif method == "linearProgramming":
            my = np.linspace(0, 0.3, num=int(3e+3))

            for m in my:
                stocksNoisy = self.addNormalNoise(portfolio.getStocks(), epsilon)
                x = FiMa.allocationLinearProgramming(portfolio.getTime(), stocksNoisy, m)
                allocations.append(x)

        return allocations