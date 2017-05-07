import numpy as np
def order2transfer(w, b0, b1, b2, a0, a1, a2):
    s = 1j*w
    D = b0 + b1*s + b2*s**2
    P = a0 + a1*s + a2*s**2
    return D/P


def order1transfer(w, b0, b1, a0, a1):
    s = 1j*w
    D = b0 + b1*s
    P = a0 + a1*s
    return D/P


def G_harmonic(freq, f_n, xi):
    w = 2*np.pi*freq
    w_n = 2*np.pi*f_n
    D = 1
    P = w_n**2 - w**2 + 2*1j*w_n*xi*w
    return D/P

def G_electric_gen_noL(freq, K):
    s = 1j*2*np.pi*freq
    D = -K*s
    P = 1
    return D/P

def H_noL(freq, K, f_n, xi):
        return G_electric_gen_noL(freq, K)*G_harmonic(freq, f_n, xi)
