import math
import random
import sys
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from meas import oscill
import time

class Window(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.thread = Worker()
        self.startButton = QtWidgets.QPushButton('Start')
        self.startButton.clicked.connect(self.start)

        layout = QtWidgets.QGridLayout(self)
        layout.addWidget(self.startButton, 0, 0)

    def start(self):
        self.thread.start()

class Worker(QtCore.QThread):
    def __init__(self):
        super().__init__()
        self.channels = ','
        self.scope = oscill(self.channels)


    def run(self):
        print('waiting')
        try:
            self.scope.snapshot()
            self.trigg
        except Exception as e:
            print(e)
        print('done')


app = QtWidgets.QApplication(sys.argv)
w = Window()
w.show()
sys.exit(app.exec_())
