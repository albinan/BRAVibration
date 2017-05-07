from PyQt5.QtWidgets import QApplication, QFileDialog
import sys
import os.path
import re
from PyQt5 import QtWidgets
import csv
import numpy as np

class window(QtWidgets.Qwidget):
    # CSV or TXT file specifications
    def __init(self):
        super().__init__()
    #regExp = r'\d+|\d+\.\d+'
    #headerlines = 0
    #dataFileLoc = fileImportDialog('*.csv') #Interactive file import
    #dataFileName, extension = os.path.splitext(dataFileLoc)

    #if extension == '.csv' or extension == '.txt':
        #data, header = fscanf(dataFileLoc, regExp, headerlines)

    def fileImportDialog(fileType):
        app = QApplication(sys.argv)
        fileLoc = QFileDialog.getOpenFileName(filter=fileType)
        return fileLoc[0]
        sys.exit(app.exec_()) # Magic after return statement? Pls explain

def fscanf(dataFileLoc, regExp, headerlines=0):
    data =  []
    header = []
    with open(dataFileLoc) as textfile:
        for i in range(0, headerlines):
            header.append(next(textfile))
        for line in textfile:
            s = re.findall(regExp, line)
            a = [float(i) for i in s]
            data.append(a)
    data = np.asarray(data)
    return data, header



if __name__ == '__main__':
    app = QtWidgets.QApplication()
    a = window()
    a.show()
    sys.exit(app._exec())
