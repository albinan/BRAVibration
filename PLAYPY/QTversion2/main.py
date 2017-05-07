from PyQt5.uic import loadUiType
from PyQt5 import QtWidgets, QtCore
import sys
import numpy as np
import time
import os.path
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQT as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
sys.path.append('C:/Users/ReVibe/Documents/Albin/MasterSnake/LIB')
from playloop import WavePlayerLoop
from oscilloscope import Oscilloscope
from importdata import guiimport
from fun import rootMeanSquare, slices
from wavaio import readWav, writeWav
from scipy.fftpack import fft, fftfreq, fftshift
from design_main import Ui_MainWindow as Ui_MainWindow_main
from dialog_wavimport import Ui_Dialog as Ui_Dialog_wavimport


#Ui_MainWindow, QMainWindow = loadUiType('C:/Users/ReVibe/Documents/Albin/MasterSnake/PLAYPY/QTversion2/design.ui')
class wavimportwindow(QtWidgets.QDialog, Ui_Dialog_wavimport):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)
        self.import_button.clicked.connect(self.importData)
        self.slice_check.stateChanged.connect(self.isSlice)
        self.fs_combo.currentTextChanged.connect(self.getSampleRate)
        self.sliceMode_combo.currentIndexChanged.connect(self.whatSlice)
        self.unitTime_combo.currentTextChanged.connect(self.isTimeCustom)
        self.unitTime_combo.currentTextChanged.connect(self.translateTimeUnits)
        self.scaleTime_edit.textChanged.connect(self.getCustomTimeScale)
        self.unitAcc_combo.currentTextChanged.connect(self.isAccCustom)
        self.unitAcc_combo.currentTextChanged.connect(self.translateAccUnits)
        self.scaleAcc_edit.textChanged.connect(self.getCustomAccScale)

        self.columnTime_combo.currentTextChanged.connect(self.getColumnTime)
        self.columnAcc_combo.currentTextChanged.connect(self.getColumnAcc)
        self.isSlice_checked = False
        self.isSlicesAuto_checked = False
        self.isTimeCustom_checked = False
        self.isAccCustom_checked = False

        self.data = []
        self.fileLoc = ''
        self.fs = int(self.fs_combo.currentText())
        self.translateTimeUnits(
            self.unitTime_combo.currentText())
        self.translateAccUnits(
            self.unitAcc_combo.currentText())

        print(self.timeScale)
        self.nt = -1
        self.na = -1

    def getColumnTime(self, string):
        self.nt = int(string)

    def getColumnAcc(self, string):
        self.na = int(string)

    def importData(self):
        try:
            imptool = guiimport()
            self.data = imptool.importdata()
            header = imptool.header
            self.fileLoc = imptool.fileLoc
            self.sample_edit.appendPlainText(header)

            ni, nj = np.shape(self.data)
            if ni > 10:
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

            try:
                self.columnAcc_combo.setCurrentIndex(1)
                self.na = 1
                self.columnTime_combo.setCurrentIndex(0)
                self.nt = 0
                self.columnAcc_combo.setEnabled(True)
                self.columnTime_combo.setEnabled(True)
            except Exception as e:
                print(e)

        except Exception as e:
            print(e)

    def getSampleRate(self, text):
        self.fs = int(text)

    def isSlice(self, checked):
        self.isSlice_checked = checked
        if checked:
            self.sliceMode_combo.setEnabled(True)
        else:
            self.sliceMode_combo.setEnabled(False)

    def whatSlice(self, string):
        if int(string) != 0:
            self.slices_spin.setEnabled(True)
            self.isSlicesAuto_checked = True

    def translateTimeUnits(self, string):
        print('string', string)
        if string == 'ns':
            self.timeScale = 0.000001
            print('timesac', self.timeScale)
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

        print(self.timeScale)

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

        print(self.accScale)


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
        print('File location: ', self.fileLoc)
        print('Column with time data: ', self.nt)
        print('Column with acceleration data: ', self.na)
        print('Sample rate: ', self.fs)
        print('Scale factor time: ', self.timeScale)
        print('Scale factor acceleration', self.accScale)
        t = []
        a = []
        n_slice = 1
        if self.isSlice_checked:
            if self.isSlicesAuto_checked:
                n_slice = self.slices_spin.value()
                n_tot = np.size(self.data[:, self.nt])

                slice_size = int(np.floor(n_tot/n_slice))
                print('slicesize', slice_size)
                for i in range(n_slice):
                    t.append(self.data[i*slice_size:(i+1)*slice_size, self.nt])
                    a.append(self.data[i*slice_size:(i+1)*slice_size, self.na])

                    print(slice_size*(i+1)/n_tot)
                print('dasdasd', np.shape(a))
            else:
                plt.plot(
                    self.data[:, self.nt],
                    self.data[:, self.na])
                msg = QtWidgets.QMessageBox(self)
                msg.setText('Välj två tidspunkter')
                msg.exec_()

                t1, t2 = plt.ginput(2)
                n1 = np.argmin(np.abs(self.data[:, self.nt]-t1[0]))
                n2 = np.argmin(np.abs(self.data[:, self.nt]-t2[0]))
                if n1 > n2:
                    n1, n2 = n2, n1
                t = self.data[n1:n2, self.nt]
                a = self.data[n1:n2, self.na]
        else:
            t.append(self.data[:, self.nt])
            a.append(self.data[:, self.na])
        msg1 = QtWidgets.QMessageBox(self)
        msg1.setText('Writing .wav file. This can take some time...')
        msg1.exec_()

        for i in range(n_slice):
            print(i)
            print(np.shape(a[i]))
            try:
                writeWav(
                    t[i],
                    a[i],
                    self.fileLoc,
                    self.fs,
                    self.timeScale,
                    self.accScale,
                    fileAdd='tcol' + str(self.nt) + 'acol' + str(self.na) + 'Slice' + str(i))
            except Exception as e:
                print(e)
        msg2 = QtWidgets.QMessageBox()
        msg2.setText('Finished writing wav file')
        msg2.exec_()
