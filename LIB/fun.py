import numpy as np

def rootMeanSquare(a):
    rms = 0
    N = np.size(a)
    for i in range(0, N):
        rms = rms + a[i]**2
    rms = rms/N
    rms = np.sqrt(rms)
    return rms

def slices(a, n_slice, n):
    if n_slice == 1 or n_slice == 0:
        return a
    a_len = np.size(a)
    inval = np.floor(a_len/n_slice)
    print(n*inval/a_len)
    return a[n*inval:(n+1)*inval]

def fixtimedata(t):
    n = len(t)
    for i in range(n-1):
        if t[i+1] < t[i]:
            t[i+1:] = t[i+1:] + t[i]
