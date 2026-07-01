import math
import datetime as dt
import scipy.stats as st

class Option:

    def __init__(self):
        pass
    
    @staticmethod
    def payOffCall(stock: float, strike: float) -> float:
        return max([stock-strike, 0])
    
    @staticmethod
    def payOffPut(stock: float, strike: float) -> float:
        return max([strike-stock, 0])
    
    @staticmethod
    def priceOptionCall(daysToMaturity: int=None, stockPrice: float=None, strikePrice: float=None, riskFreeRate: float=None, implVolatility: float=None) -> float:
        tau = dt.timedelta(days=daysToMaturity)/dt.timedelta(days=365)
        dPlus = ((riskFreeRate + 0.5*implVolatility**2)*tau + math.log(stockPrice/strikePrice))/(implVolatility*tau**0.5)
        dMinus = dPlus - implVolatility*tau**0.5

        return stockPrice*st.norm.cdf(dPlus) - strikePrice*math.exp(-riskFreeRate*tau)*st.norm.cdf(dMinus)
    
    @staticmethod
    def priceOptionPut(daysToMaturity: int=None, stockPrice: float=None, strikePrice: float=None, riskFreeRate: float=None, implVolatility: float=None) -> float:
        tau = dt.timedelta(days=daysToMaturity)/dt.timedelta(days=365)
        dPlus = ((riskFreeRate + 0.5*implVolatility**2)*tau + math.log(stockPrice/strikePrice))/(implVolatility*tau**0.5)
        dMinus = dPlus - implVolatility*tau**0.5

        return strikePrice*math.exp(-riskFreeRate*tau)*(1 - st.norm.cdf(dMinus)) - stockPrice*(1 - st.norm.cdf(dPlus))
    
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------
    #                                                                           Greeks
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    @staticmethod
    def deltaCall(daysToMaturity: int=None, stockPrice: float=None, strikePrice: float=None, riskFreeRate: float=None, implVolatility: float=None) -> float:
        tau = dt.timedelta(days=daysToMaturity)/dt.timedelta(days=365)
        dPlus = ((riskFreeRate + 0.5*implVolatility**2)*tau + math.log(stockPrice/strikePrice))/(implVolatility*tau**0.5)

        return st.norm.cdf(dPlus)
    
    @staticmethod
    def deltaPut(daysToMaturity: int=None, stockPrice: float=None, strikePrice: float=None, riskFreeRate: float=None, implVolatility: float=None) -> float:
        tau = dt.timedelta(days=daysToMaturity)/dt.timedelta(days=365)
        dPlus = ((riskFreeRate + 0.5*implVolatility**2)*tau + math.log(stockPrice/strikePrice))/(implVolatility*tau**0.5)

        return st.norm.cdf(dPlus) - 1
    
    @staticmethod
    def gamma(daysToMaturity: int=None, stockPrice: float=None, strikePrice: float=None, riskFreeRate: float=None, implVolatility: float=None) -> float:
        tau = dt.timedelta(days=daysToMaturity)/dt.timedelta(days=365)
        dPlus = ((riskFreeRate + 0.5*implVolatility**2)*tau + math.log(stockPrice/strikePrice))/(implVolatility*tau**0.5)

        return st.norm.pdf(dPlus)/(stockPrice*implVolatility*tau**0.5)
    
    @staticmethod
    def thetaCall(daysToMaturity: int=None, stockPrice: float=None, strikePrice: float=None, riskFreeRate: float=None, implVolatility: float=None) -> float:
        tau = dt.timedelta(days=daysToMaturity)/dt.timedelta(days=365)
        dPlus = ((riskFreeRate + 0.5*implVolatility**2)*tau + math.log(stockPrice/strikePrice))/(implVolatility*tau**0.5)
        dMinus = dPlus - implVolatility*tau**0.5

        return (-riskFreeRate*strikePrice*math.exp(-riskFreeRate*tau)*st.norm.cdf(dMinus) - 0.5*stockPrice*implVolatility*st.norm.pdf(dPlus)/tau**0.5)/365
    
    @staticmethod
    def thetaPut(daysToMaturity: int=None, stockPrice: float=None, strikePrice: float=None, riskFreeRate: float=None, implVolatility: float=None) -> float:
        tau = dt.timedelta(days=daysToMaturity)/dt.timedelta(days=365)
        dPlus = ((riskFreeRate + 0.5*implVolatility**2)*tau + math.log(stockPrice/strikePrice))/(implVolatility*tau**0.5)
        dMinus = dPlus - implVolatility*tau**0.5

        return (riskFreeRate*strikePrice*math.exp(-riskFreeRate*tau)*st.norm.cdf(-dMinus) - 0.5*stockPrice*implVolatility*st.norm.pdf(dPlus)/tau**0.5)/365
    
    @staticmethod
    def vega(daysToMaturity: int=None, stockPrice: float=None, strikePrice: float=None, riskFreeRate: float=None, implVolatility: float=None) -> float:
        tau = dt.timedelta(days=daysToMaturity)/dt.timedelta(days=365)
        dPlus = ((riskFreeRate + 0.5*implVolatility**2)*tau + math.log(stockPrice/strikePrice))/(implVolatility*tau**0.5)

        return 0.01*stockPrice*st.norm.pdf(dPlus)*tau**0.5
    
    @staticmethod
    def rhoCall(daysToMaturity: int=None, stockPrice: float=None, strikePrice: float=None, riskFreeRate: float=None, implVolatility: float=None) -> None:
        tau = dt.timedelta(days=daysToMaturity)/dt.timedelta(days=365)
        dMinus = ((riskFreeRate - 0.5*implVolatility**2)*tau + math.log(stockPrice/strikePrice))/(implVolatility*tau**0.5)

        return 0.01*strikePrice*tau*math.exp(-riskFreeRate*tau)*st.norm.cdf(dMinus)
    
    @staticmethod
    def rhoPut(daysToMaturity: int=None, stockPrice: float=None, strikePrice: float=None, riskFreeRate: float=None, implVolatility: float=None) -> None:
        tau = dt.timedelta(days=daysToMaturity)/dt.timedelta(days=365)
        dMinus = ((riskFreeRate - 0.5*implVolatility**2)*tau + math.log(stockPrice/strikePrice))/(implVolatility*tau**0.5)

        return -0.01*strikePrice*tau*math.exp(-riskFreeRate*tau)*st.norm.cdf(-dMinus)
    
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------
    #                                                                           Estimators
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def historicalVolatility(times: list, stock: list) -> float:
        # Estimator for the historical volatility sigma in the GBM (dS = my*S*dt + sigma*S*dW)
        # WARNING: sigma is usually underestimated
        # WARNING: Just useable for sigma < 0.5

        n = len(times) - 1

        my = 0
        for i in range(n):
            dt = (times[i+1] - times[i])/(times[-1] - times[0])
            my += (stock[i+1] - stock[i])/stock[i]*dt

        s = 0
        for i in range(n):
            dt = (times[i+1] - times[i])/(times[-1] - times[0])
            s += ((stock[i+1] - stock[i])/stock[i] - my)**2*dt

        return s**0.5
    
    def impliedVolatilityCall(daysToMaturity: int=None, stockPrice: float=None, strikePrice: float=None, riskFreeRate: float=None, priceOptionCall: float=None) -> float:
        # Estimator for the implied volatility sigma
        # WARNING: Just usable for sigma > 0.03

        N = int(1e+2) # max loops
        res = float(1e-4) # residuum

        implVolatility0 = float(1e-2)
        implVolatility1 = float(5e-2)

        for _ in range(N):
            priceOption0 = Option.priceOptionCall(
                daysToMaturity=daysToMaturity, 
                stockPrice=stockPrice, 
                strikePrice=strikePrice, 
                riskFreeRate=riskFreeRate, 
                implVolatility=implVolatility0
            )
            priceOption1 = Option.priceOptionCall(
                daysToMaturity=daysToMaturity, 
                stockPrice=stockPrice, 
                strikePrice=strikePrice, 
                riskFreeRate=riskFreeRate, 
                implVolatility=implVolatility1
            )

            implVolatility2 = implVolatility1 - (priceOption1 - priceOptionCall)*(implVolatility1 - implVolatility0)/(priceOption1 - priceOption0)

            if abs(implVolatility2 - implVolatility1) < res:
                return implVolatility2

            implVolatility0 = implVolatility1
            implVolatility1 = implVolatility2
            
        return None
    
    def impliedVolatilityPut(daysToMaturity: int=None, stockPrice: float=None, strikePrice: float=None, riskFreeRate: float=None, priceOptionPut: float=None) -> float:
        # Estimator for the implied volatility sigma
        # WARNING: Just usable for sigma > 0.03

        N = int(1e+2) # max loops
        res = float(1e-4) # residuum

        implVolatility0 = float(1e-2)
        implVolatility1 = float(5e-2)

        for _ in range(N):
            priceOption0 = Option.priceOptionPut(
                daysToMaturity=daysToMaturity, 
                stockPrice=stockPrice, 
                strikePrice=strikePrice, 
                riskFreeRate=riskFreeRate, 
                implVolatility=implVolatility0
            )
            priceOption1 = Option.priceOptionPut(
                daysToMaturity=daysToMaturity, 
                stockPrice=stockPrice, 
                strikePrice=strikePrice, 
                riskFreeRate=riskFreeRate, 
                implVolatility=implVolatility1
            )

            implVolatility2 = implVolatility1 - (priceOption1 - priceOptionPut)*(implVolatility1 - implVolatility0)/(priceOption1 - priceOption0)

            if abs(implVolatility2 - implVolatility1) < res:
                return implVolatility2

            implVolatility0 = implVolatility1
            implVolatility1 = implVolatility2
        
        return None