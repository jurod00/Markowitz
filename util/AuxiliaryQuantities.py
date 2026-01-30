import numpy as np
import datetime as dt

from util.Time import Time

#TODO
#Testen, ob dasselbe herauskommt

class AuxiliaryQuantities:

    def __init__(self):
        pass

    def duration(self, time: list):
        return time[-1] - time[0]
    
    def n(self, time: list):
        return self.duration(time).days

    def p(self, time: list):

        duration = self.duration(time)
        n = self.n(time)

        p = np.empty(n)
        for i in range(n):
            p[i] = (time[i+1] - time[i]) / duration

        return p
    
def test():
    t0 = dt.datetime(2025,12,1)
    tn = dt.datetime(2025,12,11)
    T = Time(t0, tn)
    time = T.getTime()

    AQ = AuxiliaryQuantities()
    p = AQ.p(time)
    print(p)

if __name__ == "__main__":
    test()