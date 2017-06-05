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


class wavimportwindow(QtWidgets.QDialog, Ui_Dialog_wavimport):
    def __init__(self, parent=None):
        # Setup UI and signals
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)
        self.setupSignals()

        self.data = []  # Variable to store imported data
        self.file_loc = ''  # Variable to store file location
        self.timeScale = self.translateTimeUnits(
            self.unitTime_combo.currentText())  # Time scale of imported data
        self.accScale = self.translateAccUnits(
            self.unitAcc_combo.currentText())

    def setupSignals(self):
        self.import_button.clicked.connect(self.importData)
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
            # Custom class used to import data
            imptool = importTool()
            self.file_loc, file_extention = imptool.fileLoc()
            self.data, header = imptool.importTextFile(self.file_loc)

            # Writes a sample in header_label and data_table
            self.sample_edit.appendPlainText(header)
            ni, nj = np.shape(self.data)


            if ni > 20:
                sample_size = 20
            else:
                sample_size = ni

            self.data_table.setRowCount(sample_size + 1)
            self.data_table.setColumnCount(nj)
            for j in range(nj):
                for i in range(1, sample_size):
                    if data[i+1, j] < data[i, j]:
                        print('Hello')
            #for i in range(sample_size):
                #row_str = ''
                #for j in range(nj):
                    #row_str = row_str + str(self.data[i, j]) + ','
                #row_str = row_str[:-1]
                #self.sample_edit.appendPlainText(row_str)

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
        '''
        Translates units in time combo box to scalar
        '''
        timeScale = 0
        if string == 'ns':
            timeScale = 0.000001
        elif string == 'ms':
            timeScale = 0.001
        elif string == 's':
            timeScale = 1
        elif string == 'min':
            timeScale = 60
        elif string == 'h':
            timeScale = 3600
        elif string == 'custom':
            try:
                timeScale = float(self.scaleTime_edit.text())
            except Exception:
                timeScale = 0
        print('TimeScale ', timeScale)
        return(timeScale)

    def isTimeCustom(self, string):
        '''
        Checks if user has entered custom time scale and enables edit text if
        True.
        '''
        if string == 'custom':
            self.scaleTime_edit.setEnabled(True)
            self.isTimeCustom_checked = True
        else:
            self.scaleTime_edit.setEnabled(False)
            self.isTimeCustom_checked = False

    def getCustomTimeScale(self):
        '''
        Fetches the custom acceleration from edit text.
        '''
        try:
            self.timeScale = float(self.scaleTime_edit.text())
        except Exception:
            self.timeScale = 0
        print(self.timeScale)

    def translateAccUnits(self, string):
        '''
        Translates units in time acceleration combo box to scalar
        '''
        accScale = 0
        if string == 'g':
            accScale = 1
        elif string == 'ms^2':
            accScale = 1/9.81
        elif string == 'custom':
            try:
                accScale = float(self.scaleAcc_edit.text())
            except Exception:
                accScale = 0
        print('accScale ', accScale)
        return(accScale)

    def isAccCustom(self, string):
        '''
        Checks if user has entered custom acceleration scale and enables edit text if
        True.
        '''
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
