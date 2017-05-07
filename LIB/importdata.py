from PyQt5 import QtWidgets
import re
import numpy as np
import sys


class guiimport():
    def __init__(self):
        super().__init__()
        self.data = []
        self.header = ''
        self.fileLoc = ''
        self.regExp = r'[+\-]?(?:0|[1-9]\d*)(?:\.\d*)?(?:[eE][+\-]?\d+)?'
        self.headerlines = 1
        self.filetype = '*.csv *.txt'

    def setRegExp(self, regExp):
        self.regExp = regExp

    def setHeaderlines(self, headerlines):
        self.headerlines = headerlines

    def fileLocGUI(self, fileType):
        try:
            fileLoc = QtWidgets.QFileDialog.getOpenFileName(filter=fileType)[0]
            return fileLoc
        except Exception as e:
            return 0

    def importdata(self, fileLoc=''):
        if fileLoc == '':
            #app = QtWidgets.QApplication(sys.argv)
            self.fileLoc = QtWidgets.QFileDialog.getOpenFileName(filter=self.filetype)[0]
            print('Fileloc', self.fileLoc)
        else:
            self.fileLoc = fileLoc
        print('Importing data from: ', self.fileLoc)

        with open(self.fileLoc) as textfile:
            for i in range(0, self.headerlines):
                self.header = self.header + next(textfile)

            s = re.findall(self.regExp, next(textfile))
            a = [float(i) for i in s]
            n = np.size(a)
            counterx = 0

            for line in textfile:
                counterx = counterx + 1
                s = re.findall(self.regExp, line)
                a = [float(i) for i in s]
                self.data.extend(a)

        print('done')
        data = np.asarray(self.data).reshape((counterx, n))
        print(data)
        print('1')
        return data
