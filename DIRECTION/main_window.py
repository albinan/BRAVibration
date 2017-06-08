# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 319)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.loadx_button = QtWidgets.QPushButton(self.centralwidget)
        self.loadx_button.setObjectName("loadx_button")
        self.horizontalLayout.addWidget(self.loadx_button)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.loady_button = QtWidgets.QPushButton(self.centralwidget)
        self.loady_button.setEnabled(False)
        self.loady_button.setObjectName("loady_button")
        self.horizontalLayout.addWidget(self.loady_button)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.loadz_button = QtWidgets.QPushButton(self.centralwidget)
        self.loadz_button.setEnabled(False)
        self.loadz_button.setObjectName("loadz_button")
        self.horizontalLayout.addWidget(self.loadz_button)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.calculate_button = QtWidgets.QPushButton(self.centralwidget)
        self.calculate_button.setEnabled(False)
        self.calculate_button.setObjectName("calculate_button")
        self.verticalLayout_2.addWidget(self.calculate_button)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.maxvector_label = QtWidgets.QLabel(self.centralwidget)
        self.maxvector_label.setObjectName("maxvector_label")
        self.horizontalLayout_2.addWidget(self.maxvector_label)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.save_button = QtWidgets.QPushButton(self.centralwidget)
        self.save_button.setEnabled(False)
        self.save_button.setObjectName("save_button")
        self.verticalLayout_2.addWidget(self.save_button)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.loadx_button.setText(_translate("MainWindow", "Load x acceleration"))
        self.loady_button.setText(_translate("MainWindow", "Load y acceleration"))
        self.loadz_button.setText(_translate("MainWindow", "Load z acceleration"))
        self.calculate_button.setText(_translate("MainWindow", "Calculate directionality"))
        self.maxvector_label.setText(_translate("MainWindow", "Vector of maximum acceleration (x, y, z): "))
        self.save_button.setText(_translate("MainWindow", "Save"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

