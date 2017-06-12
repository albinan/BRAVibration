import numpy as np
import sys
sys.path.append('C:/Users/ReVibe/Documents/Albin/BRAVibration/LIB')
from oscilloscope import Oscilloscope

def findEig():
    scope = Oscilloscope(activeChannels=[1,2])
    f0 = scope.get_fre
    n_waves = 5
    print(scope.meas_frequency(channel=1))



if __name__ == '__main__':
    findEig()
