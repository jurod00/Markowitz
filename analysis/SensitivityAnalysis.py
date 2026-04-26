import numpy as np

from mathematics.financialMathematics import FinancialMathematics as FiMa

class SensitivityAnalysis:
    def __init__(self):
        self.alphaDefault = 0.95
        self.gammaDefault = 0.5
        self.myDefault = 0.25 # 0.07

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
    
    def meanObjectiveScatterData(self, portfolio, allocations, alpha, gamma):
        my, obj = [], []
        
        for allocation in allocations:
            myTemp = FiMa.mean(
                time=portfolio.getTime(), 
                stocks=portfolio.getStocks(), 
                allocation=allocation
            )
            my.append(myTemp)

            AVaR = FiMa.averageValueAtRisk(
                time=portfolio.getTime(), 
                stocks=portfolio.getStocks(), 
                allocation=allocation, 
                alpha=alpha
            )

            if AVaR == None:
                objTemp = None
            else:
                objTemp = -(1-gamma)*myTemp + gamma*AVaR

            obj.append(objTemp)

        return my, obj

    # Relevante Methode
    def allocationsNoisy(self, portfolio, epsilon, model):
        allocations = []

        if model == "Markowitz":
            my = np.linspace(0, 0.3, num=int(3e+3))

            for m in my:
                stocksNoisy = self.addNormalNoise(portfolio.getStocks(), epsilon)
                x = FiMa.allocationBasic(portfolio.getTime(), stocksNoisy, m)
                allocations.append(x)
        elif model == "UtilityMaximization":
            kappa = np.linspace(1.5, 1000, num=int(3e+3))

            for k in kappa:
                stocksNoisy = self.addNormalNoise(portfolio.getStocks(), epsilon)
                x = FiMa.allocationUtilityMaximization(portfolio.getTime(), stocksNoisy, k)
                allocations.append(x)
        elif model == "LinearProgramming":
            my = np.linspace(0, 0.5, num=int(3e+3))

            for m in my:
                stocksNoisy = self.addNormalNoise(portfolio.getStocks(), epsilon)
                x = FiMa.allocationLinearProgramming(
                    time=portfolio.getTime(), 
                    stocks=stocksNoisy, 
                    alpha=self.alphaDefault, 
                    gamma=self.gammaDefault, 
                    minimumReturn=m
                )
                allocations.append(x)

        return allocations
    
    def sensitivity(self, portfolio, model, theta=-1):
        if model == "Markowitz":
            if theta == -1:
                _, b, c, d = FiMa.abcd(portfolio.getTime(), portfolio.getStocks())
                SIGMAinv = FiMa.precision(portfolio.getTime(), portfolio.getStocks())
                r = FiMa.expectedReturn(portfolio.getTime(), portfolio.getStocks())
                ones = np.ones(FiMa.numberStocks(portfolio.getStocks()))

                sensitivity = np.linalg.norm(c/d*SIGMAinv.dot(r) - b/d*SIGMAinv.dot(ones))
                return sensitivity
            else:
                pass # Delta x / Delta theta
        elif model == "UtilityMaximization":
            _, b, c, d = FiMa.abcd(portfolio.getTime(), portfolio.getStocks())
            SIGMAinv = FiMa.precision(portfolio.getTime(), portfolio.getStocks())
            r = FiMa.expectedReturn(portfolio.getTime(), portfolio.getStocks())
            ones = np.ones(FiMa.numberStocks(portfolio.getStocks()))

            sensitivity = np.linalg.norm((b/c*SIGMAinv.dot(ones) - SIGMAinv.dot(r))/theta**2)
            return sensitivity
        elif model == "LinearProgramming":
            pass

    def elasticity(self, portfolio, method, theta=-1):
        if method == "markowitz":
            if theta == -1:
                pass
            else:
                pass # (Delta x / x) / (Delta theta / theta)
        elif method == "utilityMaximization":
            pass
        elif method == "linearProgramming":
            pass

    def sensitivityNew(self, model, parameter, portfolio, theta) -> float:
        # Delta x / Delta theta

        time = portfolio.getTime()
        stocks = portfolio.getStocks()

        h = float(1e-2)

        if model == "Markowitz":
            if parameter == "my":
                x1 = FiMa.allocationBasic(time=time, stocks=stocks, minimumReturn=theta)
                x2 = FiMa.allocationBasic(time=time, stocks=stocks, minimumReturn=theta+h)

                sensitivity = np.linalg.norm(x2-x1)/h
                return sensitivity
            else:
                print("Parameter \"" + parameter + "\" in model \"" + model + "\" not available!")
        elif model == "UtilityMaximization":
            if parameter == "kappa":
                x1 = FiMa.allocationUtilityMaximization(time=time, stocks=stocks, kappa=theta)
                x2 = FiMa.allocationUtilityMaximization(time=time, stocks=stocks, kappa=theta+h)

                sensitivity = np.linalg.norm(x2-x1)/h
                return sensitivity
            else:
                print("Parameter \"" + parameter + "\" in model \"" + model + "\" not available!")
        elif model == "LinearProgramming":
            if parameter == "alpha":
                x1 = FiMa.allocationLinearProgramming(time=time, stocks=stocks, alpha=theta, gamma=self.gammaDefault, minimumReturn=self.myDefault)
                x2 = FiMa.allocationLinearProgramming(time=time, stocks=stocks, alpha=theta+h, gamma=self.gammaDefault, minimumReturn=self.myDefault)

                sensitivity = np.linalg.norm(x2-x1)/h
                return sensitivity
            elif parameter == "gamma":
                x1 = FiMa.allocationLinearProgramming(time=time, stocks=stocks, alpha=self.alphaDefault, gamma=theta, minimumReturn=self.myDefault)
                x2 = FiMa.allocationLinearProgramming(time=time, stocks=stocks, alpha=self.alphaDefault, gamma=theta+h, minimumReturn=self.myDefault)

                sensitivity = np.linalg.norm(x2-x1)/h
                return sensitivity
            elif parameter == "my":
                x1 = FiMa.allocationLinearProgramming(time=time, stocks=stocks, alpha=self.alphaDefault, gamma=self.gammaDefault, minimumReturn=theta)
                x2 = FiMa.allocationLinearProgramming(time=time, stocks=stocks, alpha=self.alphaDefault, gamma=self.gammaDefault, minimumReturn=theta+h)

                if None in x1 or None in x2:
                    return None

                sensitivity = np.linalg.norm(x2-x1)/h
                return sensitivity
            else:
                print("Parameter \"" + parameter + "\" in model \"" + model + "\" not available!")