import threading
import numpy as np
import matplotlib.pyplot as plt
import time
class myThread(threading.Thread):
    def __init__(self, threadID, name, inst, t, signal, runflag=True):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.inst = inst
        self.runflag = runflag
        self.t = t
        self.signal = signal
        print(t)
    def run(self):
        plt.ion()
        self.inst.write('RUN')
        time.sleep(2)
        fig = plt.figure(figsize=(11.69,8.27), dpi = 100)
        ax = fig.add_subplot(111)
        ax.set_xlim([0, 1000])
        self.inst.write('STOP')
        time.sleep(1)
        t_win = float(self.inst.query(':TIMebase:MAIN:SCALe?')) # Time window
        fs = float(self.inst.query(':ACQuire:SRATe?')) # Sample rate
        timestep = float(self.inst.query(':WAVeform:XINCrement?'))
        n = t_win*fs  # number of samples
        print('Samplerate: ' + str(fs) + ' [1/s]')
        print('Window size: ' + str(t_win) + ' [s]')
        print('Samples: ' + str(n) + ' [-]')
        print('Timestep: ' + str(timestep) + '| ' + str(1/timestep))
        self.inst.write(':WAV:SOUR CHAN1')
        self.inst.write(':WAV:MODE NORM')
        self.inst.write(':WAV:FORM ASCii')
        V_chan1_str = self.inst.query(':WAV:DATA?')
        V_chan1_str = V_chan1_str[11:].split(',')
        V_chan1 = [float(i) for i in V_chan1_str]
        V_chan1 = V_chan1 - np.mean(V_chan1)
        self.inst.write('RUN')
        time.sleep(2)
        fftV_chan1 = np.fft.fft(V_chan1)
        freq = np.fft.fftfreq(np.size(V_chan1), timestep)

        absfft = np.abs(fftV_chan1)
        line1, = ax.plot(freq, absfft/np.size(absfft), '.')
        signalmeas_fft = np.fft.fft(self.signal-np.mean(self.signal))
        print(self.t)
        signalmeas_freq = np.fft.fftfreq(np.size(self.t), self.t[1]-self.t[0])
        line2, = ax.plot(signalmeas_freq, np.abs(signalmeas_fft)/np.size(signalmeas_fft))
        for i in range(1, 2):
            self.inst.write('STOP')
            time.sleep(10)
            t_win = float(self.inst.query(':TIMebase:MAIN:SCALe?')) # Time window
            fs = float(self.inst.query(':ACQuire:SRATe?')) # Sample rate
            timestep = float(self.inst.query(':WAVeform:XINCrement?'))
            n = t_win*fs  # number of samples
            print('Samplerate: ' + str(fs) + ' [1/s]')
            print('Window size: ' + str(t_win) + ' [s]')
            print('Samples: ' + str(n) + ' [-]')
            print('Timestep: ' + str(timestep) + '| ' + str(1/timestep))
            self.inst.write(':WAV:SOUR CHAN1')
            self.inst.write(':WAV:MODE NORM')
            self.inst.write(':WAV:FORM ASCii')
            V_chan1_str = self.inst.query(':WAV:DATA?')
            V_chan1_str = V_chan1_str[11:].split(',')
            V_chan1 = [float(i) for i in V_chan1_str]
            V_chan1 = V_chan1 - np.mean(V_chan1)
            self.inst.write('RUN')
            time.sleep(2)
            fftV_chan1 = np.fft.fft(V_chan1)
            freq = np.fft.fftfreq(np.size(V_chan1), timestep)

            absfft = np.abs(fftV_chan1)
            line1.set_ydata(absfft)
            fig.canvas.draw()
