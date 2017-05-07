def G2V(g, sf, s_handle):
    # Vpp: Voltage peak to peak
    # sf: scaling factor from voltage to g
    Vpp = g/(sf*s_handle)
    return Vpp
