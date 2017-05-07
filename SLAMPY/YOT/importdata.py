from PyQt5 import QtWidgets
import re
import numpy as np


class guiimport():
    def __init__(self):
        super().__init__()
        self.data = []
        self.header = ''
        self.fileLoc = ''
        self.regExp = r'[+\-]?(?:0|[1-9]\d*)(?:\.\d*)?(?:[eE][+\-]?\d+)?'
        self.headerlines = 0
        self.filetype = '*.csv *.txt'

    def setRegExp(self, regExp):
        self.regExp = regExp

    def setHeaderlines(self, headerlines):
        self.headerlines = headerlines

    def importdata(self):

        self.fileLoc = QtWidgets.QFileDialog.getOpenFileName()
        print(self.fileLoc[0])

        with open(self.fileLoc[0]) as textfile:
            for i in range(0, self.headerlines):
                self.header = self.header + next(textfile)

            s = re.findall(self.regExp, next(textfile))
            a = [float(i) for i in s]
            n = np.size(a)
            counterx=0
            asd=[]
            for line in textfile:
                counterx=counterx+1
                s = re.findall(self.regExp, line)
                if np.size(a) != 4:
                    asd.append(counterx)
                a = [float(i) for i in s]
                self.data.extend(a)

        print('done')
        print(asd)
        data = np.asarray(self.data).reshape((counterx, n))
        print(data)
        print('1')
        return data
