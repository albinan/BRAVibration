
def V2G(Vpp, sf, s_handle):
    # Vpp: Voltage peak to peak
    # sf: scaling factor from voltage to g
    g = Vpp*sf*s_handle
    return g
