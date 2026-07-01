import time
import numpy as np
import math
import scipy.stats as st

sigma = 0.5
tau = 0.5
r = 0.05
S = 100
K = 120

def test1():
    start = time.time()
    for i in range(int(1e5)):
        dPlus = ((r + 0.5*sigma**2)*tau + math.log(S/K))/(sigma*tau**0.5)
        dMinus = ((r - 0.5*sigma**2)*tau + math.log(S/K))/(sigma*tau**0.5)
        priceCall = S*st.norm.cdf(dPlus) - K*np.exp(-r*tau)*st.norm.cdf(dMinus)
    print(time.time()-start)
    # print(priceCall)

    start = time.time()
    for i in range(int(1e5)):
        dPlus = ((r + 0.5*sigma**2)*tau + math.log(S/K))/(sigma*tau**0.5)
        dMinus = dPlus - sigma*tau**0.5
        priceCall = S*st.norm.cdf(dPlus) - K*math.exp(-r*tau)*st.norm.cdf(dMinus)
    print(time.time()-start)
    # print(priceCall)

if __name__ == "__main__":
    test1()