'''Application without GUI'''
import sys
import matplotlib.pyplot as plt
from scipy.fftpack import fft, fftfreq
from PyQt5 import QtWidgets
import numpy as np
import time
from scipy.signal import correlate
from scipy.integrate import cumtrapz
sys.path.append('C:/Users/ReVibe/Documents/Albin/MasterSnake/LIB')
from playloop import WavePlayerLoop
from oscilloscope import Oscilloscope
from importdata import guiimport
from fun import rootMeanSquare


def main():
    # _m stands for meassured data from a data-logger
    # _rec stands for data recorded from oscilloscope
    imptool = guiimport()
    # Import meassured data from txt file
    textFileLoc = 'C:/Users/ReVibe/Documents/Albin/MasterSnake/PLAYPY/write_wav_Matlab/data/SKF/CTO0036__ch05/SKF0036_ch05_v83.csv'
    wavFileLoc = 'C:/Users/ReVibe/Documents/Albin/MasterSnake/PLAYPY/write_wav_Matlab/data/SKF/CTO0036__ch05/SKF0036_ch05_v83.wav'
    calibWavFileLoc = 'C:/Users/ReVibe/Documents/Albin/MasterSnake/PLAYPY/write_wav_Matlab/data/CALIB/50Hz04ppCalib.wav'
    scope = Oscilloscope(activeChannels=[1, 2])  # Create oscilloscope instance
    scope.set_wavlength(0.5)
    #scope.set_voltagescale(1, 2)
    WPL_calib = WavePlayerLoop(calibWavFileLoc)
    WPL_calib.play()
    print('Increase volume and/or amplification level until g peak to peak is 0.4 g')
    #input("Press Enter to continue...")
    print('')
    time.sleep(5)
    data = scope.snapshot()
    plt.plot(data[:, 0], data[:, 1])
    plt.show()
    WPL_calib.stop()

    # Import meassured data from textfile
    data_m = imptool.importdata(textFileLoc)
    dt_m = data_m[1, 0] - data_m[0, 0]
    fs_m = 1/dt_m
    scope.set_sampleRate(10*fs_m)
    t_tot_m = data_m[-1, 0] - data_m[1, 0]
    fft_m = np.transpose(
                         np.vstack((fftfreq(np.size(data_m[:, 1]), dt_m),
                                    fft(data_m[:, 1]))))

    # Initiate and play signal
    WPL = WavePlayerLoop(wavFileLoc)
    WPL.play()  # Playing the signal

    # Recording data from oscilloscope
    data_rec, timeStamp_rec = scope.record(t_tot_m)

    # Stop playing signal after measurement
    timeStamp_play = WPL.stop()

    # Frequency spectrum of recorded data
    fft_rec = []
    for i in range(0, np.shape(data_rec)[0]):
        data_rec[i][:, 1] = data_rec[i][:, 1] - np.mean(data_rec[i][:, 1])
        q = scope.meas_RMS(
            channel=scope.activeChannels[i]
            )/rootMeanSquare(data_rec[i][:, 1])
        data_rec[i][:, 1] = data_rec[i][:, 1]*q
        # Fourier transform of recorded data for comparison
        dt_rec = data_rec[i][1, 0] - data_rec[i][0, 0]
        fft_rec.append(
            np.transpose(
                np.vstack((fftfreq(np.size(data_rec[i][:, 0]), dt_rec),
                           fft(data_rec[i][:, 1])))))
        print(np.shape(fft_rec))

    V_win1 = scope.get_voltagescale(1)
    V_win2 = scope.get_voltagescale(2)

    #cross_correlation = correlate(data_m[:, 1], data_rec[:, 1])
    #plt.plot(cross_correlation)


    fig_signal = plt.figure(figsize=(8.27, 11.69), dpi=150)
    ax_meassignal = fig_signal.add_subplot(211)
    ax_meassignal.plot(data_m[:, 0], data_m[:, 1],
                       label='RMS: ' + str(rootMeanSquare(data_m[:, 1])))
    ax_meassignal.grid(True)
    ax_meassignal.set_title('Meassured signal')
    ax_meassignal.legend()

    print(np.shape(data_rec))
    ax_recsignal = fig_signal.add_subplot(212)
    ax_recsignal.plot(data_rec[1][:, 0], data_rec[1][:, 1],
                      label='RMS: ' + str(rootMeanSquare(data_rec[1][:, 1])))
    ax_recsignal.grid(True)
    ax_recsignal.set_title('Recorded signal')
    ax_recsignal.legend()

    fig_fft = plt.figure(figsize=(8.27, 11.69), dpi=150)
    ax_measfft = fig_fft.add_subplot(111)
    ax_measfft.plot(fft_m[1:, 0], 20*np.log(np.abs(fft_m[1:, 1])/np.max(np.abs(fft_m[1:, 1]))),
                    '.', label='Meassured')
    ax_measfft.grid(True)
    ax_measfft.set_title('Meassured and Recorded FFT')

    ax_measfft.plot(fft_rec[1][1:, 0],
                    20*np.log(np.abs(fft_rec[1][1:, 1])/np.max(np.abs(fft_rec[1][1:, 1]))),
                    '.', label='Recorded')
    ax_measfft.grid(True)
    ax_measfft.legend()
    ax_measfft.set_xlim([0, 200])
    scope.terminate()
    plt.show()

if __name__ == '__main__':
    main()
