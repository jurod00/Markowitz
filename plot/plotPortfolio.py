from portfolio.portfolio import Portfolio

class PlotPortfolio:
    
    def __init__(self, portfolio: Portfolio):
        self.portfolio = portfolio

    def colors(self):
        pass

    def markers(self):
        pass

    def plotStocks(self, absRel: str="rel"):
        pass

    def plotStackedBar(self, allocation: list=None, minimumReturn: float=None, alpha: float=None, beta: float=None, riskAversion: float=None):
        if allocation is not None:
            pass
        if minimumReturn is not None and (alpha is None or beta is None): # Markowitz
            pass
        if minimumReturn is not None and alpha is not None and beta is not None: # IntegratedRiskManagement
            pass
        if riskAversion is not None: # UtilityMaximization
            pass