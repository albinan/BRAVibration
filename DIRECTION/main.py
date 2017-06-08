from PyQt5 import QtWidgets
from main_window import Ui_MainWindow
import sys
import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft, fftfreq
from scipy.integrate import cumtrapz
from scipy.signal import spectrogram
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
sys.path.append('C:/Users/ReVibe/Documents/Albin/BRAVibration/LIB/dataImportUI')
sys.path.append('C:/Users/ReVibe/Documents/Albin/BRAVibration/LIB')
from linnearmodels import mod0001
from dialog_dataimport_UI import DataImportDialog
from fun import rootMeanSquare

class mainwindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        self.setupSignals()
        self.x = []
        self.y = []
        self.z = []

    def setupSignals(self):
        self.loadx_button.clicked.connect(self.loadx)
        self.loady_button.clicked.connect(self.loady)
        self.loadz_button.clicked.connect(self.loadz)
        self.calculate_button.clicked.connect(self.calculate)

    def loadx(self):
        t, self.x = DataImportDialog.getData()
        self.loady_button.setEnabled(True)

    def loady(self):
        t, self.y = DataImportDialog.getData()
        self.loadz_button.setEnabled(True)

    def loadz(self):
        t, self.z = DataImportDialog.getData()
        self.calculate_button.setEnabled(True)

    def calculate(self):
        try:
            x_bar = np.sum(self.x)
            y_bar = np.sum(self.y)
            z_bar = np.sum(self.z)
            a_bar = np.asarray([x_bar, y_bar, z_bar])/np.sqrt(x_bar**2+y_bar**2+z_bar**2)
            self.maxvector_label.setText('Vector of maximum acceleration (x, y, z): (' + str(a_bar[0]) + ',' + str(a_bar[1]) + ',' + str(a_bar[2]) + ')')
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            ax.plot(self.x[:5000], self.y[:5000], self.z[:5000])
            ax.set_xlabel('Acceleration x (g)')
            ax.set_ylabel('Acceleration y (g)')
            ax.set_zlabel('Acceleration z (g)')
            ax.set_title('Acceleration in 3 dimension')
            plt.show()
        except Exception as e:
            print(e)


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    GUI = mainwindow()
    GUI.show()
    sys.exit(app.exec_())
