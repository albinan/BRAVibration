# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog_dataimport.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1228, 437)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.import_but = QtWidgets.QPushButton(Dialog)
        self.import_but.setObjectName("import_but")
        self.horizontalLayout_4.addWidget(self.import_but)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.fileExtention_label = QtWidgets.QLabel(Dialog)
        self.fileExtention_label.setObjectName("fileExtention_label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.fileExtention_label)
        self.fileExtention_edit = QtWidgets.QLineEdit(Dialog)
        self.fileExtention_edit.setEnabled(False)
        self.fileExtention_edit.setObjectName("fileExtention_edit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.fileExtention_edit)
        self.dataFormat_label = QtWidgets.QLabel(Dialog)
        self.dataFormat_label.setObjectName("dataFormat_label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.dataFormat_label)
        self.dataFormat_edit = QtWidgets.QLineEdit(Dialog)
        self.dataFormat_edit.setEnabled(False)
        self.dataFormat_edit.setObjectName("dataFormat_edit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.dataFormat_edit)
        self.sliceData_label = QtWidgets.QLabel(Dialog)
        self.sliceData_label.setObjectName("sliceData_label")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.sliceData_label)
        self.sliceData_check = QtWidgets.QCheckBox(Dialog)
        self.sliceData_check.setEnabled(False)
        self.sliceData_check.setText("")
        self.sliceData_check.setObjectName("sliceData_check")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.sliceData_check)
        self.sliceMode_label = QtWidgets.QLabel(Dialog)
        self.sliceMode_label.setObjectName("sliceMode_label")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.sliceMode_label)
        self.sliceMode_combo = QtWidgets.QComboBox(Dialog)
        self.sliceMode_combo.setEnabled(False)
        self.sliceMode_combo.setObjectName("sliceMode_combo")
        self.sliceMode_combo.addItem("")
        self.sliceMode_combo.addItem("")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.sliceMode_combo)
        self.slices_label = QtWidgets.QLabel(Dialog)
        self.slices_label.setObjectName("slices_label")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.slices_label)
        self.slices_spin = QtWidgets.QSpinBox(Dialog)
        self.slices_spin.setEnabled(False)
        self.slices_spin.setObjectName("slices_spin")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.slices_spin)
        self.columTime_label = QtWidgets.QLabel(Dialog)
        self.columTime_label.setObjectName("columTime_label")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.columTime_label)
        self.columnTime_combo = QtWidgets.QComboBox(Dialog)
        self.columnTime_combo.setEnabled(False)
        self.columnTime_combo.setObjectName("columnTime_combo")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.columnTime_combo)
        self.columnAcc_label = QtWidgets.QLabel(Dialog)
        self.columnAcc_label.setObjectName("columnAcc_label")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.columnAcc_label)
        self.columnAcc_combo = QtWidgets.QComboBox(Dialog)
        self.columnAcc_combo.setEnabled(False)
        self.columnAcc_combo.setObjectName("columnAcc_combo")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.columnAcc_combo)
        self.unitTime_label = QtWidgets.QLabel(Dialog)
        self.unitTime_label.setObjectName("unitTime_label")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.LabelRole, self.unitTime_label)
        self.unitTime_combo = QtWidgets.QComboBox(Dialog)
        self.unitTime_combo.setObjectName("unitTime_combo")
        self.unitTime_combo.addItem("")
        self.unitTime_combo.addItem("")
        self.unitTime_combo.addItem("")
        self.unitTime_combo.addItem("")
        self.unitTime_combo.addItem("")
        self.unitTime_combo.addItem("")
        self.unitTime_combo.addItem("")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.FieldRole, self.unitTime_combo)
        self.unitAcc_label = QtWidgets.QLabel(Dialog)
        self.unitAcc_label.setObjectName("unitAcc_label")
        self.formLayout.setWidget(9, QtWidgets.QFormLayout.LabelRole, self.unitAcc_label)
        self.unitAcc_combo = QtWidgets.QComboBox(Dialog)
        self.unitAcc_combo.setObjectName("unitAcc_combo")
        self.unitAcc_combo.addItem("")
        self.unitAcc_combo.addItem("")
        self.unitAcc_combo.addItem("")
        self.formLayout.setWidget(9, QtWidgets.QFormLayout.FieldRole, self.unitAcc_combo)
        self.sampleFrequency_label = QtWidgets.QLabel(Dialog)
        self.sampleFrequency_label.setObjectName("sampleFrequency_label")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.sampleFrequency_label)
        self.sampleFrequency_Spin = QtWidgets.QDoubleSpinBox(Dialog)
        self.sampleFrequency_Spin.setEnabled(False)
        self.sampleFrequency_Spin.setObjectName("sampleFrequency_Spin")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.sampleFrequency_Spin)
        self.verticalLayout.addLayout(self.formLayout)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setEnabled(False)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout_6.addWidget(self.buttonBox)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.progressBar = QtWidgets.QProgressBar(Dialog)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)
        self.horizontalLayout_7.addLayout(self.verticalLayout)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.sample_label = QtWidgets.QLabel(Dialog)
        self.sample_label.setObjectName("sample_label")
        self.verticalLayout_3.addWidget(self.sample_label)
        self.sample_edit = QtWidgets.QPlainTextEdit(Dialog)
        self.sample_edit.setEnabled(False)
        self.sample_edit.setObjectName("sample_edit")
        self.verticalLayout_3.addWidget(self.sample_edit)
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setEnabled(False)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout_3.addWidget(self.tableWidget)
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setEnabled(False)
        self.lineEdit.setObjectName("lineEdit")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setEnabled(False)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_2)
        self.lineEdit_3 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_3.setEnabled(False)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEdit_3)
        self.verticalLayout_3.addLayout(self.formLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setEnabled(False)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_7.addLayout(self.verticalLayout_3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_7)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.import_but.setText(_translate("Dialog", "Import"))
        self.fileExtention_label.setText(_translate("Dialog", "File extension"))
        self.dataFormat_label.setText(_translate("Dialog", "Data format"))
        self.dataFormat_edit.setText(_translate("Dialog", "%f"))
        self.sliceData_label.setText(_translate("Dialog", "Slice data?"))
        self.sliceMode_label.setText(_translate("Dialog", "Slice mode"))
        self.sliceMode_combo.setItemText(0, _translate("Dialog", "Manual"))
        self.sliceMode_combo.setItemText(1, _translate("Dialog", "Automatic"))
        self.slices_label.setText(_translate("Dialog", "Slices"))
        self.columTime_label.setText(_translate("Dialog", "Column with time data"))
        self.columnAcc_label.setText(_translate("Dialog", "Column with acceleration data"))
        self.unitTime_label.setText(_translate("Dialog", "Unit of time data"))
        self.unitTime_combo.setItemText(0, _translate("Dialog", "ChipTimeUS"))
        self.unitTime_combo.setItemText(1, _translate("Dialog", "ns"))
        self.unitTime_combo.setItemText(2, _translate("Dialog", "ms"))
        self.unitTime_combo.setItemText(3, _translate("Dialog", "s"))
        self.unitTime_combo.setItemText(4, _translate("Dialog", "min"))
        self.unitTime_combo.setItemText(5, _translate("Dialog", "h"))
        self.unitTime_combo.setItemText(6, _translate("Dialog", "custom"))
        self.unitAcc_label.setText(_translate("Dialog", "Unit of acceleration data"))
        self.unitAcc_combo.setItemText(0, _translate("Dialog", "g"))
        self.unitAcc_combo.setItemText(1, _translate("Dialog", "ms^2"))
        self.unitAcc_combo.setItemText(2, _translate("Dialog", "custom"))
        self.sampleFrequency_label.setText(_translate("Dialog", "Sample frequency"))
        self.sample_label.setText(_translate("Dialog", "Header"))
        self.label_2.setText(_translate("Dialog", "Sample Frequency"))
        self.label.setText(_translate("Dialog", "Time of meassurement:"))
        self.label_3.setText(_translate("Dialog", "RMS"))
        self.pushButton.setText(_translate("Dialog", "Clear"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

