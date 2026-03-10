import numpy as np
import scipy.optimize as opt

class FinancialMathematics:
    
    def __init__(self):
        pass
    
    alpha = 0.95
    gamma = 0.5

    @staticmethod
    def duration(time: list):
        return time[-1] - time[0]
    
    @staticmethod
    def numberTimestamps(time: list):
        n = len(time) - 1
        return n
    
    @staticmethod
    def numberStocks(stocks: list):
        J = len(stocks)
        return J

    @staticmethod
    def prob(time: list):
        duration = FiMa.duration(time)
        n = FiMa.numberTimestamps(time)

        prob = np.empty(n)
        for i in range(n):
            prob[i] = (time[i+1] - time[i]) / duration
        
        return prob
    
    @staticmethod
    def annualizedReturn(time: list, stocks: list):
        n = FiMa.numberTimestamps(time)
        J = FiMa.numberStocks(stocks)
        prob = FiMa.prob(time)

        XI = np.empty((n,J))
        for i in range(n):
            for j in range(J):
                XI[i,j] = np.log(stocks[j][i+1]/stocks[j][i])/prob[i]

        return XI
    
    @staticmethod
    def expectedReturn(time: list, stocks: list):
        prob = FiMa.prob(time)
        XI = FiMa.annualizedReturn(time, stocks)

        r = np.matmul(prob, XI)
        return r
    
    @staticmethod
    def expectedReturnPercent(time: list, stocks: list):
        r = FiMa.expectedReturn(time, stocks)

        i = np.exp(r) - 1
        return i
    
    @staticmethod
    def covariance(time: list, stocks: list):
        prob = FiMa.prob(time)
        XI = FiMa.annualizedReturn(time, stocks)
        r = FiMa.expectedReturn(time, stocks)
        D = np.diag(prob)
        
        SIGMA = XI.transpose().dot(D.dot(XI)) - np.outer(r, r)
        return SIGMA
    
    @staticmethod
    def precision(time: list, stocks: list):
        SIGMA = FiMa.covariance(time, stocks)

        SIGMAinv = np.linalg.inv(SIGMA)
        return SIGMAinv
    
    @staticmethod
    def abcd(time:list, stocks: list):
        r = FiMa.expectedReturn(time, stocks)
        SIGMAinv = FiMa.precision(time, stocks)
        ones = np.ones(FiMa.numberStocks(stocks))

        a = r.dot(SIGMAinv.dot(r))
        b = r.dot(SIGMAinv.dot(ones))
        c = ones.dot(SIGMAinv.dot(ones))
        d = a*c - b**2

        return a, b, c, d
    
    @staticmethod
    def allocationBasic(time: list, stocks: list, minimumReturn: float, unit: str="log%"):
        r = FiMa.expectedReturn(time, stocks)
        SIGMAinv = FiMa.precision(time, stocks)
        ones = np.ones(FiMa.numberStocks(stocks))

        a = r.dot(SIGMAinv.dot(r))
        b = r.dot(SIGMAinv.dot(ones))
        c = ones.dot(SIGMAinv.dot(ones))
        d = a*c - b**2

        slopeVector = c/d*SIGMAinv.dot(r) - b/d*SIGMAinv.dot(ones)
        shiftVector = a/d*SIGMAinv.dot(ones) - b/d*SIGMAinv.dot(r)

        if unit == "%":
            i = minimumReturn
            my = np.log(1+i)
        else:
            my = minimumReturn
        
        x = my*slopeVector + shiftVector
        return x
    
    @staticmethod
    def mean(time: list, stocks: list, allocation):
        # Methode gibt Erwartungswert = Return = Nebenbedingung zu gegebener Allocation zurück
        r = FiMa.expectedReturn(time, stocks)
        x = allocation

        my = r.dot(x)
        return my

    @staticmethod
    def variance(time: list, stocks: list, allocation):
        # Methode gibt Varianz = Risiko = Objective zu gegebener Allocation zurück
        SIGMA = FiMa.covariance(time, stocks)
        x = allocation

        var = x.dot(SIGMA.dot(x))
        return var
    
    @staticmethod
    def averageValueAtRisk(time: list, stocks: list, allocation, alpha):
        n = FiMa.numberTimestamps(time)
        p = FiMa.prob(time)
        XI = FiMa.annualizedReturn(time, stocks)

        c = np.empty(n+1)
        c[0] = 1
        c[1:] = 1/(1-alpha)*p

        A_ub = np.empty((n, n+1))
        for i in range(n):
            A_ub[i, 0] = -1
            A_ub[i,1:] = 0
            A_ub[i,1+i] = -1

        b_ub = np.empty(n)
        for i in range(n):
            b_ub[i] = allocation.dot(XI[i,:])

        bounds = []
        bounds.append((None, None))
        for _ in range(n):
            bounds.append((0, None))

        solution = opt.linprog(
            c=c, 
            A_ub=A_ub, 
            b_ub=b_ub, 
            bounds=bounds, 
            method="highs"
        )
        AVaR = solution.fun
        return AVaR
    
    @staticmethod
    def allocationUtilityMaximization(time: list, stocks: list, kappa: float):
        r = FiMa.expectedReturn(time, stocks)
        SIGMAinv = FiMa.precision(time, stocks)
        ones = np.ones(FiMa.numberStocks(stocks))
        
        x = 1/kappa*np.matmul(SIGMAinv, r + (kappa - ones.dot(SIGMAinv.dot(r)))/ones.dot(SIGMAinv.dot(ones))*ones)
        return x
    
    @staticmethod
    def objectiveCostVector(time: list, stocks: list):
        n = FiMa.numberTimestamps(time)
        J = FiMa.numberStocks(stocks)
        p = FiMa.prob(time)
        r = FiMa.expectedReturn(time, stocks)

        c = np.empty(J+n+1)
        c[:J] = FiMa.gamma*r
        c[J] = FiMa.gamma
        c[J+1:] = FiMa.gamma/(1-FiMa.alpha)*p

        return c
    
    @staticmethod
    def constraintsInequality(time: list, stocks: list, my: float, leftRight: str):
        n = FiMa.numberTimestamps(time)
        J = FiMa.numberStocks(stocks)

        if leftRight == "left":
            r = FiMa.expectedReturn(time, stocks)
            XI = FiMa.annualizedReturn(time, stocks)

            A = np.empty((n+1, J+n+1))
            A[0,:J] = -r
            A[0,J:] = 0

            for i in range(n):
                A[i+1,:J] = -XI[i,:]
                A[i+1, J] = -1
                A[i+1,J+1:] = 0
                A[i+1,J+1+i] = -1

            return A

        elif leftRight == "right":
            b = np.empty(n+1)
            b[0] = -my
            b[1] = 0 # Todo: Fehler
            b[2:] = 0

            return b
        
    @staticmethod
    def constraintsEquality(time: list, stocks: list, leftRight: str):
        n = FiMa.numberTimestamps(time)
        J = FiMa.numberStocks(stocks)

        if leftRight == "left":
            A = np.empty((1, J+n+1))
            A[0,:J] = 1
            A[0,J:] = 0

            return A
        
        if leftRight == "right":
            b = np.empty(1)
            b[0] = 1

            return b

    @staticmethod
    def constraintsBounds(time: list, stocks: list):
        n = FiMa.numberTimestamps(time)
        J = FiMa.numberStocks(stocks)

        bounds = []

        for _ in range(J):
            bounds.append((None, None))

        bounds.append((None, None))

        for _ in range(n):
            bounds.append((0, None))

        return bounds
    
    @staticmethod
    def allocationLinearProgramming(time: list, stocks: list, minimumReturn: float):
        alpha = 0.95
        gamma = 0.5
        c = FiMa.objectiveCostVector(time, stocks)
        bounds = FiMa.constraintsBounds(time, stocks)

        my = minimumReturn

        J = FiMa.numberStocks(stocks)
        A_ub = FiMa.constraintsInequality(time, stocks, my, "left")
        A_eq = FiMa.constraintsEquality(time, stocks, "left")

        b_ub = FiMa.constraintsInequality(time, stocks, my, "right")
        b_eq = FiMa.constraintsEquality(time, stocks, "right")

        solution = opt.linprog(
            c=c, 
            A_ub=A_ub, 
            b_ub=b_ub, 
            A_eq=A_eq, 
            b_eq=b_eq, 
            bounds=bounds, 
            method="highs"
        )
            
        x = solution.x[:J]
        return x
    
    @staticmethod
    def objectiveLinearProgramming(time: list, stocks: list, minimumReturn: float):
        alpha = 0.95
        gamma = 0.5
        c = FiMa.objectiveCostVector(time, stocks)
        bounds = FiMa.constraintsBounds(time, stocks)

        my = minimumReturn

        A_ub = FiMa.constraintsInequality(time, stocks, my, "left")
        A_eq = FiMa.constraintsEquality(time, stocks, "left")

        b_ub = FiMa.constraintsInequality(time, stocks, my, "right")
        b_eq = FiMa.constraintsEquality(time, stocks, "right")

        solution = opt.linprog(
            c=c, 
            A_ub=A_ub, 
            b_ub=b_ub, 
            A_eq=A_eq, 
            b_eq=b_eq, 
            bounds=bounds, 
            method="highs"
        )
            
        #obj = solution.fun/gamma
        obj = solution.fun
        return obj
    
FiMa = FinancialMathematics