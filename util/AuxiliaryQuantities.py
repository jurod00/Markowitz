import numpy as np
import datetime as dt

class AuxiliaryQuantities:

    def __init__(self):
        pass

    def duration(self, time: list):
        return time[-1] - time[0]
    
    def numberTimestamps(self, time: list):
        n = len(time) - 1
        return n
    
    def numberStocks(self, stocks: list):
        J = len(stocks)
        return J

    def prob(self, time: list):
        duration = self.duration(time)
        n = self.numberTimestamps(time)

        prob = np.empty(n)
        for i in range(n):
            prob[i] = (time[i+1] - time[i]) / duration
        
        return prob
    
    def annualizedReturn(self, time: list, stocks: list):
        n = self.numberTimestamps(time)
        J = self.numberStocks(stocks)
        prob = self.prob(time)

        XI = np.empty((n,J))
        for i in range(n):
            for j in range(J):
                XI[i,j] = np.log(stocks[j][i+1]/stocks[j][i])/prob[i]

        return XI
    
    def expectedReturn(self, time: list, stocks: list):
        prob = self.prob(time)
        XI = self.annualizedReturn(time, stocks)

        r = np.matmul(prob, XI)
        return r
    
    def covariance(self, time: list, stocks: list):
        prob = self.prob(time)
        XI = self.annualizedReturn(time, stocks)
        r = self.expectedReturn(time, stocks)
        D = np.diag(prob)
        
        SIGMA = XI.transpose().dot(D.dot(XI)) - np.outer(r, r)
        return SIGMA
    
    def precision(self, time: list, stocks: list):
        SIGMA = self.covariance(time, stocks)

        SIGMAinv = np.linalg.inv(SIGMA)
        return SIGMAinv
    
    def allocationBasic(self, time: list, stocks: list, minimumReturn: float):
        r = self.expectedReturn(time, stocks)
        SIGMAinv = self.precision(time, stocks)
        ones = np.ones(self.numberStocks(stocks))

        a = r.dot(SIGMAinv.dot(r))
        b = r.dot(SIGMAinv.dot(ones))
        c = ones.dot(SIGMAinv.dot(ones))
        d = a*c - b**2

        slopeVector = c/d*SIGMAinv.dot(r) - b/d*SIGMAinv.dot(ones)
        shiftVector = a/d*SIGMAinv.dot(ones) - b/d*SIGMAinv.dot(r)
        
        x = minimumReturn*slopeVector + shiftVector
        return x