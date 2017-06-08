import numpy as np
import time
def set_timescale(t, inst):
    t_win = np.array([0.000000005, 0.00000002, 0.00000005, 0.0000001, 0.0000005,
                    0.000001, 0.000005, 0.00002, 0.00005, 0.0001, 0.0005,
                    0.001, 0.005, 0.02, 0.05, 0.1, 0.5,
                    1, 5, 20, 50])

    t_set = t_win[np.argmin(np.abs(t_win-t))]

    t_current = float(inst.query(':TIMebase:MAIN:SCALe? '))

    if t_set != t_current:
        inst.write(':TIMebase:MAIN:SCALe ' + str(t_set))
        time.sleep(2)
        print('Waiting 1 second: Setting timescale')
