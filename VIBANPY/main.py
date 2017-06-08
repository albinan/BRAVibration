from PyQt5 import QtWidgets
from main_window import Ui_MainWindow
import sys
import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft, fftfreq
from scipy.integrate import cumtrapz
from scipy.signal import spectrogram
import pandas as pd
sys.path.append('C:/Users/ReVibe/Documents/Albin/BRAVibration/LIB/dataImportUI')
sys.path.append('C:/Users/ReVibe/Documents/Albin/BRAVibration/LIB')
from linnearmodels import mod0001
from dialog_dataimport_UI import DataImportDialog
from fun import rootMeanSquare

class mainwindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        self.setupSignals()
        self.t = 0
        self.a = 0
        self.bandwidth_spin.setValue(5)
        self.maximumFrequency_spin.setRange(0, 999999999)
        self.maximumFrequency_spin.setValue(300)
        self.minimumFrequency_spin.setRange(0, 999999999)
        self.minimumFrequency_spin.setValue(25)
        self.figsize = (8.27, 11.69)
        self.color = [0.2, 0.2, 0.2]
    def setupSignals(self):
        self.import_button.clicked.connect(self.importData)
        self.analyze_button.clicked.connect(self.analyze)

    def importData(self):
        try:
            (t, a) = DataImportDialog.getData()
            print(np.shape(t))
            if np.shape(t) == ():
                print('No data')
            else:
                self.analyze_button.setEnabled(True)
                self.import_button.setEnabled(True)
                print('hello')
                self.t = t
                self.a = a
        except Exception as e:
            print(e)
    def analyze(self):
        try:
            t = self.t
            a = self.a
            if self.slice_check.isChecked():
                # Get subinterval from time data
                fig_getinval = plt.figure(figsize=self.figsize, dpi=100)
                ax_getinval = fig_getinval.add_subplot(111)
                ax_getinval.plot(t, a)
                ax_getinval.set_xlabel('Time (s)')
                ax_getinval.set_ylabel('Acceleration (g)')
                ax_getinval.set_title('Markera två punkter i grafen där signalen finns')
                t1, t2 = plt.ginput(2)
                plt.close(fig_getinval)
                n1 = np.argmin(np.abs(t-t1[0]))
                n2 = np.argmin(np.abs(t-t2[0]))
                if n1 > n2:
                    n1, n2 = n2, n1
                t = t[n1:n2]
                a = a[n1:n2]
            if np.mod(np.size(t), 2) != 0:  # Vector has to have even number of elements for fft indexing
                t = t[:-1]
                a = a[:-1]

            n = np.size(t)  # Redefining number of elements from new interval
            dt = (t[-1] - t[0])/(len(t)-1)
            fs = 1/dt  # Sampling frequency
            t_max = t[-1]
            t_min = t[0]
            freq = fftfreq(n, dt)  # Frequency spectrum
            freq_pos = freq[1:int(n/2)]  # Positive frequencies
            print('Removing mean')
            a = a - np.mean(a)
            print('Calculating rms')
            rms = rootMeanSquare(a)
            print('Calculating discrete fourier transform')
            afft = fft(a)
            print('Calculating acceleration spectral density')
            apsd = np.abs(afft)**2/(fs*n)
            apsd = 2*apsd[1:int(n/2)]
            print('Integrating psd')
            apsdintegral = np.sqrt(cumtrapz(apsd, freq[1:int(n/2)], initial=0))

            print('Initializing plot')
            titlesize = 16
            labelsize = 14
            fig_signal = plt.figure(figsize=(8.27, 11.69*2/3), dpi=100)
            ax_signal = fig_signal.add_subplot(111)
            print('Plotting time signal')
            ax_signal.plot(t, a,
                           label = 'Sample frequency: ' + str(round(fs)) + ' Hz\n' +
                           'RMS: ' + "{0:0.2f}".format(rms) + ' g\n' +
                           'Time of measurement: ' + "{:.2e}".format(t_max - t_min) + ' s', linewidth=0.25, color=self.color)

            ax_signal.grid(b=True, which='major', linestyle='solid')
            ax_signal.grid(b=True, which='minor', linestyle='dashed', linewidth=0.2)
            ax_signal.set_xlim(t_min, t_max)
            ax_signal.minorticks_on()
            ax_signal.set_title('Acceleration signal', fontsize=titlesize)
            ax_signal.set_xlabel('Time (s)', fontsize=labelsize)
            ax_signal.set_ylabel('Acceleration (g)', fontsize=labelsize)
            ymin, ymax = ax_signal.get_ylim()
            ax_signal.set_ylim(ymin, ymax*1.5)
            plt.legend(loc=2, ncol=2)

            print('Plotting PSD')
            fig_psd = plt.figure(figsize=self.figsize, dpi=100)
            ax_psd = fig_psd.add_subplot(311)
            ax_cumint = fig_psd.add_subplot(312)
            ax_psdbw = fig_psd.add_subplot(313)


            print('Plotting Model')
            fig_model = plt.figure(figsize=self.figsize, dpi=100)
            ax_inputspectrum = fig_model.add_subplot(311)
            ax_model = fig_model.add_subplot(312)
            ax_outputspectrum = fig_model.add_subplot(313)

            bw = self.bandwidth_spin.value()
            bw_rolling = 0.3
            mod = mod0001()

            n_bw = int(np.ceil(bw/(freq[1]-freq[0])))
            n_bw_rolling = int(np.round(bw_rolling/(freq[1]-freq[0])))
            if np.mod(n_bw, 2) != 0:
                n_bw = n_bw + 1

            print('Plotting PSD')
            ax_psd.semilogy(freq_pos, pd.rolling_mean(apsd, n_bw_rolling), linewidth=0.5, color=self.color)
            print('Plotting cummulative integral')
            line = ax_cumint.plot(freq_pos, apsdintegral, linewidth=1, color=self.color)
            ax_cumint.plot([0, np.max(freq_pos)], [rms, rms], linestyle='dashed', linewidth=1, color=self.color)
            print('Plotting PSDBW')
            psdbw = apsdintegral[int(n_bw):]-apsdintegral[:-int(n_bw)]
            fmin = self.minimumFrequency_spin.value()
            fmax = self.maximumFrequency_spin.value()
            print(fmin, fmax)
            nmin_interest = np.argmin(np.abs(freq_pos-fmin))
            nmax_interest = np.argmin(np.abs(freq_pos-fmax))
            print(nmin_interest, nmax_interest)
            if nmin_interest != nmax_interest:
                psdbw_max = np.max(psdbw[nmin_interest:nmax_interest])
            else:
                psdbw_max = np.max(psdbw)
            psdbw_nmax = np.argmin(np.abs(psdbw-psdbw_max))
            psdbw_fmax = freq_pos[psdbw_nmax+int(n_bw/2)]
            print('n_bw', n_bw)
            ax_psdbw.semilogy(freq_pos[int(n_bw/2):-int(n_bw/2)], psdbw, linewidth=0.5, label='Frequency of maximum: ' + str("{0:0.2f}".format(psdbw_fmax)) +' (Hz)' + '\n' + 'Integrated Acceleration: ' + "{0:0.3f}".format(psdbw_max)+' (g)', color=self.color)

            wmax = 2*np.pi*freq_pos[psdbw_nmax]
            kmax = wmax**2*mod.mass
            H = mod.H(freq, k=kmax)
            print('Calculating and plotting model')
            Vfft_pred = np.abs(H)*np.exp(1j*np.angle(H)*np.pi/180)*np.abs(afft)*np.exp(1j*np.angle(afft)*np.pi/180)
            print('1')
            Vpsd_pred = np.abs(Vfft_pred)**2/(n*fs)
            print('2')
            Vrms_pred = np.sqrt(np.trapz(Vpsd_pred, dx=freq_pos[2]-freq_pos[1]))
            print('3')
            Prms_pred = Vrms_pred**2/mod.testRload
            print('4')
            ax_inputspectrum.plot(freq_pos, pd.rolling_mean(2*np.abs(afft[1:int(n/2)]/n), n_bw_rolling), linewidth=0.5, color=self.color)
            print('5')
            ax_outputspectrum.plot(freq_pos, pd.rolling_mean(2*np.abs(Vpsd_pred[1:int(n/2)]), n_bw_rolling), label='Average power : ' +"{0:0.2f}".format(Prms_pred*1000)+' mW' , linewidth=0.5, color=self.color)
            print('6')
            ax_model.plot(freq_pos, 2*np.abs(H[1:int(n/2)]), label='Model V(jw)/g(jw)', linewidth=1, color=self.color)

            ax_psd.set_title('Acceleration Spectral Density', fontsize=titlesize)
            ax_psd.set_ylabel('ASD (g^2/Hz)', fontsize=labelsize)

            ax_psd.set_xlim(0, fmax)
            ax_psd.set_xticklabels([])
            ax_psd.grid(b=True, which='major', linestyle='solid')
            ax_psd.grid(b=True, which='minor', linestyle='dashed', linewidth=0.2)
            ax_psd.minorticks_on()
            print('6')
            ax_cumint.set_title('Integral of Acceleration Spectral Density', fontsize=titlesize)
            ax_cumint.set_ylabel('Acceleration (g)', fontsize=labelsize)
            ax_cumint.set_xlim(0, fmax)
            #ax_cumint.set_ylim(0, cumint_max*1.2)
            ax_cumint.set_xticklabels([])
            ax_cumint.grid(b=True, which='major', linestyle='solid')
            ax_cumint.grid(b=True, which='minor', linestyle='dashed', linewidth=0.2)
            ax_cumint.minorticks_on()
            print('7')
            ax_psdbw.set_title('Integral of ASD with ' + str(bw) +' Hz Bandwidth', fontsize=titlesize)
            ax_psdbw.set_ylabel('Acceleration (g)', fontsize=labelsize)
            ax_psdbw.set_xlabel('Frequency (Hz)', fontsize=labelsize)
            ax_psdbw.grid(b=True, which='major', linestyle='solid')
            ax_psdbw.grid(b=True, which='minor', linestyle='dashed', linewidth=0.2)
            ax_psdbw.set_xlim(0, fmax)
            ylim = ax_psdbw.get_ylim()
            ax_psdbw.minorticks_on()
            ax_psdbw.legend(loc=2)
            #for f in fmaxpsdbw:
            #    ax_psdbw.plot([f, f], [ylim[0], ylim[1]], color='k', linestyle='dashed', linewidth=1)


            print('8')
            ax_inputspectrum.set_title('Input spectrum (DFT)', fontsize=titlesize)
            ax_inputspectrum.set_ylabel('Acceleration (g)', fontsize=labelsize)
            ax_inputspectrum.grid(b=True, which='major', linestyle='solid')
            ax_inputspectrum.grid(b=True, which='minor', linestyle='dashed', linewidth=0.2)
            ax_inputspectrum.set_xlim(0, fmax)
            ax_inputspectrum.minorticks_on()
            ax_inputspectrum.set_xticklabels([])

            ax_model.set_title('Model of harvester', fontsize=titlesize)
            ax_model.set_ylabel('H(jw)=G(jw)/V(jw) (g/V)', fontsize=labelsize)
            ax_model.grid(b=True, which='major', linestyle='solid')
            ax_model.grid(b=True, which='minor', linestyle='dashed', linewidth=0.2)
            ax_model.set_xlim(0, fmax)
            ax_model.minorticks_on()
            ax_model.set_xticklabels([])

            ax_outputspectrum.set_title('Estimated output voltage over ' + str(mod.testRload) +' Ohm load', fontsize=titlesize)
            ax_outputspectrum.set_ylabel('Estimated voltage (V)', fontsize=labelsize)
            ax_outputspectrum.set_xlabel('Frequency (Hz)', fontsize=labelsize)
            ax_outputspectrum.grid(b=True, which='major', linestyle='solid')
            ax_outputspectrum.grid(b=True, which='minor', linestyle='dashed', linewidth=0.2)
            ax_outputspectrum.set_xlim(0, fmax)
            ymin, ymax = ax_outputspectrum.get_ylim()
            ax_outputspectrum.set_ylim(ymin, ymax*1.1)
            ax_outputspectrum.legend(loc=2, ncol=2)
            ax_outputspectrum.minorticks_on()

            #f, t2, Sxx = signal.spectrogram(x, Fs, nperseg = Fs/4)
            #fig_spectrogram = plt.figure(figsize=(8.27,11.69*2/3), dpi=100)
            #ax_spectrogram = fig_spectrogram.add_subplot(111)
            #ax_spectrogram.pcolormesh(t2, f, np.log(Sxx))
            #ax_spectrogram.set_ylabel('Frequency (Hz)')
            #ax_spectrogram.xlabel('Time (sec)')
            plt.show()

        except Exception as e:
            print(e)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    GUI = mainwindow()
    GUI.show()
    sys.exit(app.exec_())