class mainwindow(QtWidgets.QMainWindow, Ui_MainWindow_main):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        self.wavFileLocations = []
        self.calibNum = []
        self.actionOpen.triggered.connect(self.open_file)
        self.play_button.clicked.connect(self.play_signal)
        self.actionClear.triggered.connect(self.clear_files)
        self.actionCalibrate.triggered.connect(self.calibrate)
        self.actionExport_wav.triggered.connect(self.exportwav)
        self.scope = Oscilloscope(activeChannels=[1, 2])

    def exportwav(self):
        try:
            window = wavimportwindow()
            if window.exec_():
                window.writeWavFile()
        except Exception as e:
            print(e)
            #for i in a_col:
                #for slice_number in range(0, n_slices):
                    #print(i)
                    #print(slice_number, ' ', n_slices )
                    #print('shapedat', np.shape(data))
                    #t_tmp = slices(data[:, t_col], n_slices, slice_number)
                    #a_tmp = slices(data[:, int(i)], n_slices, slice_number)
                    #print('shapeslicedat', np.shape(a_tmp))
                    #writeWav(t_tmp, a_tmp, fileLoc, fs_f=fs, n_t=t_col, n_a=a_col, scale_t=t_scale, scale_a=a_scale, fileAdd=i+str(slice_number))

    def closeEvent(self):
        self.reject()
    def addsignalplot(self, fig):
        self.canvas = FigureCanvas(fig)
        self.canvas.setParent(self.signal_fig)
        self.canvas.draw()
    def clearsignalplot(self):
        print('asd')

    def open_file(self):
        imptool = guiimport()
        fileLoc = imptool.fileLocGUI('*.wav')
        try:
            if fileLoc != 0:
                self.wavFileLocations.append(fileLoc)
                wavFileName = self.wavFileLocations[-1].split('/')[-1]
                print(wavFileName)
                item = QtWidgets.QListWidgetItem(wavFileName)
                self.play_list.addItem(item)

                calibLoc = imptool.fileLocGUI('*.csv *.txt')
                if calibLoc == 0:
                    g_max, ok = QtWidgets.QInputDialog.getDouble(self, 'Manual Calibration', 'Enter maximum acceleration of meassurment')
                else:
                    with open(calibLoc, 'r') as calibFile:
                        a = next(calibFile)
                        a = next(calibFile)
                        g_max = float(next(calibFile))
                        print(calibLoc)
                        print(a)
                        print(g_max)
                self.calibNum.append(g_max)
        except Exception as e:
            print(e)




    def clear_files(self):
        self.wavFileLocations = []
        self.play_list.clear()

    def calibrate(self):
        try:
            calibWavFileLoc = 'PLAYPY/QTversion2/Calib/30Hz0.4vppCalibtcol0acol1Fs8000Sw4.wav'
            WPL_calib = WavePlayerLoop(calibWavFileLoc)
            WPL_calib.play()
            self.scope.set_wavlength(0.5)

            n_d = int(self.play_list.row(self.play_list.currentItem()))
            QtWidgets.QMessageBox.about(
                self, 'Kalibrering',
                'Kalibrering för: \n' +
                str(self.wavFileLocations[n_d]) + '\n'
                'Öka volym och förstärkning tills dess att accelerationen \n' +
                'är ' + str(self.calibNum[n_d]*np.sqrt(2)) + 'g PEAK TO PEAK på oscilloscopet.')

        except Exception as e:
            print(e)
            WPL_calib.stop()
        WPL_calib.stop()

    def play_signal(self):

        try:

            n_d = int(self.play_list.row(self.play_list.currentItem()))
            print(n_d)
            if n_d == -1:
                return 0
            self.scope.run()
            wavFileLoc = self.wavFileLocations[n_d]
            fs_m, data_m = readWav(wavFileLoc)
            data_m = data_m/np.max(np.abs(data_m))
            data_m = data_m*self.calibNum[n_d]
            n_m = np.size(data_m)
            dt_m = 1/fs_m
            t_tot_m = dt_m*(n_m-1)
            t_m = np.linspace(0, 1, n_m)*t_tot_m

            freq_m = fftfreq(n_m, dt_m)
            fft_m = fft(data_m)
            freq_m = np.reshape(freq_m, (n_m, 1))
            fft_m = np.reshape(fft_m, (n_m, 1))
            fft_m = np.hstack((freq_m, fft_m))
            print(np.shape(fft_m))
            WPL = WavePlayerLoop(wavFileLoc)
            print('playing')
            WPL.play()  # Playing the signal

            # Recording data from oscilloscope
            data_rec, timeStamp_rec = self.scope.record(t_tot_m, fs_m/10)

            timeStamp_play = WPL.stop()

            fft_rec = []
            print('datarec', np.shape(data_rec))
            for i in range(0, np.shape(data_rec)[0]):
                data_rec[i][:, 1] = data_rec[i][:, 1] - np.mean(data_rec[i][:, 1])
                q = self.scope.meas_RMS(
                    channel=self.scope.activeChannels[i]
                    )/rootMeanSquare(data_rec[i][:, 1])
                data_rec[i][:, 1] = data_rec[i][:, 1]*q
                # Fourier transform of recorded data for comparison
                dt_rec = data_rec[i][1, 0] - data_rec[i][0, 0]
                fft_rec.append(
                    np.transpose(
                        np.vstack((fftfreq(np.size(data_rec[i][:, 0]), dt_rec),
                                   fft(data_rec[i][:, 1])))))
                print('FFTSHAPE0', np.shape(fft_rec))

            fig_signal = plt.figure(figsize=(8.27, 11.69), dpi=150)
            rms_meas = rootMeanSquare(data_m)
            ax_meassignal = fig_signal.add_subplot(211)
            ax_meassignal.plot(t_m, data_m,
                               label='RMS: ' + str(rms_meas))
            ax_meassignal.grid(True)
            ax_meassignal.set_title('Recorded signal')
            ax_meassignal.legend()

            print(np.shape(data_rec))
            rms_rec = rootMeanSquare(data_rec[1][:, 1])
            ax_recsignal = fig_signal.add_subplot(212)
            ax_recsignal.plot(data_rec[1][:, 0], data_rec[1][:, 1],
                              label='RMS: ' + str(rms_rec))
            ax_recsignal.grid(True)
            ax_recsignal.set_title('Replayed signal')
            ax_recsignal.legend()

            fig_fft_comapre_g = plt.figure(figsize=(8.27, 11.69), dpi=150)
            ax_measfft = fig_fft_comapre_g.add_subplot(111)
            ax_measfft.plot(fft_m[1:, 0], 20*np.log(np.abs(fft_m[1:, 1])),
                                '.', label='Recorded')
            ax_measfft.grid(True)
            ax_measfft.set_title('Recorded and Replayed FFT')

            ax_measfft.plot(fft_rec[1][1:, 0],
                            20*np.log(np.abs(fft_rec[1][1:, 1])),
                            '.', label='Replayed')
            ax_measfft.grid(True)
            ax_measfft.legend()
            ax_measfft.set_xlim([0, 200])
            ax_measfft.set_xlabel('Frequency (Hz)')
            ax_measfft.set_ylabel('Acceleration (g)')

            # Meassured data
            fig_fft_frequency_response = plt.figure(figsize=(8.27, 11.69), dpi=150)
            fig_fft_frequency_response.suptitle('Recording at ' + str(int(np.round(100*rms_rec/rms_meas))) + '% signal strength', fontweight='bold', fontsize=14)
            ax_rec_fft_g = fig_fft_frequency_response.add_subplot(211)
            ax_rec_fft_g.plot(fftshift(fft_rec[1][:, 0]), fftshift(2*np.abs(fft_rec[1][:, 1])/np.size(fft_rec[1][:, 1])), linewidth=0.5)
            ax_rec_fft_g.grid(True)
            ax_rec_fft_g.set_title('DFT of input acceleration')
            ax_rec_fft_g.set_ylabel('Acceleration (g)')
            ax_rec_fft_g.set_xlim([0, 200])
            ax_rec_fft_g.grid(b=True, which='major', linestyle='solid')
            ax_rec_fft_g.grid(b=True, which='minor', linestyle='dashed', linewidth=0.2)

            ax_rec_fft_V = fig_fft_frequency_response.add_subplot(212)
            ax_rec_fft_V.plot(fftshift(fft_rec[0][:, 0]), fftshift(2*np.abs(fft_rec[0][:, 1])/np.size(fft_rec[0][:, 1])), linewidth=0.5, color='orange')
            ax_rec_fft_V.grid(True)
            ax_rec_fft_V.set_title('DFT of output voltage')
            ax_rec_fft_V.set_ylabel('Voltage (V)')
            ax_rec_fft_V.set_xlim([0, 200])
            ax_rec_fft_V.set_xlabel('Frequency (Hz)')
            ax_rec_fft_V.grid(b=True, which='major', linestyle='solid')
            ax_rec_fft_V.grid(b=True, which='minor', linestyle='dashed', linewidth=0.2)
            fig_fft_frequency_response.subplots_adjust(hspace=0.3)

            #ax_rec_fft_response = fig_fft_frequency_response.add_subplot(313)
            #H = np.abs(fft_rec[0][1:, 1])/np.abs(fft_rec[1][1:, 1])
            #rms_calib = rootMeanSquare(data_rec[0][:, 1])
            #ax_rec_fft_response.plot(fft_rec[0][1:, 0], H, linewidth=0.5)
            #ax_rec_fft_response.grid(True)
            #ax_rec_fft_response.set_title('Frequency response')
            #ax_rec_fft_response.set_ylabel('Response (g/V)')
            #ax_rec_fft_response.set_xlabel('Frequency (Hz)')
            #ax_rec_fft_response.set_xlim([0, 200])
            #ax_rec_fft_response.set_ylim([0, 10*rms_calib])
            #fig_fft_frequency_response.subplots_adjust(hspace=1)

            fig_signal_response = plt.figure(figsize=(8.27, 11.69), dpi=150)
            rms_g = rms_rec
            fig_signal_response.suptitle('Recording at ' + str(int(np.round(100*rms_rec/rms_meas))) + '% signal strength', fontweight='bold', fontsize=14)
            ax_signal_g = fig_signal_response.add_subplot(211)
            ax_signal_g.plot(data_rec[1][:, 0], data_rec[1][:, 1],
                              label='RMS: ' + str(rms_g) + ' g', linewidth=0.5)
            ax_signal_g.set_title('Replayed acceleration signal')
            ax_signal_g.set_ylabel('Acceleration (g)')
            ax_signal_g.legend(loc=2)
            ax_signal_g.set_xlim([data_rec[1][0, 0], data_rec[1][-1, 0]])
            ax_signal_g.grid(b=True, which='major', linestyle='solid')
            ax_signal_g.grid(b=True, which='minor', linestyle='dashed', linewidth=0.2)

            ax_signal_V = fig_signal_response.add_subplot(212)
            rms_V = rootMeanSquare(data_rec[0][:, 1])
            ax_signal_V.plot(data_rec[0][:, 0], data_rec[0][:, 1],
                              label='RMS: ' + str(rms_V) + ' V', linewidth=0.5, color='orange')
            ax_signal_V.set_title('Measured voltage signal')
            ax_signal_V.set_ylabel('Voltage (V)')
            ax_signal_V.set_xlabel('Time (s)')
            ax_signal_V.legend(loc=2)
            ax_signal_V.set_xlim([data_rec[0][0, 0], data_rec[0][-1, 0]])
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
