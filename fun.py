import numpy as np

def rootMeanSquare(a):
    rms = 0
    N = np.size(a)
    for i in range(0, N):
        rms = rms + a[i]**2
    rms = rms/N
    rms = np.sqrt(rms)
    return rms
