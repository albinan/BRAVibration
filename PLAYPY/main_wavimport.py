'''
UI for importing acceleration data from txt or csv files and exporting
them as wav files, used to replay signals on vibration table
'''

from PyQt5 import QtWidgets
import sys
import numpy as np
sys.path.append('C:/Users/ReVibe/Documents/Albin/BRAVibration/LIB')
from importdata0 import importTool
from dialog_wavimport import Ui_Dialog as Ui_Dialog_wavimport
from wavaio import writeWav
from fun import fixtimedata, rootMeanSquare

class wavimportwindow(QtWidgets.QDialog, Ui_Dialog_wavimport):
    def __init__(self, parent=None):
        # Setup UI and signals
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)
        self.setupSignals()

        self.data = []  # Variable to store imported data
        self.file_loc = ''  # Variable to store file location
        self.na = 1  # Column with acceleration vector
        self.nt = 0  # Column with time vector
        self.scale_a = 1
        self.scale_t = 1

    def setupSignals(self):
        self.import_button.clicked.connect(self.importData)
        self.unitTime_combo.currentTextChanged.connect(self.translateTimeUnits)
        self.unitAcc_combo.currentTextChanged.connect(self.translateAccUnits)
        self.columnTime_combo.currentTextChanged.connect(self.getColumnTime)
        self.columnAcc_combo.currentTextChanged.connect(self.getColumnAcc)

    def getColumnTime(self, string):
        print('getColumnTime')
        self.nt = int(string) - 1
        self.writeParamTable()

    def getColumnAcc(self, string):
        print('getColumnAcc')
        self.na = int(string) - 1
        self.writeParamTable()

    def importData(self):
        '''
        Imports csv or txt file and visualizes appropriate data and variables
        to determine the type of data
        '''
        try:
            # Custom class used to import data
            imptool = importTool()
            self.file_loc, file_extention = imptool.file_loc_UI()
            self.data, header = imptool.importTextFile(self.file_loc)
            self.ni, self.nj = np.shape(self.data)
            self.translateTimeUnits(
                self.unitTime_combo.currentText())
            self.translateAccUnits(
                self.unitAcc_combo.currentText())

            # Writes a sample in header_label and data_table
            self.sample_edit.appendPlainText(header)
            self.writeDataTable()
        except Exception as e:
            print(e)

    def writeParamTable(self):
        try:

            self.parameters_table.setRowCount(2)
            self.parameters_table.setColumnCount(4)
            t = self.data[:, self.nt]*self.scale_t
            fixtimedata(t)
            a = self.data[:, self.na]*self.scale_a

            # Write sample frequency
            self.parameters_table.setItem(0, 0, QtWidgets.QTableWidgetItem('Sample frequency (Hz)'))
            fs = int(1/((t[-1] - t[0])/(len(t)-1)))
            self.parameters_table.setItem(1, 0, QtWidgets.QTableWidgetItem(str(fs)))
            # Write total time in minutes
            self.parameters_table.setItem(0, 1, QtWidgets.QTableWidgetItem('Total time (min)'))
            t_tot_min = int((t[-1] - t[0])/60)
            self.parameters_table.setItem(1, 1, QtWidgets.QTableWidgetItem(str(t_tot_min)))
            # Write rms
            self.parameters_table.setItem(0, 2, QtWidgets.QTableWidgetItem('RMS (g)'))
            g_rms = rootMeanSquare(a - np.mean(a))
            self.parameters_table.setItem(1, 2, QtWidgets.QTableWidgetItem(str(g_rms)))
            # Write peak to peak
            self.parameters_table.setItem(0, 3, QtWidgets.QTableWidgetItem('Peak to peak (g)'))
            g_p2p = np.max(a)-np.min(a)
            self.parameters_table.setItem(1, 3, QtWidgets.QTableWidgetItem(str(g_p2p)))
        except Exception as e:
            print(e)

    def writeDataTable(self):
        try:
            if self.ni > 10:
                sample_size = 10
            else:
                sample_size = self.ni
            self.data_table.setRowCount(sample_size + 1)
            self.data_table.setColumnCount(self.nj)
            isTime = True
            for j in range(self.nj):
                for i in range(1, sample_size):
                    if self.data[i+1, j] < self.data[i, j]:
                        isTime = False
                    self.data_table.setItem(i, j,
                                        QtWidgets.QTableWidgetItem(str(self.data[i,j])))
                if isTime:
                    self.data_table.setItem(0, j,
                                        QtWidgets.QTableWidgetItem('Time'))
                else:
                    self.data_table.setItem(0, j,
                                        QtWidgets.QTableWidgetItem('Acceleration'))
            self.columnAcc_combo.clear()
            self.columnTime_combo.clear()
            for i in range(self.nj):
                self.columnAcc_combo.addItem(str(i+1))
                self.columnTime_combo.addItem(str(i+1))
            # Initialize column combo boxes
            self.columnAcc_combo.setCurrentIndex(self.na)
            self.columnTime_combo.setCurrentIndex(self.nt)
            self.columnAcc_combo.setEnabled(True)
            self.columnTime_combo.setEnabled(True)
        except Exception as e:
            print(e)

    def translateTimeUnits(self, string):
        '''
        Translates units in time combo box to scalar
        '''
        scale_t = 0
        if string == 'ChipTimeUS':
            scale_t = 0.000001
        elif string == 'ns':
            scale_t = 0.000001
        elif string == 'ms':
            scale_t = 0.001
        elif string == 's':
            scale_t = 1
        elif string == 'min':
            scale_t = 60
        elif string == 'h':
            scale_t = 3600
        print('scale_t ', scale_t)
        self.scale_t = scale_t
        self.writeParamTable()

    def translateAccUnits(self, string):
        '''
        Translates units in time acceleration combo box to scalar
        '''
        scale_a = 0
        if string == 'g':
            scale_a = 1
        elif string == 'ms^2':
            scale_a = 1/9.81
        print('scale_a ', scale_a)
        self.scale_a = scale_a
        self.writeParamTable()

    def writeWavFile(self):
        print('File location: ', self.file_loc)
        print('Column with time data: ', self.nt)
        print('Column with acceleration data: ', self.na)
        print('Sample rate: ', self.fs)
        print('Scale factor time: ', self.scale_t)
        print('Scale factor acceleration', self.scale_a)
        t = self.data[:, self.nt]
        a = self.data[:, self.na]
        writeWav(
            t,
            a,
            self.file_loc,
            self.fs,
            self.scale_t,
            self.scale_a,
            )
        msg2 = QtWidgets.QMessageBox()
        msg2.setText('Finished writing wav file')
        msg2.exec_()
