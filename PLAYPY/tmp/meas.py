import numpy as np
import visa
import time
import os
import matplotlib.pyplot as plt
from scipy.fftpack import fft, fftfreq
import threading


class oscill():
    def __init__(self, channels, oscillResource='USB0::0x1AB1::0x04CE::DS1ZD171500380::INSTR'):
        rm = visa.ResourceManager()
        self.inst = rm.open_resource(oscillResource)
        self.initinst()
        self.t_inc = 0
        self.fs = 0
        self.t_win = 0
        self.channels = channels
        self.initinst()

    def initinst(self):
        self.t_win = float(self.inst.query(':TIMebase:MAIN:SCALe?'))

        print('Samplerate: ' + str(self.fs) + ' [1/s]')
        print('Window size: ' + str(self.t_win) + ' [s]')
        print('Sampling frequency: ' + str(self.fs))
        print('Time increment: ' + str(self.t_inc))
        self.inst.write(':WAV:MODE NORM')
        self.inst.write(':WAV:FORM ASCii')

    def snapshot(self):
        self.t_inc = float(self.inst.query(':WAVeform:XINCrement?'))
        self.fs = 1/self.t_inc
        V_chan = []
        channels = self.channels.split(',')
        for channel in channels:
            V_chan_tmp = []
            self.inst.write(':WAV:SOUR CHAN' + channel)
            V_chan_str = self.inst.query(':WAV:DATA?')
            V_chan_str = V_chan_str[11:].split(',')
            V_chan_tmp.extend([float(i) for i in V_chan_str])
            V_chan.append(V_chan_tmp)

        n = np.size(V_chan[0])
        t = []
        t.append(np.asarray(range(0, n))*self.t_inc)
        data = np.transpose(np.vstack((t, V_chan)))

        return data
