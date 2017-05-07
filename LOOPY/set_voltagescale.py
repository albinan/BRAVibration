import numpy as np
import time
from overshoot import overshoot
def set_voltagescale(inst, channel):
    V_win = np.array(
        [0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10])

    V = float(inst.query(':MEASure:ITEM? VPP,'+channel))/8  # p2p voltage
    # divided by the number of divisions on screen
    while V > 9999:
        V_current = float(inst.query(':' + channel + ':SCALe?'))
        if V_current > 6:
            print('Unexpected error')
            exit(0)
        V_set = V_win[np.argmin(np.abs(V_win-V_current)) + 1]
        print('Setting scale to ' + str(V_set) + ' V')
        inst.write(':' + channel + ':SCALe ' + str(V_set))
        time.sleep(3)
        print('Waiting in 3 seconds: Finding window size')
        V = float(inst.query(':MEASure:ITEM? VPP,'+channel))/8
    # We want the closest value above V for the window so that the signal will
    # fit. We are thefore looking for the closest value above 0 in V_win - V.
    for i in range(np.size(V_win)):
        if (V_win[i] - V) < 0:
            V_win[i] = 9999

    V_set = V_win[np.argmin(V_win-V) + 1]

    V_current = float(inst.query(':' + channel + ':SCALe?'))
    # print('Voltage:' + str(V/8))
    # print('Voltage_set:' + str(V_set))
    # print('Voltage_current:' + str(V_current))
    if V_set != V_current:
        inst.write(':' + channel + ':SCALe ' + str(V_set))
        time.sleep(1)
        print('Waiting 1 second: Setting voltage scale')
