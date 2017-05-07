from PyQt5 import QtWidgets
import sys


class window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.inputFileLoc = ''
        self.outputFolderLoc = ''
        vbox = QtWidgets.QVBoxLayout(self)
        hbox1 = QtWidgets.QHBoxLayout()
        hbox2 = QtWidgets.QHBoxLayout()
        hbox3 = QtWidgets.QHBoxLayout()
        # -----Horizontal box 1-----
        # Contents
        self.browse_inputFile_button = QtWidgets.QPushButton()
        self.browse_inputFile_button.setText(' Browse MIDE datafile ')
        self.browse_inputFile_button.clicked.connect(
            self.browse_inputFile_button_press)

        self.browse_inputFile_text = QtWidgets.QLabel()
        self.browse_inputFile_text.setFixedSize(250, 10)
        # Add content to Layout
        hbox1.addWidget(self.browse_inputFile_button)
        hbox1.addStretch()
        hbox1.addWidget(self.browse_inputFile_text)
        hbox1.addStretch()
        # -----Horizontal box 2-----
        # Contents
        self.browse_outputFolder_button = QtWidgets.QPushButton()
        self.browse_outputFolder_button.setText(' Browse output folder ')
        self.browse_outputFolder_button.clicked.connect(
            self.browse_outputFolder_button_press)

        self.browse_outputFolder_text = QtWidgets.QLabel()
        self.browse_outputFolder_text.setFixedSize(250, 10)

        # Add content to Layout
        hbox2.addWidget(self.browse_outputFolder_button)
        hbox2.addStretch()
        hbox2.addWidget(self.browse_outputFolder_text)
        hbox2.addStretch()

        # -----Horizontal box 3-----
        # Contents
        self.convert_button = QtWidgets.QPushButton()
        self.convert_button.setText(' Browse output folder ')
        self.convert_button.clicked.connect(
            self.convert_button_press)
        hbox3.addStretch()
        # ----- Vertical box -----
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)

    def browse_inputFile_button_press(self):
        fileLoc = QtWidgets.QFileDialog.getOpenFileName()[0]
        try:
            self.browse_inputFile_text.setText(fileLoc)
            self.inputFileLoc = fileLoc
        except Exception as e:
            print(e)

    def browse_outputFolder_button_press(self):
        folderLoc = QtWidgets.QFileDialog.getExistingDirectory()
        try:
            self.browse_outputFolder_text.setText(folderLoc)
            self.outputFolderLoc = folderLoc
        except Exception as e:
            print(e)

    def convert_button_press(self):
        try:
            print('converting')
        except Exception as e:
            print(e)

app = QtWidgets.QApplication(sys.argv)
a = window()
a.show()

#fileLoc = QFileDialog.getOpenFileName(filter='*.csv')
sys.exit(app.exec_()) # Magic after return statement? Pls explain
