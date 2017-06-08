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
        MainWindow.resize(396, 162)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.import_button = QtWidgets.QPushButton(self.centralwidget)
        self.import_button.setObjectName("import_button")
        self.horizontalLayout.addWidget(self.import_button)
        self.analyze_button = QtWidgets.QPushButton(self.centralwidget)
        self.analyze_button.setEnabled(False)
        self.analyze_button.setObjectName("analyze_button")
        self.horizontalLayout.addWidget(self.analyze_button)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.slice_label = QtWidgets.QLabel(self.centralwidget)
        self.slice_label.setObjectName("slice_label")
        self.horizontalLayout_3.addWidget(self.slice_label)
        self.slice_check = QtWidgets.QCheckBox(self.centralwidget)
        self.slice_check.setText("")
        self.slice_check.setObjectName("slice_check")
        self.horizontalLayout_3.addWidget(self.slice_check)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.bandwidth_label = QtWidgets.QLabel(self.centralwidget)
        self.bandwidth_label.setObjectName("bandwidth_label")
        self.horizontalLayout_2.addWidget(self.bandwidth_label)
        self.bandwidth_spin = QtWidgets.QSpinBox(self.centralwidget)
        self.bandwidth_spin.setObjectName("bandwidth_spin")
        self.horizontalLayout_2.addWidget(self.bandwidth_spin)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.minimumFrequency_label = QtWidgets.QLabel(self.centralwidget)
        self.minimumFrequency_label.setObjectName("minimumFrequency_label")
        self.horizontalLayout_4.addWidget(self.minimumFrequency_label)
        self.minimumFrequency_spin = QtWidgets.QSpinBox(self.centralwidget)
        self.minimumFrequency_spin.setObjectName("minimumFrequency_spin")
        self.horizontalLayout_4.addWidget(self.minimumFrequency_spin)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.maximumFrequency_label = QtWidgets.QLabel(self.centralwidget)
        self.maximumFrequency_label.setObjectName("maximumFrequency_label")
        self.horizontalLayout_5.addWidget(self.maximumFrequency_label)
        self.maximumFrequency_spin = QtWidgets.QSpinBox(self.centralwidget)
        self.maximumFrequency_spin.setObjectName("maximumFrequency_spin")
        self.horizontalLayout_5.addWidget(self.maximumFrequency_spin)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.import_button.setText(_translate("MainWindow", "Import"))
        self.analyze_button.setText(_translate("MainWindow", "Analyze"))
        self.slice_label.setText(_translate("MainWindow", "Slice data?"))
        self.bandwidth_label.setText(_translate("MainWindow", "Bandwidth"))
        self.minimumFrequency_label.setText(_translate("MainWindow", "Minimum frequency"))
        self.maximumFrequency_label.setText(_translate("MainWindow", "Maximum frequency"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

