from portfolio.portfolio import Portfolio

import numpy as np
import matplotlib.pyplot as plt

cmap = plt.get_cmap("Greens")
# Verwendung mit cmap(c) für c in [0,1]

class PlotPortfolio:
    
    def __init__(self, portfolio: Portfolio):
        self.portfolio = portfolio

    def colors(self):
        pass

    def markers(self):
        pass

    def plotStocks(self, absRel: str="rel"):
        # keine Marker!
        pass

    def plotStackedBar(self, allocation: np.ndarray=None, minimumReturn: float=None, alpha: float=None, beta: float=None, riskAversion: float=None):
        if allocation is not None:
            groups = ["Portfolio"]

            fig, ax = plt.subplots(figsize=(10, 2))
            for i in range(len(allocation)):
                left = (0 if i == 0 else sum(allocation[:i]))
                ax.barh(y=groups, width=allocation[i], left=left, color=cmap((i+1)/len(allocation)))
                ax.text(x=left+0.5*allocation[i], y=0, s="{:.2f}".format(100*allocation[i]) + "%", ha="center", color="white", weight="bold", size=10)
            
            ax.set_xlim(0, 1)
            ax.set_ylim(-1, 1)

            plt.show()

        if minimumReturn is not None and (alpha is None or beta is None): # Markowitz
            pass
        if minimumReturn is not None and alpha is not None and beta is not None: # IntegratedRiskManagement
            pass
        if riskAversion is not None: # UtilityMaximization
            pass