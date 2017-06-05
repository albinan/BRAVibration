'''Application without GUI'''
from oscilloscope import Oscilloscope
import matplotlib.pyplot as plt

def main():
    channels = '2'
    scope = Oscilloscope(channels)
    scope.set_timescale(12)
    #a = []
    #scope.manualrecord(1, a)
    #plt.plot(a)
    #plt.show()

if __name__ == '__main__':
    main()
