from importdata0 import importTool
from PyQt5 import QtWidgets
import sys
import numpy as np
import re

string = '7, 0.7, 0.007, 7e-1'
regExp = '(?:0)\.7'
p = re.compile(regExp)
s = p.search(string)
print(s.group())
#app = QtWidgets.QApplication(sys.argv)
#mptool = importTool()
#file_loc, file_extention = imptool.fileLoc()
#print(file_loc, '|', file_extention)
#data, header = imptool.importTextFile(file_loc)
#print(np.shape(data))
#print(data)
#sys.exit(app.exec_())

#a = QtWidgets.QDialog.getOpenFileName()
