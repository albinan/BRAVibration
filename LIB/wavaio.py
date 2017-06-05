import wave
import csv
import numpy as np
import sys
import matplotlib.pyplot as plt
from scipy.fftpack import fft, ifft, fftshift, ifftshift
from scipy.io import wavfile
sys.path.append('C:/Users/ReVibe/Documents/Albin/MasterSnake/LIB')
sys.path.append('C:/Users/ReVibe/Documents/Albin/MasterSnake/LIB/wavio')
import wavio
from importdata0 import importTool
from fun import rootMeanSquare, fixtimedata
from scipy.signal import resample
import scipy.io.wavfile
import struct


def writeWav(t_i, x_i, csvFileLoc, fs_f=41000, scale_t=1, scale_a=1, fileAdd='', test=False):

    ##INITIAL SIGNAL
    x_i = (x_i - np.mean(x_i))*scale_a  # initial acceleration vector
    t_i = (t_i - t_i[0])*scale_t  # final acceleration vector
    fixtimedata(t_i)
    # Parameters for initial signal
    n_i = np.size(t_i)

    dt_i = (t_i[-1]-t_i[0])/(n_i-1)
    fs_i = 1/dt_i
    xrms_i = rootMeanSquare(x_i)
    
    x_i_max = np.max(np.abs(x_i))

    # Resample time vector in case of strange data
    t_i = np.linspace(0, 1, n_i)*dt_i*(n_i-1)
    t_tot = t_i[-1]

    # FINAL SIGNAL
    n_f = np.round(t_tot*fs_f) # number of samples for final signal
    print('Resampling signal. This migth take some time...')
    (x_f, t_f) = resample(x_i, n_f, t_i)
    x_f_max = np.max(np.abs(x_f))
    xrms_f = rootMeanSquare(x_f)

    if test:
        plt.plot(t_f, x_f)
        plt.plot(t_i, x_i)
        print('xrms_i', xrms_i)
        print('max_i', x_i_max)
        print('fs_i', fs_i)
        print('xrms_f', xrms_f)
        print('max_f', x_f_max)
        plt.show()

    sampwidth = 4
    x_f_scaled = np.int16((x_f/x_f_max) * 32767)
    print('Sample Frequency initial: ', fs_i)
    print('Sample Frequency final: ', 1/(t_f[1]-t_f[0]))
    print('wavFileLoc: ', csvFileLoc[:-4] + '.wav')
    print('xrms_i/xrms_f', str(xrms_i/xrms_f))
    print('gmax_i/gmax_f', str(x_i_max/x_f_max))
    print('Writing wav file...')

    scipy.io.wavfile.write(csvFileLoc[:-4] + fileAdd +'resampled_Fs' + str(fs_f) + '.wav', fs_f, x_f_scaled)

    with open(csvFileLoc[:-4] + fileAdd +'resampled_Fs' + str(fs_f) + 'CALIBRATION.csv', 'w') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')
        spamwriter.writerow(['g_max'])
        spamwriter.writerow([str(x_f_max)])
        spamwriter.writerow(['rms'])
        spamwriter.writerow([str(xrms_f)])

    fig = plt.figure()
    ax_fig = fig.add_subplot(111)
    ax_fig.plot(t_i, x_i)
    ax_fig.set_ylabel('Acceleration (g)')
    ax_fig.set_xlabel('Time (s)')
    fig.savefig(csvFileLoc[:-4] + fileAdd + 'Fs' + str(fs_f) + 'Sw' + str(sampwidth) + 'CALIBRATION' + '.png')

def readWav(wavFileLoc):
    fs, data = scipy.io.wavfile.read(wavFileLoc)
    return fs, data
