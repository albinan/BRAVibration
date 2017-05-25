from PyQt5.uic import loadUiType
from PyQt5 import QtWidgets, QtCore
import sys
import numpy as np
import time
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
from dialog_wavimport import Ui_Dialog as Ui_Dialog_wavimport


#Ui_MainWindow, QMainWindow = loadUiType('C:/Users/ReVibe/Documents/Albin/MasterSnake/PLAYPY/QTversion2/design.ui')
class wavimportwindow(QtWidgets.QDialog, Ui_Dialog_wavimport):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self)
        self.data = []
        self.setupUi(self)
        self.setupSignals()
        self.fs = int(self.fs_combo.currentText())
        self.translateTimeUnits(
            self.unitTime_combo.currentText())
        self.translateAccUnits(
            self.unitAcc_combo.currentText())

    def setupSignals(self):
        self.import_button.clicked.connect(self.importData)
        self.fs_combo.currentTextChanged.connect(self.getSampleRate)
        self.unitTime_combo.currentTextChanged.connect(self.isTimeCustom)
        self.unitTime_combo.currentTextChanged.connect(self.translateTimeUnits)
        self.scaleTime_edit.textChanged.connect(self.getCustomTimeScale)
        self.unitAcc_combo.currentTextChanged.connect(self.isAccCustom)
        self.unitAcc_combo.currentTextChanged.connect(self.translateAccUnits)
        self.scaleAcc_edit.textChanged.connect(self.getCustomAccScale)
        self.columnTime_combo.currentTextChanged.connect(self.getColumnTime)
        self.columnAcc_combo.currentTextChanged.connect(self.getColumnAcc)
        self.isTimeCustom_checked = False
        self.isAccCustom_checked = False

    def getColumnTime(self, string):
        self.nt = int(string)

    def getColumnAcc(self, string):
        self.na = int(string)

    def getSampleRate(self, string):
        self.fs = int(string)

    def importData(self):

        try:
            imptool = importTool()
            self.file_loc, file_extention = imptool.fileLoc()

            self.data, header = imptool.importTextFile(self.file_loc)

            self.sample_edit.appendPlainText(header)

            ni, nj = np.shape(self.data)
            for i in range(10):
                row_str = ''
                for j in range(nj):
                    row_str = row_str + str(self.data[i, j]) + ','
                row_str = row_str[:-1]
                self.sample_edit.appendPlainText(row_str)

            self.columnAcc_combo.clear()
            self.columnTime_combo.clear()
            for i in range(nj):
                self.columnAcc_combo.addItem(str(i))
                self.columnTime_combo.addItem(str(i))


            self.columnAcc_combo.setCurrentIndex(1)
            self.na = 1 # Column with acceleration vector
            self.columnTime_combo.setCurrentIndex(0)
            self.nt = 0 # Column with time vector
            self.columnAcc_combo.setEnabled(True)
            self.columnTime_combo.setEnabled(True)

        except Exception as e:
            print(e)

    def translateTimeUnits(self, string):
        print('string', string)
        if string == 'ns':
            self.timeScale = 0.000001
        elif string == 'ms':
            self.timeScale = 0.001
        elif string == 's':
            self.timeScale = 1
        elif string  == 'min':
            self.timeScale = 60
        elif string == 'h':
            self.timeScale = 3600
        elif string == 'custom':
            try:
                self.timeScale = float(self.scaleTime_edit.text())
            except Exception:
                self.timeScale = 0

        print('timeScale ', self.timeScale)

    def isTimeCustom(self, string):
        if string == 'custom':
            self.scaleTime_edit.setEnabled(True)
            self.isTimeCustom_checked = True
        else:
            self.scaleTime_edit.setEnabled(False)
            self.isTimeCustom_checked = False

    def getCustomTimeScale(self):
        try:
            self.timeScale = float(self.scaleTime_edit.text())
        except Exception:
            self.timeScale = 0
        print(self.timeScale)

    def translateAccUnits(self, string):
        if string == 'g':
            self.accScale = 1
        elif string == 'ms^2':
            self.accScale = 1/9.81
        elif string == 'custom':
            try:
                self.accScale = float(self.scaleAcc_edit.text())
            except Exception:
                self.accScale = 0

        print('accScale ', self.accScale)

    def isAccCustom(self, string):
        if string == 'custom':
            self.scaleAcc_edit.setEnabled(True)
            self.isAccCustom_checked = True
        else:
            self.scaleAcc_edit.setEnabled(False)
            self.isAccCustom_checked = False

    def getCustomAccScale(self):
        try:
            self.accScale = float(self.scaleAcc_edit.text())
        except Exception:
            self.accScale = 0
        print(self.accScale)

    def writeWavFile(self):
        print('File location: ', self.file_loc)
        print('Column with time data: ', self.nt)
        print('Column with acceleration data: ', self.na)
        print('Sample rate: ', self.fs)
        print('Scale factor time: ', self.timeScale)
        print('Scale factor acceleration', self.accScale)
        t = self.data[:, self.nt]
        a = self.data[:, self.na]
        writeWav(
            t,
            a,
            self.file_loc,
            self.fs,
            self.timeScale,
            self.accScale,
            )
        msg2 = QtWidgets.QMessageBox()
        msg2.setText('Finished writing wav file')
        msg2.exec_()

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
        print('hello')
        if self.shouldIreallyspin:
            print('adasdasdasdasda')
            try:
                self.t_start = self.start_spin.value()
                self.t_stop = self.stop_spin.value()
                n_start = np.argmin(np.abs(self.t_start-self.t_rec))
                n_stop = np.argmin(np.abs(self.t_stop-self.t_rec))
                self.a_rec_prime = self.a_rec[n_start:n_stop]
                self.t_rec_prime = self.t_rec[n_start:n_stop]

                self.n_rec = np.size(self.a_rec_prime)
                self.dt_rec = 1/self.fs_rec
                self.t_tot_rec = self.dt_rec*(self.n_rec-1)

                self.addsignalplot(self.t_rec_prime, self.a_rec_prime)
            except Exception as e:
                print(e)

    def itemChanged(self):
        print('WABALABADUBBDUBB')
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
        self.ax_signal.set_xlabel('Time (s)')
        self.ax_signal.set_ylabel('Acceleration (g)')
        self.ax_signal.set_title('Recorded signal')
        self.ax_signal.grid(True, which='both')

        self.signalCanvas = FigureCanvas(self.fig_signal)
        self.signalCanvas.setParent(self.signal_fig)
        self.signalCanvas.draw()
        self.signalCanvas.show()

    def clearsignalplot(self):
        print('asd')
    def ifprint(self, val):
        if self.isPrint:
            print(val)
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
            calibWavFileLoc = 'PLAYPY/QTversion2/Calib/30Hz0.4vppCalibresampled_Fs8000.wav'
            WPL_calib = WavePlayerLoop(calibWavFileLoc)
            WPL_calib.play()
            self.scope.set_wavlength(0.5)

            n_d = int(self.play_list.row(self.play_list.currentItem()))
            QtWidgets.QMessageBox.about(
                self, 'Kalibrering',
                'Kalibrering för: \n' +
                str(self.wavFileLocations[n_d]) + '\n'
                'Öka volym och förstärkning tills dess att accelerationen \n' +
                'är ' + str(self.calibNumPeak[n_d]) + 'V PEAK TO PEAK på oscilloscopet.')

        except Exception as e:
            print(e)
            WPL_calib.stop()
        WPL_calib.stop()

    def play_signal(self):
        self.isPrint = True
        try:
            # Playing signal in "length" sequences at the time
            overlap = 0.5  # Overlap between sequences in seconds
            length = 21  # Length of sequence in seconds
            t_init = self.t_rec_prime[0]
            t_stop = self.t_rec_prime[-1]
            flag = True  # Flag for looping sequences
            i = 0  # index for looping
            breakFlagWindow = False # Boolean used to replay the same signal if the window is too small.
            breakNoData = False # Boolean used to replay the same signal if failed to transfer data.
            a_rep_full = []  # Array with concatenated acceleration sequences in g
            t_rep_full = []  # Array with concatenated time sequences in seconds
            V_rep_full = []
            self.ifprint('Starting while loop')
            self.scope.record_init(length, self.fs_rec)
            while flag:
                t_start = t_init + i*length - i*overlap
                print('t_start: ', t_start, 't_stop: ', t_start+length)
                # Recording data from oscilloscope.
                # data_rep[0][:, 0] contains time array
                # data_rep[0][:, 1] contains output voltage array
                # data_rep[1][:, 0] contains time array
                # data_rep[1][:, 1] contains acceleration array

                data_rep, timeStamp_rep = self.scope.record(self.wavFileLoc, t_start, length)
                print('Recording sampleRate: ', self.scope.get_sampleRate())

                # Signals are not formated to V. This loop is going through channels
                # 1 and 2 and formats according to measured RMS
                for j in range(0, 2):
                    print(j)
                    data_rep[j][:, 1] = data_rep[j][:, 1] - np.mean(data_rep[j][:, 1])
                    q = self.scope.meas_RMS(channel=j+1)
                    Vpp = self.scope.meas_VPP(channel=j+1)
                    # If the RMS could not be meassured the function returns -1.
                    # The cause is most likely that the window on the oscilloscope
                    # is too narrow. This raises a flag and the sequence will
                    # be replayed again. (The user gets to resize the window)
                    if q == -1:
                        print('Could not measure rms')
                        breakFlagWindow = True
                    rms = rootMeanSquare(data_rep[j][:, 1])
                    print('rms: ', rms)
                    if data_rep[j][:, 1] == []:
                        print('Data array is empty')
                        breakNoData = True
                    else:
                        q = q/rms
                        data_rep[j][:, 1] = data_rep[j][:, 1]*q
                        print('rmsnew: ', rootMeanSquare(data_rep[j][:, 1]))

                if breakFlagWindow:
                    QtWidgets.QMessageBox.about(
                        self, 'Error','Ändra den vertikala skalan så att signalen får plats.')
                    breakFlagWindow = False
                elif breakNoData:
                    print('Trying again')
                    breakNoData = False
                elif Vpp < 0.5:
                    #if (t_start + length) > t_stop:
                    #    print('Flag is false')
                    #    flag = False
                    #    n_end = (self.t_tot_rec-t_start+t_init)*fs_rep
                    #    t_rep = t_rep[n_overlap:n_end]
                    #    t_rep = np.linspace(t_start + overlap, self.t_tot_rec-t_start+t_init, n_end)
                    #elif i==0:
                    #    t_rep = np.linspace(t_start, t_start + length-overlap, (t_start + length - overlap)*fs_rep)
                    #    print('EERRRR')
                    #    print(t_start + length, t_stop)
                    #else:
                    #    t_rep = np.linspace(t_start + overlap, t_start + length-overlap, (t_start + length - 2*overlap)*fs_rep)

                    #a_rep = np.zeros(np.shape(t_rep))
                    #V_rep = np.zeros(np.shape(t_rep))
                    #t_rep_full.extend(t_rep)
                    #a_rep_full.extend(a_rep)
                    #V_rep_full.extend(V_rep)
                    print('boop')
                else:
                    # Custom variables for more straight forward code
                    t_rep = data_rep[1][:, 0]  # Time array for replayed sequence in seconds
                    a_rep = data_rep[1][:, 1]  # Acceleration array for replayed sequence in g
                    V_rep = data_rep[0][:, 1]  # Output voltage array for replayed sequence

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
                    a_rep_cross = resample(a_rep, n_cross)
                    # Creating time array for resampled signal
                    t_rep_cross = np.linspace(0, 1, n_cross)*t_tot_rep

                    #http://stackoverflow.com/questions/19642443/use-of-pandas-shift-to-align-datasets-based-on-scipy-signal-correlate
                    # Its computationally expensive and unecessary to calculate the
                    # cross correlation between the replayed sequence and the entire
                    # recorded signal. We know that the replayed should align somewhere
                    # between t_start and t_start + length.
                    n_start = np.argmin(np.abs(t_start - self.t_rec_prime))
                    n_stop = np.argmin(np.abs((t_start+length)-self.t_rec_prime))

                    # Im not entirely sure why this works.
                    # t_shift is the time the replayed array should be shifted in order
                    # to match with the recorded signal.

                    # Fix this if statement later

                    t_shift = (np.argmax(correlate(self.a_rec_prime, a_rep_cross)) - len(a_rep_cross))*self.dt_rec
                    print('shift: ', t_shift)

                    t_break = t_start-t_shift-t_init
                    print('t_break: ', t_break)
                    n = int(np.round(t_break*fs_rep))
                    print('n:', n)
                    print(np.shape(t_rep))
                    print('111')
                    print(np.shape(t_rep))
                    t_rep = t_rep[n:]
                    t_rep = t_rep - t_rep[0]
                    t_rep = t_rep + t_start
                    a_rep = a_rep[n:]
                    V_rep = V_rep[n:]

                    n_rep = len(t_rep)
                    n_length = int(np.round(length*fs_rep))
                    print('112')
                    t_rep = t_rep[:n_length]
                    a_rep = a_rep[:n_length]
                    V_rep = V_rep[:n_length]

                    n_overlap = int(np.round(overlap*fs_rep/2))
                    if (t_start + length) > t_stop:
                        print('Flag is false')
                        flag = False
                        n_end = (self.t_tot_rec-t_start+t_init)*fs_rep
                        t_rep = t_rep[n_overlap:n_end]
                        a_rep = a_rep[n_overlap:n_end]
                        V_rep = V_rep[n_overlap:n_end]
                    elif i==0:
                        t_rep = t_rep[:-n_overlap]
                        a_rep = a_rep[:-n_overlap]
                        V_rep = V_rep[:-n_overlap]
                        print('EERRRR')
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
            a_rep_full = a_rep_full - np.mean(a_rep_full)
            V_rep_full = np.asarray(V_rep_full)
            V_rep_full = V_rep_full - np.mean(V_rep_full)
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
            #self.fft_rec = fft(self.a_rec_prime)
            #self.freq_rec = np.reshape(self.freq_rec, (self.n_rec, 1))
            #self.fft_rec = np.reshape(self.fft_rec, (self.n_rec, 1))
            #self.fft_rec = np.hstack((self.freq_rec, self.fft_rec))

            # Plotting
            #fig_signal = plt.figure(figsize=(8.27, 11.69), dpi=150)
            rms_rec = rootMeanSquare(self.a_rec_prime)
            #ax_recsignal = fig_signal.add_subplot(211)
            #ax_recsignal.plot(self.t_rec_prime, self.a_rec_prime,
            #                   label='RMS: ' + str(rms_rec))
            #ax_recsignal.grid(True)
            #ax_recsignal.set_title('Recorded signal')
            #ax_recsignal.set_xlim([self.t_rec_prime[0], self.t_rec_prime[-1]])
            #ax_recsignal.legend()
            #np.savetxt('Recorded.csv', [t_rec, a_rec], delimiter=',')
            #rms_rep = rootMeanSquare(a_rep_full)
            #ax_repsignal = fig_signal.add_subplot(212)
            rms_rep = rootMeanSquare(a_rep_full)
            #ax_repsignal.plot(t_rep_full, a_rep_full,
            #                  label='RMS: ' + str(rms_rep))
            #ax_repsignal.grid(True)
            #ax_repsignal.set_title('Replayed signal')
            #ax_repsignal.set_xlim([self.t_rec_prime[0], self.t_rec_prime[-1]])
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
            fig_signal_response.suptitle('Recording at approx.' + str(int(np.round(100*rms_rep/rms_rec))) + '% signal strength', fontweight='bold', fontsize=14)
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
