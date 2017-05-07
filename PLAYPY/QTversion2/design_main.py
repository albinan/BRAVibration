# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1132, 747)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.mplvl = QtWidgets.QVBoxLayout()
        self.mplvl.setObjectName("mplvl")
        self.signal_fig = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.signal_fig.sizePolicy().hasHeightForWidth())
        self.signal_fig.setSizePolicy(sizePolicy)
        self.signal_fig.setObjectName("signal_fig")
        self.mplvl.addWidget(self.signal_fig)
        self.fft_fig = QtWidgets.QWidget(self.centralwidget)
        self.fft_fig.setObjectName("fft_fig")
        self.mplvl.addWidget(self.fft_fig)
        self.horizontalLayout.addLayout(self.mplvl)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.play_list = QtWidgets.QListWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.play_list.sizePolicy().hasHeightForWidth())
        self.play_list.setSizePolicy(sizePolicy)
        self.play_list.setMaximumSize(QtCore.QSize(200, 16777215))
        self.play_list.setObjectName("play_list")
        self.verticalLayout_2.addWidget(self.play_list)
        self.play_button = QtWidgets.QPushButton(self.centralwidget)
        self.play_button.setObjectName("play_button")
        self.verticalLayout_2.addWidget(self.play_button)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1132, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionClear = QtWidgets.QAction(MainWindow)
        self.actionClear.setObjectName("actionClear")
        self.actionExport_Wav = QtWidgets.QAction(MainWindow)
        self.actionExport_Wav.setObjectName("actionExport_Wav")
        self.actionExport_wav = QtWidgets.QAction(MainWindow)
        self.actionExport_wav.setObjectName("actionExport_wav")
        self.actionCalibrate = QtWidgets.QAction(MainWindow)
        self.actionCalibrate.setObjectName("actionCalibrate")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionClear)
        self.menuFile.addAction(self.actionExport_wav)
        self.menuFile.addAction(self.actionCalibrate)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.play_button.setText(_translate("MainWindow", "Play"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionClear.setText(_translate("MainWindow", "Clear"))
        self.actionExport_Wav.setText(_translate("MainWindow", "Export Wav"))
        self.actionExport_wav.setText(_translate("MainWindow", "Export wav"))
        self.actionCalibrate.setText(_translate("MainWindow", "Calibrate"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

