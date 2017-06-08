'''
Generic import dialog widget.
'''
from PyQt5 import QtWidgets
import sys
import numpy as np
import matplotlib.pyplot as plt
sys.path.append('C:/Users/ReVibe/Documents/Albin/BRAVibration/LIB')
from importdata0 import importTool
from dialog_dataimport import Ui_Dialog
from wavaio import writeWav
from fun import fixtimedata, rootMeanSquare


class DataImportDialog(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        # Setup UI and signals
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)
        self.setupSignals()
        #self.createTime = False
        self.imptool = importTool()
        self.data = []  # Variable to store imported data
        self.file_loc = ''  # Variable to store file location
        self.na = 0  # Column with acceleration vector
        self.nt = 0  # Column with time vector
        self.scale_a = 1  # Scale factor acceleration
        self.scale_t = 0.000001  # Scale factor time
        #self.sampleFrequency_Spin.setRange(1, 9999999)

    def setupSignals(self):
        self.import_button.clicked.connect(self.importData)
        self.unitTime_combo.currentTextChanged.connect(self.getTimeUnits)
        self.unitAcc_combo.currentTextChanged.connect(self.getAccUnits)
        self.columnTime_combo.currentTextChanged.connect(self.getColumnTime)
        self.columnAcc_combo.currentTextChanged.connect(self.getColumnAcc)
        self.sampleFrequency_Spin.valueChanged.connect(self.sampleRateChanged)

    def getTimeUnits(self, string):
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

    def getAccUnits(self, string):
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

    def getColumnTime(self, string):
        '''
        Retrives current time column and recalculates sample frequency and
        total time of measurement
        '''
        print('getColumnTime')
        self.nt = int(string) - 1  # Column starting with 1
        print('nt', self.nt)
        self.writeParamTable()

    def getColumnAcc(self, string):
        '''
        Retrives current time column and recalculates sample frequency and
        total time of measurement
        '''
        print('getColumnAcc')
        self.na = int(string) - 1  # Column starting with 1
        print('na', self.na)
        self.writeParamTable()

    def writeParamTable(self):
        try:
            #if not self.createTime:
            t = self.data[:, self.nt]*self.scale_t
            fixtimedata(t)
            #else:
                #print('Custom time vector')
                #t = self.getSampleRateTimeVector()
                #self.sampleFrequency_Spin.setEnabled(True)
            a = self.data[:, self.na]*self.scale_a

            # Write sample frequency
            fs = int(1/((t[-1] - t[0])/(len(t)-1)))
            self.sampleFrequency_edit.setText(str(fs))
            # Write total time in minutes
            t_tot_min = int((t[-1] - t[0])/60)
            self.timeOfMeasurement_edit.setText(str(t_tot_min))
            # Write rms
            g_rms = rootMeanSquare(a-np.mean(a))
            self.rms_edit.setText(str(g_rms))

        except Exception as e:
            print(e)

    def importData(self):
        '''
        Imports csv, txt or dat file and calculates appropriate
        variables to determine scale factor and the type of data.
        '''
        self.status_label.setText('Status: Loading data')
        try:
            self.file_loc, self.file_extention = self.imptool.file_loc_UI()
            print(self.file_extention)
            if self.file_extention == '.csv' or self.file_extention == '.txt':
                self.activateDelimited()
                self.importDelimited()
        except Exception as e:
            print(e)

    def activateDelimited(self):
        try:
            self.fileExtention_edit.setText('.csv')
            self.header_edit.setEnabled(True)
            self.data_table.setEnabled(True)
            self.unitAcc_combo.setEnabled(True)
            self.unitTime_combo.setEnabled(True)
            self.OK_buttonBox.setEnabled(True)
            self.slice_check.setEnabled(True)
        except Exception as e:
            print(e)

    def importDelimited(self):
        '''
        Imports delimited text file
        '''
        try:
            # Custom class used to import data
            self.data, header = self.imptool.importDelimited(self.file_loc)
            self.ni, self.nj = np.shape(self.data)
            # Writes a sample in header_label and data_table
            self.header_edit.appendPlainText(header)
            self.writeDataTable()
        except Exception as e:
            print(e)

    def writeDataTable(self):
        '''
        Writes data to data_table if data is not empty
        '''
        try:
            if self.ni > 100:
                sample_size = 100
            else:
                sample_size = self.ni
            self.data_table.setRowCount(sample_size + 1)
            self.data_table.setColumnCount(self.nj)
            self.isTime = True  # Assuming time vector exists
            #self.createTime = True
            for j in range(self.nj):
                for i in range(1, sample_size):
                    if self.data[i+1, j] < self.data[i, j]:
                        self.isTime = False

                    self.data_table.setItem(i, j,
                                            QtWidgets.QTableWidgetItem(str(self.data[i, j])))
                if self.isTime:
                    self.data_table.setItem(0, j,
                                            QtWidgets.QTableWidgetItem('Time'))
                    self.nt = j
                    #self.createTime = False
                else:
                    self.data_table.setItem(0, j,
                                            QtWidgets.QTableWidgetItem('Acceleration'))

            # If time vector does not exist, sample frequency is needed to
            # import data
            # if self.isTime:
            #     self.sampleFrequency_Spin.setEnabled(True)

            self.columnAcc_combo.clear()
            for i in range(self.nj):
                self.columnAcc_combo.addItem(str(i+1))
            # Initialize column combo boxes
            self.columnAcc_combo.setEnabled(True)
            self.columnAcc_combo.setCurrentIndex(self.na)

            # if not self.createTime:
            self.columnTime_combo.clear()
            for i in range(self.nj):
                self.columnTime_combo.addItem(str(i+1))
            self.columnTime_combo.setEnabled(True)
            self.columnTime_combo.setCurrentIndex(self.nt)

            self.status_label.setText('Status:')
        except Exception as e:
            print(e)

    def sampleRateChanged(self):
        self.writeParamTable()

    def getSampleRateTimeVector(self):
        fs = self.sampleFrequency_Spin.value()
        print('fs', fs)
        t_tot = (1/fs)*self.nj
        t = np.linspace(0, 1, self.nj)*t_tot
        plt.plot(t)
        plt.show()
        return t

    def finalData(self):
        if self.OK_buttonBox.isEnabled():
            #if not self.createTime:
            t = self.data[:, self.nt]*self.scale_t
            fixtimedata(t)
            #else:
                #print('Custom time vector')
                #t = self.getSampleRateTimeVector()
            a = self.data[:, self.na]*self.scale_a

            if self.slice_check.isChecked():
                # Get subinterval from time data
                fig_getinval = plt.figure(dpi=100)
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
            return (t, a)
        else:
            return(0, 0)

    # static method to create the dialog and return (date, time, accepted)
    @staticmethod
    def getData(parent = None):
        dialog = DataImportDialog(parent)
        dialog.exec_()
        (t, a) = dialog.finalData()
        return (t, a)
