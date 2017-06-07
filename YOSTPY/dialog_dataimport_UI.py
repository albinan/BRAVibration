'''
Generic import dialog widget.
'''
from PyQt5 import QtWidgets
import sys
import numpy as np
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

        self.imptool = importTool()
        self.data = []  # Variable to store imported data
        self.file_loc = ''  # Variable to store file location
        self.na = 1  # Column with acceleration vector
        self.nt = 0  # Column with time vector
        self.scale_a = 1  # Scale factor acceleration
        self.scale_t = 1  # Scale factor time

    def setupSignals(self):
        self.import_button.clicked.connect(self.importData)
        self.unitTime_combo.currentTextChanged.connect(self.getTimeUnits)
        self.unitAcc_combo.currentTextChanged.connect(self.getAccUnits)
        self.columnTime_combo.currentTextChanged.connect(self.getColumnTime)
        self.columnAcc_combo.currentTextChanged.connect(self.getColumnAcc)

    def getColumnTime(self, string):
        '''
        Retrives current time column and recalculates sample frequency and
        total time of measurement
        '''
        print('getColumnTime')
        self.nt = int(string) - 1  # Column starting with 1
        self.writeParamTable()

    def getColumnAcc(self, string):
        '''
        Retrives current time column and recalculates sample frequency and
        total time of measurement
        '''
        print('getColumnAcc')
        self.na = int(string) - 1  # Column starting with 1
        self.writeParamTable()

    def importData(self):
        self.file_loc, file_extention = self.imptool.file_loc_UI()

    def importDelimited(self, file_loc):
        '''
        Imports csv or txt file and visualizes appropriate data and variables
        to determine the type of data
        '''
        try:
            # Custom class used to import data
            self.data, header = self.imptool.importDelimited(self.file_loc)
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
