import math
import numpy as np
import datetime as dt
import scipy.stats as st
import scipy.optimize as opt

np.set_printoptions(threshold=np.inf)
np.set_printoptions(linewidth=np.inf)

class FinancialMathematics:
    
    def __init__(self):
        pass

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
    def annualizedReturn(time: list, stocks: list, options: dict=None):
        n = FiMa.numberTimestamps(time)
        J = FiMa.numberStocks(stocks)
        prob = FiMa.prob(time)

        # XI = np.empty((n,J))
        # for i in range(n):
        #     for j in range(J):
        #         XI[i,j] = np.log(stocks[j][i+1]/stocks[j][i])/prob[i]

        XI = np.empty((n,J))
        for i in range(n):
            for j in range(J):
                XI[i,j] = ((stocks[j][i+1] - stocks[j][i])/stocks[j][i])/prob[i]

        # XI = np.empty((n,J))
        # for i in range(n):
        #     for j in range(J):
        #         XI[i,j] = (stocks[j][i+1]/stocks[j][i] - 1)/prob[i]

        # XI = np.empty((n,J))
        # for i in range(n):
        #     for j in range(J):
        #         XI[i,j] = (stocks[j][i+1]-stocks[j][i])/prob[i]

        if options == None:
            return XI
        
        XIcall, XIput = FiMa.annualizedReturnOptions(time, stocks, options)

        XIoptions = np.hstack((XI, XIcall, XIput))
        return XIoptions
    
    @staticmethod
    def annualizedReturnOptions(time: list, stocks: list, options: dict):
        n = FiMa.numberTimestamps(time)
        prob = FiMa.prob(time)

        Jcall = len(options["callIndices"])
        XIcall = np.empty((n, Jcall))

        for jCall, j in enumerate(options["callIndices"]):
            for i in range(n):
                tau = (time[-1]-time[i]).days

                delta, _ = FiMa.delta(
                    daysToMaturity=tau, 
                    stockPrice=stocks[j][i], 
                    strikePrice=options["callStrikes"][jCall], 
                    volatility=options["callVolatilities"][jCall], 
                    riskFreeRate=options["riskFreeRate"]
                )
                gamma = FiMa.gamma(
                    daysToMaturity=tau, 
                    stockPrice=stocks[j][i], 
                    strikePrice=options["callStrikes"][jCall], 
                    volatility=options["callVolatilities"][jCall], 
                    riskFreeRate=options["riskFreeRate"]
                )
                theta, _ = FiMa.theta(
                    daysToMaturity=tau, 
                    stockPrice=stocks[j][i], 
                    strikePrice=options["callStrikes"][jCall], 
                    volatility=options["callVolatilities"][jCall], 
                    riskFreeRate=options["riskFreeRate"]
                )
                priceCall, _ = FiMa.priceOption(
                    daysToMaturity=tau, 
                    stockPrice=stocks[j][i],
                    strikePrice=options["callStrikes"][jCall],
                    volatility=options["callVolatilities"][jCall],
                    riskFreeRate=options["riskFreeRate"]
                )
                deltaS = stocks[j][i+1] - stocks[j][i]
                deltaT = prob[i]
                deltaT = (time[i+1]-time[i])/dt.timedelta(days=365)

                deltaC = delta*deltaS + 0.5*gamma*deltaS**2 + theta*deltaT
                XIcall[i, jCall] = deltaC/priceCall/prob[i]


        Jput = len(options["putIndices"])
        XIput = np.empty((n, Jput))

        for jPut, j in enumerate(options["putIndices"]):
            for i in range(n):
                tau = (time[-1]-time[i]).days

                _, delta = FiMa.delta(
                    daysToMaturity=tau, 
                    stockPrice=stocks[j][i], 
                    strikePrice=options["putStrikes"][jPut], 
                    volatility=options["putVolatilities"][jPut], 
                    riskFreeRate=options["riskFreeRate"]
                )
                gamma = FiMa.gamma(
                    daysToMaturity=tau, 
                    stockPrice=stocks[j][i], 
                    strikePrice=options["putStrikes"][jPut], 
                    volatility=options["putVolatilities"][jPut], 
                    riskFreeRate=options["riskFreeRate"]
                )
                _, theta = FiMa.theta(
                    daysToMaturity=tau, 
                    stockPrice=stocks[j][i], 
                    strikePrice=options["putStrikes"][jPut], 
                    volatility=options["putVolatilities"][jPut], 
                    riskFreeRate=options["riskFreeRate"]
                )

                _, pricePut = FiMa.priceOption(
                    daysToMaturity=tau, 
                    stockPrice=stocks[j][i],
                    strikePrice=options["putStrikes"][jPut],
                    volatility=options["putVolatilities"][jPut],
                    riskFreeRate=options["riskFreeRate"]
                )
                deltaS = stocks[j][i+1] - stocks[j][i]
                deltaT = prob[i]
                deltaT = (time[i+1]-time[i])/dt.timedelta(days=365)

                deltaP = delta*deltaS + 0.5*gamma*deltaS**2 + theta*deltaT
                XIput[i, jPut] = deltaP/pricePut/prob[i]

        return XIcall, XIput

    @staticmethod
    def expectedReturn(time: list, stocks: list, options: dict=None):
        prob = FiMa.prob(time)
        XI = FiMa.annualizedReturn(time, stocks, options)

        r = np.matmul(prob, XI)
        return r
    
    @staticmethod
    def covariance(time: list, stocks: list, options: dict=None):
        prob = FiMa.prob(time)
        XI = FiMa.annualizedReturn(time, stocks, options)
        r = FiMa.expectedReturn(time, stocks, options)
        D = np.diag(prob)
        
        SIGMA = XI.transpose().dot(D.dot(XI)) - np.outer(r, r)
        return SIGMA
    
    @staticmethod
    def precision(time: list, stocks: list, options: dict=None):
        SIGMA = FiMa.covariance(time, stocks, options)
        
        SIGMAinv = np.linalg.inv(SIGMA)
        return SIGMAinv
    
    @staticmethod
    def abcd(time:list, stocks: list, options: dict=None):
        r = FiMa.expectedReturn(time, stocks, options)
        SIGMAinv = FiMa.precision(time, stocks, options)

        J = FiMa.numberStocks(stocks)
        if options != None:
            Jcall = len(options["callIndices"])
            Jput = len(options["putIndices"])
        else:
            Jcall = 0
            Jput = 0

        ones = np.ones(J + Jcall + Jput)

        a = r.dot(SIGMAinv.dot(r))
        b = r.dot(SIGMAinv.dot(ones))
        c = ones.dot(SIGMAinv.dot(ones))
        d = a*c - b**2

        return a, b, c, d
    
    @staticmethod
    def allocationBasic(time: list, stocks: list, minimumReturn: float, options: dict=None, unit: str="log%"):
        r = FiMa.expectedReturn(time, stocks, options)
        SIGMAinv = FiMa.precision(time, stocks, options)
        
        J = FiMa.numberStocks(stocks)
        if options != None:
            Jcall = len(options["callIndices"])
            Jput = len(options["putIndices"])
        else:
            Jcall = 0
            Jput = 0

        ones = np.ones(J + Jcall + Jput)

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

        if None in x:
            return None

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
    def averageValueAtRisk(time: list, stocks: list, allocation: list, alpha: float):
        
        if None in allocation:
            return None
        
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
    def objectiveCostVector(time: list, stocks: list, alpha: float, gamma: float, options: dict=None):
        n = FiMa.numberTimestamps(time)

        J = FiMa.numberStocks(stocks)
        if options != None:
            J += len(options["callIndices"])
            J += len(options["putIndices"])

        p = FiMa.prob(time)
        r = FiMa.expectedReturn(time, stocks, options)

        c = np.empty(J+n+1)
        c[:J] = -(1-gamma)*r
        c[J] = gamma
        c[J+1:] = gamma/(1-alpha)*p

        return c
    
    @staticmethod
    def constraintsInequality(time: list, stocks: list, my: float, leftRight: str, options: dict=None):
        n = FiMa.numberTimestamps(time)

        J = FiMa.numberStocks(stocks)
        if options != None:
            J += len(options["callIndices"])
            J += len(options["putIndices"])

        if leftRight == "left":
            r = FiMa.expectedReturn(time, stocks, options)
            XI = FiMa.annualizedReturn(time, stocks, options)

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
            b[1:] = 0

            return b
        
    @staticmethod
    def constraintsEquality(time: list, stocks: list, leftRight: str, options: dict=None):
        n = FiMa.numberTimestamps(time)

        J = FiMa.numberStocks(stocks)
        if options != None:
            J += len(options["callIndices"])
            J += len(options["putIndices"])

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
    def constraintsBounds(time: list, stocks: list, options: dict=None):
        n = FiMa.numberTimestamps(time)

        J = FiMa.numberStocks(stocks)
        if options != None:
            J += len(options["callIndices"])
            J += len(options["putIndices"])

        bounds = []

        for _ in range(J):
            bounds.append((0, None))

        bounds.append((None, None))

        for _ in range(n):
            bounds.append((0, None))

        return bounds
    
    @staticmethod
    def allocationLinearProgramming(time: list, stocks: list, alpha: float, gamma: float, minimumReturn: float, options: dict=None):
        c = FiMa.objectiveCostVector(time, stocks, alpha, gamma, options)
        bounds = FiMa.constraintsBounds(time, stocks, options)

        my = minimumReturn

        J = FiMa.numberStocks(stocks)
        if options != None:
            J += len(options["callIndices"])
            J += len(options["putIndices"])

        A_ub = FiMa.constraintsInequality(time, stocks, my, "left", options)
        A_eq = FiMa.constraintsEquality(time, stocks, "left", options)

        b_ub = FiMa.constraintsInequality(time, stocks, my, "right", options)
        b_eq = FiMa.constraintsEquality(time, stocks, "right", options)

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
            return J*[None]
            
        x = solution.x[:J]
        return x
    
    @staticmethod
    def objectiveLinearProgramming(time: list, stocks: list, alpha: float, gamma: float, minimumReturn: float, options: dict=None):
        c = FiMa.objectiveCostVector(time, stocks, alpha, gamma, options)
        bounds = FiMa.constraintsBounds(time, stocks, options)

        my = minimumReturn

        A_ub = FiMa.constraintsInequality(time, stocks, my, "left", options)
        A_eq = FiMa.constraintsEquality(time, stocks, "left", options)

        b_ub = FiMa.constraintsInequality(time, stocks, my, "right", options)
        b_eq = FiMa.constraintsEquality(time, stocks, "right", options)

        solution = opt.linprog(
            c=c, 
            A_ub=A_ub, 
            b_ub=b_ub, 
            A_eq=A_eq, 
            b_eq=b_eq, 
            bounds=bounds, 
            method="highs"
        )
        
        obj = solution.fun
        return obj
    
    @staticmethod
    def payOff(stock: float, strike: float):
        S = stock
        K = strike

        payOffCall = max([S-K, 0])
        payOffPut = max([K-S, 0])

        return payOffCall, payOffPut
    
    @staticmethod
    def priceOption(date: dt.datetime=None, dateExpiration: dt.datetime=None, daysToMaturity: int=None, stockPrice: float=0.00, strikePrice: float=0.00, volatility: float=0.00, riskFreeRate: float=0.00) -> float:
        if stockPrice == 0.00 or strikePrice == 0.00 or volatility == 0.00 or riskFreeRate == 0.00:
            print("Mindestens ein Eingabeparameter fehlt oder ist 0")
            return 0.00, 0.00
        
        if date != None and dateExpiration != None and daysToMaturity == None:
            tau = (dateExpiration - date) / dt.timedelta(days=365)
        elif date == None and dateExpiration == None and daysToMaturity != None:
            tau = dt.timedelta(days=daysToMaturity) / dt.timedelta(days=365)
        else:
            print("Entweder date & dateEpiration oder daysToMaturity müssen übergeben werden")
            return 0.00, 0.00
        
        S = stockPrice
        K = strikePrice
        r = riskFreeRate
        sigma = volatility

        dPlus = ((r + 0.5*sigma**2)*tau + np.log(S/K))/(sigma*np.sqrt(tau))
        dMinus = ((r - 0.5*sigma**2)*tau + np.log(S/K))/(sigma*np.sqrt(tau))

        vCall = S*st.norm.cdf(dPlus) - K*np.exp(-r*tau)*st.norm.cdf(dMinus)
        vPut = K*np.exp(-r*tau)*(1 - st.norm.cdf(dMinus)) - S*(1 - st.norm.cdf(dPlus))

        return vCall, vPut
    
    @staticmethod
    def historicalVolatility(times, stock):
        # Schätzter für die Volatilität sigma in der GBM (dS = my*S*dt + sigma*S*dW) aus historisches Stock-Daten
        # ACHTUNG: Bis maximal sigma = 0.5 geeignet.
        # Hinweis: Sigma wird in der Regel unterschätzt

        myHat = 0
        for i in range(len(times)-1):
            deltaT = (times[i+1] - times[i])/(times[-1] - times[0])
            myHat += (stock[i+1] - stock[i])/stock[i]*deltaT

        sTemp = 0
        for i in range(len(times)-1):
            deltaT = (times[i+1] - times[i])/(times[-1] - times[0])
            sTemp += ((stock[i+1] - stock[i])/stock[i] - myHat)**2*deltaT

        sigmaHat = np.sqrt(sTemp)
        return sigmaHat
    
    @staticmethod
    def impliedVolatility(daysToMaturity, stockPrice, strikePrice, optionPrice, riskFreeRate):
        # Annäherung der Impliziten Volatilität
        # ACHTUNG: Sehr langsame Methode, wegen hoher Komplexität
        # Hinweis: Sigma auf vier Nachkommastellen genau
        
        sigmaCall = float(0.50) # Startwert sigma für Call-Optionen
        sigmaPut = float(0.50) # Startwert sigma für Put-Optionen

        stepSize = float(1e-5) # Schrittweite

        for _ in range(int(1e+5)):
            optionPriceCall, _ = FiMa.priceOption(
                daysToMaturity=daysToMaturity, 
                stockPrice=stockPrice, 
                strikePrice=strikePrice, 
                volatility=sigmaCall, 
                riskFreeRate=riskFreeRate
            )
            if optionPriceCall < optionPrice:
                sigmaCall += stepSize
            else:
                sigmaCall -= stepSize

            residuum = abs(optionPriceCall - optionPrice)
            if residuum < float(1e-5) or sigmaCall < 0:
                break

        for _ in range(int(1e+5)):
            _, optionPricePut = FiMa.priceOption(
                daysToMaturity=daysToMaturity, 
                stockPrice=stockPrice, 
                strikePrice=strikePrice, 
                volatility=sigmaPut, 
                riskFreeRate=riskFreeRate
            )
            if optionPricePut < optionPrice:
                sigmaPut += stepSize
            else:
                sigmaPut -= stepSize

            residuum = abs(optionPricePut - optionPrice)
            if residuum < float(1e-5) or sigmaPut < 0:
                break

        return sigmaCall, sigmaPut
    
    @staticmethod
    def delta(daysToMaturity: int=None, stockPrice: float=0.00, strikePrice: float=0.00, volatility: float=0.00, riskFreeRate: float=0.00):
        tau = dt.timedelta(days=daysToMaturity) / dt.timedelta(days=365)
        S = stockPrice
        K = strikePrice
        r = riskFreeRate
        sigma = volatility

        dPlus = ((r + 0.5*sigma**2)*tau + np.log(S/K))/(sigma*np.sqrt(tau))

        deltaCall = st.norm.cdf(dPlus)
        deltaPut = st.norm.cdf(dPlus) - 1

        return deltaCall, deltaPut
    
    @staticmethod
    def gamma(daysToMaturity: int=None, stockPrice: float=0.00, strikePrice: float=0.00, volatility: float=0.00, riskFreeRate: float=0.00):
        tau = dt.timedelta(days=daysToMaturity) / dt.timedelta(days=365)
        S = stockPrice
        K = strikePrice
        r = riskFreeRate
        sigma = volatility

        dPlus = ((r + 0.5*sigma**2)*tau + np.log(S/K))/(sigma*np.sqrt(tau))

        gamma = st.norm.pdf(dPlus)/(S*sigma*np.sqrt(tau))

        return gamma

    @staticmethod
    def theta(daysToMaturity: int=None, stockPrice: float=0.00, strikePrice: float=0.00, volatility: float=0.00, riskFreeRate: float=0.00):
        tau = dt.timedelta(days=daysToMaturity) / dt.timedelta(days=365)
        S = stockPrice
        K = strikePrice
        r = riskFreeRate
        sigma = volatility

        dPlus = ((r + 0.5*sigma**2)*tau + np.log(S/K))/(sigma*np.sqrt(tau))
        dMinus = ((r - 0.5*sigma**2)*tau + np.log(S/K))/(sigma*np.sqrt(tau))

        thetaCall = -r*K*np.exp(-r*tau)*st.norm.cdf(dMinus) - 0.5*S*sigma*st.norm.pdf(dPlus)/np.sqrt(tau)
        thetaPut = r*K*np.exp(-r*tau)*st.norm.cdf(-dMinus) - 0.5*S*sigma*st.norm.pdf(dPlus)/np.sqrt(tau)

        return thetaCall/365, thetaPut/365

    @staticmethod
    def vega(daysToMaturity: int=None, stockPrice: float=0.00, strikePrice: float=0.00, volatility: float=0.00, riskFreeRate: float=0.00):
        tau = dt.timedelta(days=daysToMaturity) / dt.timedelta(days=365)
        S = stockPrice
        K = strikePrice
        r = riskFreeRate
        sigma = volatility

        dPlus = ((r + 0.5*sigma**2)*tau + np.log(S/K))/(sigma*np.sqrt(tau))

        vega = S*np.sqrt(tau)*st.norm.pdf(dPlus)

        return vega/100

    @staticmethod
    def rho(daysToMaturity: int=None, stockPrice: float=0.00, strikePrice: float=0.00, volatility: float=0.00, riskFreeRate: float=0.00):
        tau = dt.timedelta(days=daysToMaturity) / dt.timedelta(days=365)
        S = stockPrice
        K = strikePrice
        r = riskFreeRate
        sigma = volatility

        dMinus = ((r - 0.5*sigma**2)*tau + np.log(S/K))/(sigma*np.sqrt(tau))

        rhoCall = K*tau*np.exp(-r*tau)*st.norm.cdf(dMinus)
        rhoPut = -K*tau*np.exp(-r*tau)*st.norm.cdf(-dMinus)

        return rhoCall/100, rhoPut/100
    
FiMa = FinancialMathematics