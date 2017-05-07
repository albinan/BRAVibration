
def linmod(w, N, B, l, Rload, Rcoil, m, k, dm):
    G = ((N*B*l*Rload)/(Rload + Rcoil))*(1j*w/(-m*(w**2) + k + 1j*(dm + ((N*B*l)**2))/Rload))
    return G
