import numpy as np
def gaussWindow4(f, f0, M, sigma):
    w = (np.exp(-1/2*((f-f0)/sigma)**4) + np.exp(-1/2*((f+f0)/sigma)**4))/2
    return w
def gaussWindow(f, f0, M, sigma):
    w = (np.exp(-1/2*((f-f0)/sigma)**2) + np.exp(-1/2*((f+f0)/sigma)**2))/2
    return w
