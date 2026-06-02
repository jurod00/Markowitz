import numpy as np
import pandas as pd
import datetime as dt
import scipy.optimize as opt

from mathematics.financialMathematics import FinancialMathematics as FiMa
from simulation.geometricBrownianMotion import GeometricBrownianMotion as Gbm
from iO.input import Input

class PortfolioSharesOptions:
    def __init__(self):
        self.time : list=[]
        self.stocks : list=[]
        self.options : dict={}
        self.symbols : list=[]

    def getTime(self) -> list:
        return self.time
    
    def setTime(self, time: list) -> None:
        self.time = time

    def getStocks(self) -> list:
        return self.stocks
    
    def setStocks(self, stocks: list) -> None:
        self.stocks = stocks

    def getOptions(self) -> dict:
        return self.options
    
    def setOptions(self, options: dict) -> None:
        self.options = options

    def getSymbols(self) -> list:
        return self.symbols
    
    def setSymbols(self, symbols: list) -> None:
        self.symbols = symbols