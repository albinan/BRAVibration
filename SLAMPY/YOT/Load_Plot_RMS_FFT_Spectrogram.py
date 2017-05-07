import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft
from scipy import signal
import tkinter as tk
from tkinter import filedialog
import time

def fftpsdspectrogram(t, acc):

    N = np.int(np.prod(t.shape))  # length of the array
    fs = 1/(t[1]-t[0])  # sample rate (Hz)
    Timestep = 1/fs

    # Compute and FFT
    freq_fft = np.linspace(0.0, 1.0/(2.0*Timestep), N/2)
    accfft = fft(acc)
    #absacc1side = 2.0/N*np.abs(yf[0:np.int(N/2)]))

    # Compute and Plot Spectrogram
	freq_spectrogram, t2, Sxx = signal.spectrogram(x, fs, nperseg = Fs/4)
	#plt.pcolormesh(t2, f, np.log(Sxx))
	#plt.ylabel('Frequency [Hz]')
	#plt.xlabel('Time [sec]')
	#plt.title('Spectrogram - ' + file_path)
