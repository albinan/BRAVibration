import numpy as np
def errFun(S, S_k):
    return (np.sum(np.abs(np.abs(S_k) - np.abs(S))) + np.sum(np.abs(np.angle(S_k) - np.angle(S))))/np.size(S)

def errFunAmp(S, S_k):
    return np.sum(np.abs(np.abs(S_k) - np.abs(S)))/np.size(S)
