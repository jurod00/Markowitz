import matplotlib.pyplot as plt

class PlotStock:

    def __init__(self, time, stock):
        self.time = time
        self.stock = stock

    def setTime(self, time):
        self.time = time

    def setStock(self, stock):
        self.stock = stock

    def plot(self):
        fig, ax1 = plt.subplots(figsize=(15,10))
        #ax2 = ax1.twinx()

        ax1.plot(self.time, self.stock)
        plt.show()

        #fig.savefig("C:/Users/j.rode/Desktop/Markowitz/plot/plot.svg")