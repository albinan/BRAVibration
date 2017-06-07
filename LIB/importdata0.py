'''
Tools for importing arbitrary data files
'''
from PyQt5 import QtWidgets
import re
import numpy as np
import os


class importTool():
    def __init__(self):
        super().__init__()
        self.regExpNum = r'[+\-]?(?:0|[1-9]\d*)(?:\.\d*)?(?:[eE][+\-]?\d+)?'
        self.regExpHeader = r'[a-df-zA-DF-Z]'

    def file_loc_UI(self, fileType=None):
        '''
        Simple function that opens UI to retrive file location
        '''
        try:
            file_loc, _ = QtWidgets.QFileDialog.getOpenFileName(filter=fileType)
            _, file_extension = os.path.splitext(file_loc)
            return file_loc, file_extension
        except Exception as e:
            print(e)
            return 0

    def importBinary(self, fileLoc, dataFormat):
        print('in the making')

    def importDelimited(self, fileLoc, sample=0):
        '''
        Imports arbitrary text file containing header and numbers
        '''
        data = []
        header = ''
        with open(fileLoc) as textfile:
            for line in enumerate(textfile):
                if line[0] > sample and sample != 0:
                    break
                if re.search(self.regExpHeader, line[1]):
                    header = header + line[1] + '\n'
                else:
                    s = re.findall(self.regExpNum, line[1])
                    a = [float(i) for i in s]
                    data.extend(a)
            n = np.size(a)
        data = np.asarray(data).reshape((-1, n))
        return data, header
