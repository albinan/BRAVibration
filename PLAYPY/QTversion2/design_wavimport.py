# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design_wavimport.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(776, 320)
        MainWindow.setAcceptDrops(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.import_button = QtWidgets.QPushButton(self.centralwidget)
        self.import_button.setObjectName("import_button")
        self.horizontalLayout_4.addWidget(self.import_button)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.fs_label = QtWidgets.QLabel(self.centralwidget)
        self.fs_label.setObjectName("fs_label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.fs_label)
        self.fs_combo = QtWidgets.QComboBox(self.centralwidget)
        self.fs_combo.setObjectName("fs_combo")
        self.fs_combo.addItem("")
        self.fs_combo.addItem("")
        self.fs_combo.addItem("")
        self.fs_combo.addItem("")
        self.fs_combo.addItem("")
        self.fs_combo.addItem("")
        self.fs_combo.addItem("")
        self.fs_combo.addItem("")
        self.fs_combo.addItem("")
        self.fs_combo.addItem("")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.fs_combo)
        self.slice_label = QtWidgets.QLabel(self.centralwidget)
        self.slice_label.setObjectName("slice_label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.slice_label)
        self.slice_check = QtWidgets.QCheckBox(self.centralwidget)
        self.slice_check.setEnabled(True)
        self.slice_check.setText("")
        self.slice_check.setObjectName("slice_check")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.slice_check)
        self.sliceMode_label = QtWidgets.QLabel(self.centralwidget)
        self.sliceMode_label.setObjectName("sliceMode_label")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.sliceMode_label)
        self.sliceMode_combo = QtWidgets.QComboBox(self.centralwidget)
        self.sliceMode_combo.setEnabled(False)
        self.sliceMode_combo.setObjectName("sliceMode_combo")
        self.sliceMode_combo.addItem("")
        self.sliceMode_combo.addItem("")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.sliceMode_combo)
        self.slices_label = QtWidgets.QLabel(self.centralwidget)
        self.slices_label.setObjectName("slices_label")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.slices_label)
        self.columTime_label = QtWidgets.QLabel(self.centralwidget)
        self.columTime_label.setObjectName("columTime_label")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.columTime_label)
        self.columnTime_combo = QtWidgets.QComboBox(self.centralwidget)
        self.columnTime_combo.setEnabled(False)
        self.columnTime_combo.setObjectName("columnTime_combo")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.columnTime_combo)
        self.columnAcc_label = QtWidgets.QLabel(self.centralwidget)
        self.columnAcc_label.setObjectName("columnAcc_label")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.columnAcc_label)
        self.unitTime_label = QtWidgets.QLabel(self.centralwidget)
        self.unitTime_label.setObjectName("unitTime_label")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.unitTime_label)
        self.unitTime_combo = QtWidgets.QComboBox(self.centralwidget)
        self.unitTime_combo.setObjectName("unitTime_combo")
        self.unitTime_combo.addItem("")
        self.unitTime_combo.addItem("")
        self.unitTime_combo.addItem("")
        self.unitTime_combo.addItem("")
        self.unitTime_combo.addItem("")
        self.unitTime_combo.addItem("")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.unitTime_combo)
        self.unitAcc_label = QtWidgets.QLabel(self.centralwidget)
        self.unitAcc_label.setObjectName("unitAcc_label")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.unitAcc_label)
        self.unitAcc_combo = QtWidgets.QComboBox(self.centralwidget)
        self.unitAcc_combo.setObjectName("unitAcc_combo")
        self.unitAcc_combo.addItem("")
        self.unitAcc_combo.addItem("")
        self.unitAcc_combo.addItem("")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.unitAcc_combo)
        self.columnAcc_combo = QtWidgets.QComboBox(self.centralwidget)
        self.columnAcc_combo.setEnabled(False)
        self.columnAcc_combo.setObjectName("columnAcc_combo")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.columnAcc_combo)
        self.slices_spin = QtWidgets.QSpinBox(self.centralwidget)
        self.slices_spin.setEnabled(False)
        self.slices_spin.setObjectName("slices_spin")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.slices_spin)
        self.verticalLayout.addLayout(self.formLayout)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem1)
        self.ok_button = QtWidgets.QPushButton(self.centralwidget)
        self.ok_button.setObjectName("ok_button")
        self.horizontalLayout_6.addWidget(self.ok_button)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem2)
        self.cancel_button = QtWidgets.QPushButton(self.centralwidget)
        self.cancel_button.setObjectName("cancel_button")
        self.horizontalLayout_6.addWidget(self.cancel_button)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7.addLayout(self.verticalLayout)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.sample_label = QtWidgets.QLabel(self.centralwidget)
        self.sample_label.setObjectName("sample_label")
        self.verticalLayout_3.addWidget(self.sample_label)
        self.sample_edit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.sample_edit.setObjectName("sample_edit")
        self.verticalLayout_3.addWidget(self.sample_edit)
        self.horizontalLayout_7.addLayout(self.verticalLayout_3)
        self.horizontalLayout_8.addLayout(self.horizontalLayout_7)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.import_button.setText(_translate("MainWindow", "Import"))
        self.fs_label.setText(_translate("MainWindow", "Wav sample rate"))
        self.fs_combo.setItemText(0, _translate("MainWindow", "8000"))
        self.fs_combo.setItemText(1, _translate("MainWindow", "9600"))
        self.fs_combo.setItemText(2, _translate("MainWindow", "11025"))
        self.fs_combo.setItemText(3, _translate("MainWindow", "12000"))
        self.fs_combo.setItemText(4, _translate("MainWindow", "16000"))
        self.fs_combo.setItemText(5, _translate("MainWindow", "22050"))
        self.fs_combo.setItemText(6, _translate("MainWindow", "24000"))
        self.fs_combo.setItemText(7, _translate("MainWindow", "32000"))
        self.fs_combo.setItemText(8, _translate("MainWindow", "44100"))
        self.fs_combo.setItemText(9, _translate("MainWindow", "48000"))
        self.slice_label.setText(_translate("MainWindow", "Slice data?"))
        self.sliceMode_label.setText(_translate("MainWindow", "Slice mode"))
        self.sliceMode_combo.setItemText(0, _translate("MainWindow", "Manual"))
        self.sliceMode_combo.setItemText(1, _translate("MainWindow", "Automatic"))
        self.slices_label.setText(_translate("MainWindow", "Slices"))
        self.columTime_label.setText(_translate("MainWindow", "Column with time data"))
        self.columnAcc_label.setText(_translate("MainWindow", "Column with acceleration data"))
        self.unitTime_label.setText(_translate("MainWindow", "Unit of time data"))
        self.unitTime_combo.setItemText(0, _translate("MainWindow", "ns"))
        self.unitTime_combo.setItemText(1, _translate("MainWindow", "ms"))
        self.unitTime_combo.setItemText(2, _translate("MainWindow", "s"))
        self.unitTime_combo.setItemText(3, _translate("MainWindow", "min"))
        self.unitTime_combo.setItemText(4, _translate("MainWindow", "h"))
        self.unitTime_combo.setItemText(5, _translate("MainWindow", "custom"))
        self.unitAcc_label.setText(_translate("MainWindow", "Unit of acceleration data"))
        self.unitAcc_combo.setItemText(0, _translate("MainWindow", "g"))
        self.unitAcc_combo.setItemText(1, _translate("MainWindow", "ms^2"))
        self.unitAcc_combo.setItemText(2, _translate("MainWindow", "custom"))
        self.ok_button.setText(_translate("MainWindow", "OK"))
        self.cancel_button.setText(_translate("MainWindow", "Cancel"))
        self.sample_label.setText(_translate("MainWindow", "Sample of imported data"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())