__author__ = 'pussbb'

from settings import Settings

import sys

from PyQt5 import QtCore, QtGui, QtWidgets

settings = Settings()
settings.setValue('list_value', [1, 2, 3])
#time = QtCore.QTime()
#print(QtCore.QTime.currentTime())
#print(time.toString('h:m ap'))


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        self.menu = QtWidgets.QMenu(parent)
        self.setContextMenu(self.menu)

    def add_menu_actions(self, actions):
        for i in actions:
            self.menu.addAction(i)

class MainWindow(QtWidgets.QMainWindow):

    time_format = 'hh:mm:ss'

    def __init__(self, parent=None, flags=QtCore.Qt.Widget):
        super().__init__(parent, flags)
        self.time = QtCore.QTime.currentTime()
        actions = [
            QtWidgets.QAction("Start work", self, triggered=self.start_work),
            #QtWidgets.QAction("Settings", self, triggered=self.show),
            QtWidgets.QAction("Exit", self, triggered=self.on_exit)
        ]

        icon = QtGui.QIcon(self.style().standardPixmap(QtWidgets.QStyle.SP_FileIcon))
        self.trayIcon = SystemTrayIcon(icon)
        self.trayIcon.add_menu_actions(actions)
        self.trayIcon.activated.connect(self.on_tray_icon_activated)
        self.trayIcon.show()

    def on_exit(self):
        QtWidgets.QApplication.instance().exit()

    def start_work(self):
        self.time = QtCore.QTime.currentTime()
        self.time.start()
        print()

    def on_tray_icon_activated(self, reason):
        if reason == QtWidgets.QSystemTrayIcon.Trigger:
            now_string = QtCore.QTime.currentTime().toString(self.time_format)
            self.trayIcon.showMessage("dfdsfdsf",
                                      "now {0}".format(now_string))

def main():

    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

