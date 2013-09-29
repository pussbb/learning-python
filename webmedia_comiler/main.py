__author__ = 'pussbb'

from settings import Settings

import sys
import PyQt5.QtCore
import PyQt5.QtGui
import PyQt5.QtWidgets



settings = Settings()
settings.setValue('list_value', [1, 2, 3])

def main():

    app = PyQt5.QtWidgets.QApplication(sys.argv)

    w = PyQt5.QtWidgets.QDialog()
    w.resize(250, 150)
    w.move(300, 300)
    w.setWindowTitle('Simple')
    w.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

