from View import window
from PyQt5 import QtWidgets
import sys
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = window()
    w.show()
    sys.exit(app.exec_())
