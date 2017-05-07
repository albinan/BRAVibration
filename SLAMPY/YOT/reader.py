from PyQt5.QtWidgets import QApplication, QFileDialog
import sys
import os.path
import re
import csv
import numpy as np

def guiimport():
    # CSV or TXT file specifications
    regExp = r'\d+|\d+\.\d+'
    headerlines = 0

    dataFileLoc = fileImportDialog('*.csv') #Interactive file import
    dataFileName, extension = os.path.splitext(dataFileLoc)

    if extension == '.csv' or extension == '.txt':
        data, header = fscanf(dataFileLoc, regExp, headerlines)
        return data, header, dataFileLoc
    return 0

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
