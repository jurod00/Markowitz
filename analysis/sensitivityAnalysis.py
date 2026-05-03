import numpy as np

from mathematics.financialMathematics import FinancialMathematics as FiMa

class SensitivityAnalysis:
    def __init__(self):
        pass

    alphaDefault = 0.95
    gammaDefault = 0.5
    myDefault = 0.25 # 0.07
    
    @staticmethod
    def setSeed(s) -> None:
        np.random.seed(s)

    @staticmethod
    def addUniformNoise(stocks, epsilon):
        n = len(stocks[0])

        stocksNoisy = []
        for stock in stocks:
            noise = stock[0]*epsilon*np.random.uniform(0, 1, n)
            stocksNoisy.append(list(stock + noise))

        return stocksNoisy
    
    @staticmethod
    def addNormalNoise(stocks, epsilon):
        n = len(stocks[0])

        stocksNoisy = []
        for stock in stocks:
            noise = stock[0]*epsilon*np.random.normal(0, 1, n)
            stocksNoisy.append(list(stock + noise))
        
        return stocksNoisy
    
    @staticmethod
    def meanVarianceScatterData(portfolio, allocations):
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
    
    @staticmethod
    def meanObjectiveScatterData(portfolio, allocations, alpha, gamma):
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

    @staticmethod
    def allocationsNoisy(portfolio, epsilon, model):
        allocations = []

        if model == "Markowitz":
            my = np.linspace(0, 0.3, num=int(3e+3))

            for m in my:
                stocksNoisy = SeAn.addNormalNoise(portfolio.getStocks(), epsilon)
                x = FiMa.allocationBasic(portfolio.getTime(), stocksNoisy, m)
                allocations.append(x)
        elif model == "UtilityMaximization":
            kappa = np.linspace(1.5, 1000, num=int(3e+3))

            for k in kappa:
                stocksNoisy = SeAn.addNormalNoise(portfolio.getStocks(), epsilon)
                x = FiMa.allocationUtilityMaximization(portfolio.getTime(), stocksNoisy, k)
                allocations.append(x)
        elif model == "LinearProgramming":
            my = np.linspace(0, 0.5, num=int(3e+3))

            for m in my:
                stocksNoisy = SeAn.addNormalNoise(portfolio.getStocks(), epsilon)
                x = FiMa.allocationLinearProgramming(
                    time=portfolio.getTime(), 
                    stocks=stocksNoisy, 
                    alpha=SeAn.alphaDefault, 
                    gamma=SeAn.gammaDefault, 
                    minimumReturn=m
                )
                allocations.append(x)

        return allocations

    @staticmethod
    def sensitivityNew(model, parameter, portfolio, theta) -> float:
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
                x1 = FiMa.allocationLinearProgramming(time=time, stocks=stocks, alpha=theta, gamma=SeAn.gammaDefault, minimumReturn=SeAn.myDefault)
                x2 = FiMa.allocationLinearProgramming(time=time, stocks=stocks, alpha=theta+h, gamma=SeAn.gammaDefault, minimumReturn=SeAn.myDefault)

                sensitivity = np.linalg.norm(x2-x1)/h
                return sensitivity
            elif parameter == "gamma":
                x1 = FiMa.allocationLinearProgramming(time=time, stocks=stocks, alpha=SeAn.alphaDefault, gamma=theta, minimumReturn=SeAn.myDefault)
                x2 = FiMa.allocationLinearProgramming(time=time, stocks=stocks, alpha=SeAn.alphaDefault, gamma=theta+h, minimumReturn=SeAn.myDefault)

                sensitivity = np.linalg.norm(x2-x1)/h
                return sensitivity
            elif parameter == "my":
                x1 = FiMa.allocationLinearProgramming(time=time, stocks=stocks, alpha=SeAn.alphaDefault, gamma=SeAn.gammaDefault, minimumReturn=theta)
                x2 = FiMa.allocationLinearProgramming(time=time, stocks=stocks, alpha=SeAn.alphaDefault, gamma=SeAn.gammaDefault, minimumReturn=theta+h)

                if None in x1 or None in x2:
                    return None

                sensitivity = np.linalg.norm(x2-x1)/h
                return sensitivity
            else:
                print("Parameter \"" + parameter + "\" in model \"" + model + "\" not available!")

SeAn = SensitivityAnalysis