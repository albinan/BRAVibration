from PyQt5 import QtWidgets
from dialog_dataimport import Ui_Dialog as ui_Dialog_dataimport
import sys
import numpy as np
sys.path.append('C:/Users/albin/OneDrive/Dokument/GitHub/BRAVibration/LIB')
from importdata0 import importTool


class dataImportWindow(QtWidgets.QDialog, ui_Dialog_dataimport):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)
        self.setupSignals()
        self.allowedFilextentions = ['.csv', '.txt', '.dat']
        self.dataSample = []
        self.initDisable()
    def initDisable(self):
        print('disable')
        self.fileExtention_edit.setEnabled(False)
    def setupSignals(self):
        self.import_but.clicked.connect(self.importData)
    def textEnable(self):
        print('ahello')
    def importData(self):
        try:
            impTool = importTool()
            file_loc, file_extention = impTool.fileLoc()
            if file_loc == '':
                return 0
            print(file_extention)
            if file_extention in self.allowedFilextentions:
                self.fileExtention_edit.setText(file_extention)
                if file_extention == '.csv' or '.txt':
                    self.dataSample, self.header = impTool.importTextFile(file_loc, sample=10)
            self.setSampleText(self.dataSample)
        except Exception as e:
            print(e)

    def setSampleText(self, data):
        sample = ''
        sample = sample + self.header
        for i in range(np.shape(data)[0]):
            for j in range(np.shape(data)[1]):
                sample = sample + str(data[i, j]) + ' , '
            sample = sample[:-2]
            sample = sample + '\n'
        self.sample_edit.setPlainText(sample)
def main():
    app = QtWidgets.QApplication(sys.argv)
    window = dataImportWindow()
    window.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()
