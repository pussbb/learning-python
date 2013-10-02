__author__ = 'pussbb'

from settings import Settings

import sys

from PyQt5 import QtCore, QtGui, QtWidgets

settings = Settings()
settings.setValue('list_value', [1, 2, 3])
timer =  QtCore.QTimer()

class SystemTrayIcon(QtWidgets.QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        self.menu = QtWidgets.QMenu(parent)
        self.setContextMenu(self.menu)
        self.activated.connect(self.on_activated)

    def on_activated(self, reason):
        if reason == QtWidgets.QSystemTrayIcon.Trigger:
            self.showMessage("dfdsfdsf", "ytytrytr")


    def add_menu_actions(self, actions):
        for i in actions:
            self.menu.addAction(i)

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None, flags=QtCore.Qt.Widget):
        super().__init__(parent, flags)

        actions = [
            QtWidgets.QAction("Settings", self, triggered=self.show),
            QtWidgets.QAction("Exit", self, triggered=self.on_exit)
        ]

        icon = QtGui.QIcon(self.style().standardPixmap(QtWidgets.QStyle.SP_FileIcon))
        self.trayIcon = SystemTrayIcon(icon)
        self.trayIcon.add_menu_actions(actions)
        self.trayIcon.show()

    def on_exit(self):
        QtWidgets.QApplication.instance().exit()


def main():

    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

