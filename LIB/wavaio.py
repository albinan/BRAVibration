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
from importdata import guiimport
from fun import rootMeanSquare
import scipy.io.wavfile
import struct


def writeWav(t_i, x_i, csvFileLoc, fs_f=41000, scale_t=1, scale_a=1, fileAdd=''):
    x_i = (x_i - np.mean(x_i))*scale_a
    t_i = (t_i - t_i[0])*scale_t


    # Parameters for initial signal
    dt_i = t_i[1]-t_i[0]
    fs_i = 1/dt_i
    n_i = np.size(t_i)
    rms_i = rootMeanSquare(x_i)

    # Resample time vector in case of strange data
    t_i = np.linspace(0, 1, n_i)*dt_i*(n_i-1)
    t_tot = t_i[-1]
    print(t_tot)
    # Parameters for final signal
    n_f = np.round(t_tot*fs_f)
    delta_n = n_f - n_i

    if np.mod(delta_n, 2) == 1:
        delta_n = delta_n - 1

    print('Calculating FFT...')
    x_fft_i = fftshift(fft(x_i))
    print('nf', n_f, 'ni', n_i)
    if n_f > n_i:
        print('Padding...')
        x_fft_f = np.pad(
            x_fft_i,
            pad_width=int(delta_n/2),
            mode='constant',
            constant_values=0)
        print('Calculating IFFT...')
        x_f = ifft(ifftshift(x_fft_f))
        x_f = x_f.real
        rms_f = rootMeanSquare(x_f)
        x_f = x_f*(rms_i/rms_f)
        t_f = np.linspace(0, 1, np.size(x_f))*t_tot
    if n_f < n_i:
        x_fft_f = x_fft_i[int(n_f/2):-int(n_f/2)]

        x_f = ifft(ifftshift(x_fft_f))
        x_f = x_f.real
        rms_f = rootMeanSquare(x_f)
        x_f = x_f*(rms_i/rms_f)
        t_f = np.linspace(0, 1, np.size(x_f))*t_tot

    print('Sample Frequency initial: ', fs_i)
    print('Sample Frequency final: ', 1/(t_f[1]-t_f[0]))
    print('wavFileLoc: ', csvFileLoc[:-4] + '.wav')
    print('Writing wav file...')
    sampwidth = 4
    plt.plot(t_f, x_f)
    plt.show()
    x_i_max = np.max(np.abs(x_i))
    x_f_max = np.max(np.abs(x_f))
    x_f_scaled = np.int16((x_f/x_f_max) * 32767)
    scipy.io.wavfile.write(csvFileLoc[:-4] + fileAdd + 'Fs' + str(fs_f) + 'Sw' + str(sampwidth) + '.wav', fs_f, x_f_scaled)

    with open(csvFileLoc[:-4] + fileAdd + 'Fs' + str(fs_f) + 'Sw' + str(sampwidth) + 'CALIBRATION' + '.csv', 'w') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')
        spamwriter.writerow(['g_max'])
        spamwriter.writerow([str(x_i_max)])

    fig = plt.figure()
    ax_fig = fig.add_subplot(111)
    ax_fig.plot(t_i, x_i)
    ax_fig.set_ylabel('Acceleration (g)')
    ax_fig.set_xlabel('Time (s)')
    fig.savefig(csvFileLoc[:-4] + fileAdd + 'Fs' + str(fs_f) + 'Sw' + str(sampwidth) + 'CALIBRATION' + '.png')

def readWav(wavFileLoc):
    fs, data = scipy.io.wavfile.read(wavFileLoc)
    print(fs)
    print(data)
    return fs, data

#imptool = guiimport()
#fileLoc = 'PLAYPY/QTversion2/Calib/30Hz0.4vppCalib.csv'
#data_csv = imptool.importdata(fileLoc)
#plt.plot(data[:,0], data[:,1])
#plt.show()

#writeWav(data_csv[:, 0], data_csv[:, 1], fileLoc, 8000, scale_t=1, n_a=3)

#fs, data_wav = scipy.io.wavfile.read('PLAYPY/QTversion2/Calib/30Hz0.4vppCalibFs8000ScipySw4.wav')


#plt.subplot(211)
#plt.plot(data_csv[:, 1])

#plt.subplot(212)
#plt.plot(data_wav)

#plt.show()
