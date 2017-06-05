from PyQt5.uic import loadUiType
from PyQt5 import QtWidgets, QtCore
import sys
import numpy as np
import time
import pyaudio
import os.path
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
sys.path.append('C:/Users/ReVibe/Documents/Albin/BRAVibration/LIB')
from playloop import WavePlayerLoop
from oscilloscope import Oscilloscope
from importdata0 import importTool
from fun import rootMeanSquare
from wavaio import readWav, writeWav
from scipy.fftpack import fft, fftfreq, fftshift
from scipy.signal import correlate, resample
from design_main import Ui_MainWindow as Ui_MainWindow_main
from main_wavimport import wavimportwindow


class mainwindow(QtWidgets.QMainWindow, Ui_MainWindow_main):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        self.wavFileLocations = []
        self.calibNumPeak = []
        self.calibNumRms = []
        self.actionOpen.triggered.connect(self.open_file)
        self.play_button.clicked.connect(self.play_signal)
        self.actionClear.triggered.connect(self.clear_files)
        self.actionCalibrate.triggered.connect(self.calibrate)
        self.actionExport_wav.triggered.connect(self.exportwav)
        self.play_list.currentItemChanged.connect(self.itemChanged)
        self.start_spin.valueChanged.connect(self.set_interval)
        self.start_spin.setMaximum(1000000000)
        self.stop_spin.valueChanged.connect(self.set_interval)
        self.stop_spin.setMaximum(1000000000)
        self.shouldIreallyspin = False
        self.scope = Oscilloscope(activeChannels=[1, 2])

    def set_interval(self):
        if self.shouldIreallyspin:
            try:
                self.t_start = self.start_spin.value()
                self.t_stop = self.stop_spin.value()
                n_start = np.argmin(np.abs(self.t_start-self.t_rec))
                n_stop = np.argmin(np.abs(self.t_stop-self.t_rec))
                self.a_rec_inval = self.a_rec[n_start:n_stop]
                self.t_rec_inval = self.t_rec[n_start:n_stop]

                self.n_rec = np.size(self.a_rec_inval)
                self.dt_rec = 1/self.fs_rec
                self.t_tot_rec = self.dt_rec*(self.n_rec-1)

                self.addsignalplot(self.t_rec_inval, self.a_rec_inval)
            except Exception as e:
                print(e)

    def itemChanged(self):
        try:
            #Calibrates data
            self.n_d = int(self.play_list.row(self.play_list.currentItem())) # Get current data in playlist
            if self.n_d == -1: # If nothing is selected, return 0 error
                return 0
            self.wavFileLoc = self.wavFileLocations[self.n_d] # Gets current Wavfile
            self.fs_rec, self.a_rec = readWav(self.wavFileLoc) # Reads wavfile
            self.a_rec = self.a_rec/np.max(np.abs(self.a_rec)) # formats

            self.a_rec = self.a_rec*self.calibNumPeak[self.n_d]
            self.n_rec = np.size(self.a_rec)
            self.dt_rec = 1/self.fs_rec
            self.t_tot_rec = self.dt_rec*(self.n_rec-1)
            self.t_rec = np.linspace(0, 1, self.n_rec)*self.t_tot_rec

            self.shouldIreallyspin = False
            self.start_spin.setValue(self.t_rec[0])
            self.stop_spin.setValue(self.t_rec[-1])
            self.shouldIreallyspin = True

            self.set_interval()

        except Exception as e:
            print(e)
    def exportwav(self):
        try:
            window = wavimportwindow()
            if window.exec_():
                window.writeWavFile()
        except Exception as e:
            print(e)

    def closeEvent(self):
        self.reject()

    def addsignalplot(self, t, a):
        self.fig_signal = plt.figure(figsize=(self.signal_fig.width()/150, self.signal_fig.height()/150), dpi=150)
        self.ax_signal = self.fig_signal.add_subplot(111)
        self.ax_signal.plot(t, a)
        self.ax_signal.set_xlim([t[0], t[-1]])
        self.ax_signal.set_xlabel('Time (s)')
        self.ax_signal.set_ylabel('Acceleration (g)')
        self.ax_signal.set_title('Recorded signal')
        self.ax_signal.grid(True, which='both')

        self.signalCanvas = FigureCanvas(self.fig_signal)
        self.signalCanvas.setParent(self.signal_fig)
        self.signalCanvas.draw()
        self.signalCanvas.show()
    def resetplot(self, t, a):
        self.addsignalplot(t, a)

    def open_file(self):
        imptool = importTool()
        self.file_loc, file_extention = imptool.fileLoc('*.wav')
        try:
            if self.file_loc != 0:
                self.wavFileLocations.append(self.file_loc)
                wavFileName = self.wavFileLocations[-1].split('/')[-1]
                print(wavFileName)
                item = QtWidgets.QListWidgetItem(wavFileName)
                self.play_list.addItem(item)
                calibLoc = self.wavFileLocations[-1][:-4] + 'CALIBRATION.csv'
                print(calibLoc)
                if os.path.isfile(calibLoc):
                    with open(calibLoc, 'r') as calibFile:
                        a = next(calibFile)
                        a = next(calibFile)
                        g_max = float(next(calibFile))
                        a = next(calibFile)
                        a = next(calibFile)
                        a = next(calibFile)
                        g_rms = float(next(calibFile))
                        print(calibLoc)
                        print(a)
                        print(g_max)
                else:
                    g_max, ok = QtWidgets.QInputDialog.getDouble(self, 'Manual Calibration', 'Enter maximum acceleration of meassurment')

                self.calibNumPeak.append(g_max)
                self.calibNumRms.append(g_rms)
                print('grms', g_rms)

        except Exception as e:
            print(e)

    def clear_files(self):
        self.wavFileLocations = []
        self.play_list.clear()

    def calibrate(self):
        try:
            eigfreq, ok = QtWidgets.QInputDialog.getInt(self,"Kalibrering 1","Skriv in approximativ egenfrekvens för harvestern")
            #calibWavFileLoc = 'PLAYPY/QTversion2/Calib/30Hz0.4vppCalibresampled_Fs8000.wav'
            #WPL_calib = WavePlayerLoop(calibWavFileLoc)
            #WPL_calib.play()
            self.scope.set_wavlength(0.5)

            n_d = int(self.play_list.row(self.play_list.currentItem()))
            QtWidgets.QMessageBox.about(
                self, 'Kalibrering 2',
                'Öka volym och förstärkning tills dess att accelerationen \n' +
                'är ' + str(self.calibNumPeak[n_d]*np.sqrt(2)/5) + 'V PEAK TO PEAK på oscilloscopet. \n'
                'Justera den vertikala skalan så att båda signalerna passar med lite marginal')
            p = pyaudio.PyAudio()

            volume = 0.2     # range [0.0, 1.0]
            fs = 44100       # sampling rate, Hz, must be integer
            duration = 120   # in seconds, may be float
            f = eigfreq        # sine frequency, Hz, may be float

            # generate samples, note conversion to float32 array
            samples = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)

            # for paFloat32 sample values must be in range [-1.0, 1.0]
            stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                output=True)

            # play. May repeat with different volume values (if done interactively)
            stream.write(volume*samples)

            stream.stop_stream()
            stream.close()

            p.terminate()
        except Exception as e:
            print(e)
            #WPL_calib.stop()
        #WPL_calib.stop()

    def play_signal(self):
        self.resetplot(self.t_rec_inval, self.a_rec_inval)
        try:
            # Playing signal in "length" sequences at the time
            overlap = 0.5  # Overlap between sequences in seconds
            length = 10  # Length of sequence in seconds
            t_init = self.t_rec_inval[0]
            t_stop = self.t_rec_inval[-1]
            flag = True  # Flag for looping sequences
            i = 0  # index for looping
            breakFlagWindow = False # Boolean used to replay the same signal if the window is too small.
            breakNoData = False # Boolean used to replay the same signal if failed to transfer data.
            breakEmptyArray = False
            breakDifferentArraySizes = False
            breakNoiseData = False
            a_rep_full = []  # Array with concatenated acceleration sequences in g
            t_rep_full = []  # Array with concatenated time sequences in seconds
            V_rep_full = []  # Array with concatenated measured voltage sequences
            self.scope.record_init(length, self.fs_rec)

            while flag:
                t_start = t_init + i*length - i*overlap
                print('t_start: ', t_start, 't_stop: ', t_start+length)
                # Recording data from oscilloscope.
                # data_rep[0][:, 0] contains time array
                # data_rep[0][:, 1] contains output voltage array
                # data_rep[1][:, 0] contains time array
                # data_rep[1][:, 1] contains acceleration array
                n_start_rec = np.argmin(np.abs(t_start - self.t_rec)) # Starting frame for the sequence
                n_stop_rec = np.argmin(np.abs(t_start+length - self.t_rec)) # Ending frame for the sequence
                Vpp_rec_int = 2*np.max(np.abs(self.a_rec[n_start_rec:n_stop_rec]))

                ## Playing signal once to adjust window size, then playing the same signal again
                self.scope.set_voltagescale(2*Vpp_rec_int, channel=2) # Setting acceleration scale to maximum of recorded signal
                self.scope.set_voltagescale(99999, channel=1) # Uncertenty about the voltage output. Setting window to maximum size.
                data_rep, timeStamp_rep = self.scope.record(self.wavFileLoc, t_start, length) # Recording signal
                print('Recording sampleRate: ', self.scope.get_sampleRate())
                # Signals are not formated to V. This loop is going through channels
                # 1 and 2 and formats according to measured RMS
                for j in range(0, 2):
                    data_rep[j][:, 1] = data_rep[j][:, 1] - np.mean(data_rep[j][:, 1]) # Removing mean from signal
                    q = self.scope.meas_RMS(channel=j+1) # Meassuring rms of signal
                    Vpp = self.scope.meas_VPP(channel=j+1) # Meassuring peak to peak voltage of signal
                    if Vpp > 99999: # If signal is outside window, Vpp is approx 1E37.
                        Vpp = self.scope.get_voltagescale(channel=j+1)
                        self.scope.set_voltagescale(Vpp, channel=j+1, margin=True) # Setting voltagescale to one less than it was before
                    else:
                        self.scope.set_voltagescale(Vpp, channel=j+1, margin=True)

                ## Playing signal again with corrected window size
                data_rep, timeStamp_rep = self.scope.record(self.wavFileLoc, t_start, length)

                fs_rep = self.scope.get_sampleRate() # Sample frequency of recorded signal
                dt_rep = 1/fs_rep
                n_length = int(np.round(length*fs_rep)) # Number of frames in signal (including overlap)
                n_overlap = int(np.round(overlap*fs_rep/2)) # Number of overlapping frames
                # Signals are not formated to V. This loop is going through channels
                # 1 and 2 and formats according to measured RMS
                for j in range(0, 2):
                    data_rep[j][:, 1] = data_rep[j][:, 1] - np.mean(data_rep[j][:, 1]) # Removing mean from signal
                    q = self.scope.meas_RMS(channel=j+1) # Measuring rms
                    Vpp = self.scope.meas_VPP(channel=j+1) # Measuring peak to peak voltage

                    # If the RMS could not be meassured the function returns -1.
                    # The cause is most likely that the window on the oscilloscope
                    # is too narrow. This raises a flag and the sequence will
                    # be replayed again. (The user gets to resize the window)
                    if q == -1:
                        print('Could not measure rms')
                        breakFlagWindow = True
                    elif np.size(data_rep[j][:, 1]) == 0:
                        print('Data array is empty')
                        breakNoData = True
                    #elif Vpp < 0.1:
                    #    breakNoiseData = True
                    else:
                        # Rescaling measured signal to have correct rms
                        rms = rootMeanSquare(data_rep[j][:, 1]) # Calculating rms from measured signal
                        q = q/rms
                        data_rep[j][:, 1] = data_rep[j][:, 1]*q

                if np.size(data_rep[1][:, 1]) != np.size(data_rep[0][:, 1]):
                    print('Different array sizes')
                    breakDifferentArraySizes = True

                # All the break flags fixes the appropriate issue and replays
                # the sequence
                if breakFlagWindow:
                    # Reducing windows size
                    for j in range(0, 2):
                        print(j)
                        Vpp = self.scope.meas_VPP(channel=j+1)
                        if Vpp > 100000:
                            Vpp = self.scope.get_voltagescale(channel=j+1)
                            self.scope.set_voltagescale(Vpp, channel=j+1, margin=True)
                        else:
                            self.scope.set_voltagescale(Vpp, channel=j+1, margin=True)
                    breakFlagWindow = False
                    breakNoData = False
                    breakDifferentArraySizes = False
                    breakNoiseData = False
                elif breakNoData or breakEmptyArray or breakDifferentArraySizes:
                    print('Trying again')
                    breakFlagWindow = False
                    breakNoData = False
                    breakDifferentArraySizes = False
                    breakNoiseData = False
                elif breakNoiseData:
                    print('Noise data')
                    if (t_start + length) > t_stop:
                        print('Flag is false')
                        flag = False
                    i = i + 1
                    breakFlagWindow = False
                    breakNoData = False
                    breakDifferentArraySizes = False
                    breakNoiseData = False
                else:
                    # Custom variables for more straight forward code
                    t_rep = data_rep[1][:, 0]  # Time array for replayed sequence in seconds
                    a_rep = data_rep[1][:, 1]  - np.mean(data_rep[1][:, 1])# Acceleration array for replayed sequence in g
                    V_rep = data_rep[0][:, 1] - np.mean(data_rep[0][:, 1]) # Output voltage array for replayed sequence

                    # Parameters for the replayed signal
                    t_tot_rep = t_rep[-1]-t_rep[0]
                    n_rep = np.size(t_rep)
                    fs_rep = 1/(t_tot_rep/(n_rep-1))

                    # Cross correlation is used to align the replayed sequences with the full
                    # recorded signals. For this to be done, the replayed signal need to have
                    # the same sample frequency as the recorded one. n_cross is the number of
                    # elements the replayed signal sequence should have in order to have the
                    # same sample frequency as the recorded signal
                    n_cross = self.fs_rec*t_tot_rep

                    # Resampling signal to n_cross elements
                    print('Resampling signal')
                    a_rep_cross = resample(a_rep, n_cross)
                    # Creating time array for resampled signal
                    t_rep_cross = np.linspace(0, 1, n_cross)*t_tot_rep

                    #http://stackoverflow.com/questions/19642443/use-of-pandas-shift-to-align-datasets-based-on-scipy-signal-correlate
                    # Its computationally expensive and unecessary to calculate the
                    # cross correlation between the replayed sequence and the entire
                    # recorded signal. We know that the replayed should align somewhere
                    # between t_start and t_start + length.
                    n_start_rec_cross = np.argmin(np.abs(t_start - self.t_rec_inval))
                    n_stop_rec_cross = np.argmin(np.abs((t_start+length)-self.t_rec_inval))

                    # t_shift is the time the replayed array should be shifted in order
                    # to match with the recorded signal.

                    print('Calculating time shift')
                    t_shift = (np.argmax(correlate(np.abs(self.a_rec_inval[n_start_rec_cross:n_stop_rec_cross]), np.abs(a_rep_cross))) - len(a_rep_cross) + n_start_rec_cross)*self.dt_rec
                    print('shift: ', t_shift)
                    t_break = t_start-t_shift-t_init
                    n = int(np.round(t_break*fs_rep))
                    n_rep = len(t_rep)


                    if n > np.size(t_rep):
                        print('Cant find sequence')
                        t_rep = np.linspace(0, 1, n_length-2*n_overlap)*(length-2*overlap) + t_end_check + dt_check
                        a_rep = np.zeros(np.size(t_rep))
                        V_rep = np.zeros(np.size(V_rep))
                    else:
                        t_rep = t_rep[n:]
                        t_rep = t_rep - t_rep[0]
                        t_rep = t_rep + t_start
                        a_rep = a_rep[n:]
                        V_rep = V_rep[n:]
                        t_rep = t_rep[:n_length]
                        a_rep = a_rep[:n_length]
                        V_rep = V_rep[:n_length]


                        if (t_start + length) > t_stop:
                            print('Flag is false')
                            flag = False
                            n_end = (self.t_tot_rec-t_start+t_init)*fs_rep
                            if i == 0:
                                t_rep = t_rep[:n_end]
                                a_rep = a_rep[:n_end]
                                V_rep = V_rep[:n_end]
                            else:
                                t_rep = t_rep[n_overlap:n_end]
                                a_rep = a_rep[n_overlap:n_end]
                                V_rep = V_rep[n_overlap:n_end]
                        elif i==0:
                            t_rep = t_rep[:-n_overlap]
                            a_rep = a_rep[:-n_overlap]
                            V_rep = V_rep[:-n_overlap]
                            print(t_start + length, t_stop)
                        else:
                            t_rep = t_rep[n_overlap:-n_overlap]
                            a_rep = a_rep[n_overlap:-n_overlap]
                            V_rep = V_rep[n_overlap:-n_overlap]

                        self.ax_signal.plot(t_rep, a_rep)
                        self.signalCanvas.draw()

                    t_rep_full.extend(t_rep)
                    a_rep_full.extend(a_rep)
                    V_rep_full.extend(V_rep)
                    i = i + 1
                #flag = False
            t_rep_full = np.asarray(t_rep_full)
            a_rep_full = np.asarray(a_rep_full)

            #if np.abs(t_rep_full[0] - self.t_start) > 1.5*dt_rep:
            #    print('First sequence empty')
            #    n_add_start = self.fs_rec*(t_rep_full[0] - self.t_start)
            #    t_add_start = np.linspace(0, 1)
            #if np.abs(t_rep_full[-1] - self.t_end) > 1.5*dt_rep:
            #    print('Last sequence empty')
            #a_rep_full = a_rep_full - np.mean(a_rep_full)
            #V_rep_full = np.asarray(V_rep_full)
            #V_rep_full = V_rep_full - np.mean(V_rep_full)

            np.savetxt(self.wavFileLoc[:-4] + str(time.strftime("%Y_%m_%d_%H_%M_%S", time.gmtime())) + '.csv'
                , np.transpose(np.vstack((t_rep_full, a_rep_full, V_rep_full)))
                , header='time(s),acc(g),output (V)'
                , delimiter=',')
            print('shapetrep: ', np.shape(t_rep_full))

            #fft_rep = []
            #print('datarec', np.shape(data_rep))
            #for i in range(0, np.shape(data_rep)[0]):
                # Fourier transform of recorded data for comparison
            #    dt_rep = t_rep_full[1] - t_rep_full[0]
            #    fft_rep.append(
            #        np.transpose(
            #            np.vstack((fftfreq(np.size(t_rep_full), dt_rep),
            #                       fft(a_rep_full)))))
            #    print('FFTSHAPE0', np.shape(fft_rep))
            # Calculating FFT for recorded signal
            #self.freq_rec = fftfreq(self.n_rec, self.dt_rec)
            #self.fft_rec = fft(self.a_rec_inval)
            #self.freq_rec = np.reshape(self.freq_rec, (self.n_rec, 1))
            #self.fft_rec = np.reshape(self.fft_rec, (self.n_rec, 1))
            #self.fft_rec = np.hstack((self.freq_rec, self.fft_rec))

            # Plotting
            #fig_signal = plt.figure(figsize=(8.27, 11.69), dpi=150)
            rms_rec = rootMeanSquare(self.a_rec_inval)
            #ax_recsignal = fig_signal.add_subplot(211)
            #ax_recsignal.plot(self.t_rec_inval, self.a_rec_inval,
            #                   label='RMS: ' + str(rms_rec))
            #ax_recsignal.grid(True)
            #ax_recsignal.set_title('Recorded signal')
            #ax_recsignal.set_xlim([self.t_rec_inval[0], self.t_rec_inval[-1]])
            #ax_recsignal.legend()
            #np.savetxt('Recorded.csv', [t_rec, a_rec], delimiter=',')
            #rms_rep = rootMeanSquare(a_rep_full)
            #ax_repsignal = fig_signal.add_subplot(212)
            rms_rep = rootMeanSquare(a_rep_full)
            #ax_repsignal.plot(t_rep_full, a_rep_full,
            #                  label='RMS: ' + str(rms_rep))
            #ax_repsignal.grid(True)
            #ax_repsignal.set_title('Replayed signal')
            #ax_repsignal.set_xlim([self.t_rec_inval[0], self.t_rec_inval[-1]])
            #ax_repsignal.legend()
            #print('saving')
            #np.savetxt('Replayed.csv', data_rep[1], delimiter=',')

            #fig_fft_comapre_g = plt.figure(figsize=(8.27, 11.69), dpi=150)
            #ax_recfft = fig_fft_comapre_g.add_subplot(111)
            #ax_recfft.plot(self.fft_rec[1:, 0], 20*np.log(np.abs(self.fft_rec[1:, 1])),
            #                    '.', label='Recorded')
            #ax_recfft.grid(True)
            #ax_recfft.set_title('Recorded and Replayed FFT')

            #ax_recfft.plot(fft_rep[1][1:, 0],
            #                20*np.log(np.abs(fft_rep[1][1:, 1])),
            #                '.', label='Replayed')
            #ax_recfft.grid(True)
            #ax_recfft.legend()
            #ax_recfft.set_xlim([0, 200])
            #ax_recfft.set_xlabel('Frequency (Hz)')
            #ax_recfft.set_ylabel('Acceleration (g)')

            # Meassured data
            #fig_fft_frequency_response = plt.figure(figsize=(8.27, 11.69), dpi=150)
            #fig_fft_frequency_response.suptitle('Recording at ' + str(int(np.round(100*rms_rep/rms_rec))) + '% signal strength', fontweight='bold', fontsize=14)
            #ax_rep_fft_g = fig_fft_frequency_response.add_subplot(211)
            #ax_rep_fft_g.plot(fftshift(fft_rep[1][:, 0]), fftshift(2*np.abs(fft_rep[1][:, 1])/np.size(fft_rep[1][:, 1])), linewidth=0.5)
            #ax_rep_fft_g.grid(True)
            #ax_rep_fft_g.set_title('DFT of input acceleration')
            #ax_rep_fft_g.set_ylabel('Acceleration (g)')
            #ax_rep_fft_g.set_xlim([0, 200])
            #ax_rep_fft_g.grid(b=True, which='major', linestyle='solid')
            #ax_rep_fft_g.grid(b=True, which='minor', linestyle='dashed', linewidth=0.2)

            #ax_rep_fft_V = fig_fft_frequency_response.add_subplot(212)
            #ax_rep_fft_V.plot(fftshift(fft_rep[0][:, 0]), fftshift(2*np.abs(fft_rep[0][:, 1])/np.size(fft_rep[0][:, 1])), linewidth=0.5, color='orange')
            #ax_rep_fft_V.grid(True)
            #ax_rep_fft_V.set_title('DFT of output voltage')
            #ax_rep_fft_V.set_ylabel('Voltage (V)')
            #ax_rep_fft_V.set_xlim([0, 200])
            #ax_rep_fft_V.set_xlabel('Frequency (Hz)')
            #ax_rep_fft_V.grid(b=True, which='major', linestyle='solid')
            #ax_rep_fft_V.grid(b=True, which='minor', linestyle='dashed', linewidth=0.2)
            #fig_fft_frequency_response.subplots_adjust(hspace=0.3)

            #ax_rep_fft_response = fig_fft_frequency_response.add_subplot(313)
            #H = np.abs(fft_rep[0][1:, 1])/np.abs(fft_rep[1][1:, 1])
            #rms_calib = rootMeanSquare(V_rep)
            #ax_rep_fft_response.plot(fft_rep[0][1:, 0], H, linewidth=0.5)
            #ax_rep_fft_response.grid(True)
            #ax_rep_fft_response.set_title('Frequency response')
            #ax_rep_fft_response.set_ylabel('Response (g/V)')
            #ax_rep_fft_response.set_xlabel('Frequency (Hz)')
            #ax_rep_fft_response.set_xlim([0, 200])
            #ax_rep_fft_response.set_ylim([0, 10*rms_calib])
            #fig_fft_frequency_response.subplots_adjust(hspace=1)

            fig_signal_response = plt.figure(figsize=(8.27, 11.69), dpi=150)
            rms_g = rms_rep
            fig_signal_response.suptitle('Recording at approx. ' + str(int(np.round(100*rms_rep/rms_rec))) + '% signal strength', fontweight='bold', fontsize=14)
            ax_signal_g = fig_signal_response.add_subplot(211)
            ax_signal_g.plot(t_rep_full, a_rep_full,
                              label='RMS: ' + str(rms_g) + ' g', linewidth=0.5)
            ax_signal_g.set_title('Replayed acceleration signal')
            ax_signal_g.set_ylabel('Acceleration (g)')
            ax_signal_g.legend(loc=2)
            ax_signal_g.set_xlim([self.t_start, self.t_stop])
            ax_signal_g.grid(b=True, which='major', linestyle='solid')
            ax_signal_g.grid(b=True, which='minor', linestyle='dashed', linewidth=0.2)

            ax_signal_V = fig_signal_response.add_subplot(212)
            rms_V = rootMeanSquare(V_rep)
            ax_signal_V.plot(t_rep_full, V_rep_full,
                              label='RMS: ' + str(rms_V) + ' V', linewidth=0.5, color='orange')
            ax_signal_V.set_title('Measured voltage signal')
            ax_signal_V.set_ylabel('Voltage (V)')
            ax_signal_V.set_xlabel('Time (s)')
            ax_signal_V.legend(loc=2)
            ax_signal_V.set_xlim([self.t_start, self.t_stop])
            ax_signal_V.grid(b=True, which='major', linestyle='solid')
            ax_signal_V.grid(b=True, which='minor', linestyle='dashed', linewidth=0.2)
            fig_signal_response.subplots_adjust(hspace=0.3)

            plt.show()



        except Exception as e:
            print(e)

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    GUI = mainwindow()
    GUI.show()

    sys.exit(app.exec_())
