import numpy as np
'''
A set of utility function
'''


def rootMeanSquare(a):
    '''
    Calculates RMS for any 1D array like object
    '''
    rms = 0
    N = np.size(a)
    for i in range(0, N):
        rms = rms + a[i]**2
    rms = rms/N
    rms = np.sqrt(rms)
    return rms


def fixtimedata(t):
    '''
    Modifies time vector from vibration logger
    '''
    n = len(t)
    for i in range(n-1):
        if t[i+1] < t[i]:
            t[i+1:] = t[i+1:] + t[i]
