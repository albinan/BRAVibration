from V2G import V2G
from G2V import G2V
import numpy as np
import time
from set_voltagescale import set_voltagescale
from amplifierCheck import amplifierCheck
def set_g(g_f, inst, sf_vg, s_handle, g_err, iterations, k_p, checkAmplifier):

    # Initiation variables
    y_f = G2V(g_f, sf_vg, s_handle)  # The value of V that we want
    y_0 = float(inst.query(':MEASure:ITEM? VRMS,CHANnel2'))  # The value of V that we have
    r = y_f-y_0  # Variable we want to mimimize

    y_err = G2V(g_err, sf_vg, s_handle)  # Tranlated error to V
    counter = 0

    while np.abs(r) > y_err:
        set_voltagescale(inst, 'CHANnel1')
        set_voltagescale(inst, 'CHANnel2')
        x = float(inst.query('VOLTage?')) + k_p*r

        if np.abs(x) < 1000:  # Can not set voltage to unreasonable value
            inst.write('VOLTage ' + str(x))

            if checkAmplifier:
                amplifierCheck(inst) # Checks if meassured voltage is greater or less than actual voltage

        time.sleep(1)


        # print('Waiting 1 second: System adapting, setting g level')
        set_voltagescale(inst, 'CHANnel1')
        set_voltagescale(inst, 'CHANnel2')
        y_0 = float(inst.query(':MEASure:ITEM? VRMS,CHANnel2'))  # The value of
        # V that we have
        r = y_f-y_0  # Variable we want to mimimize
        counter = counter + 1
        if counter > iterations:
            print('Too many iterations')
            return 0

    return 1
