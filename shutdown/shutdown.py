__author__ = 'pussbb'

import sys

from PyQt4 import QtCore, uic, QtGui
import subprocess
import os
import datetime, time


_dir = os.path.abspath(os.path.dirname(__file__))
class SystemTrayIcon(QtGui.QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        if not QtGui.QSystemTrayIcon.isSystemTrayAvailable():
            QtGui.QMessageBox.critical(None, "Systray",
                "I couldn't detect any system tray on this system.")
            sys.exit(1)
        QtGui.QSystemTrayIcon.__init__(self, icon, parent)

class MainWindow(QtGui.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = uic.loadUi(os.path.join(_dir, 'main.ui'))
        self.ui.closeEvent = self.closeEvent

        icon = QtGui.QIcon(QtGui.QPixmap(os.path.join(_dir, "icon.png")))
        self.setWindowIcon(icon)
        self.trayIcon = SystemTrayIcon(icon)
        self.trayIcon.show()
        menu = QtGui.QMenu(self)
        menu.addAction(QtGui.QAction("&Show",
                                     self, triggered=self.activate_window))
        menu.addAction(QtGui.QAction("&Quit", self, triggered=QtGui.qApp.quit))
        self.trayIcon.setContextMenu(menu)
        self.trayIcon.activated.connect(self.on_tray_icon_activated)

        self.connect(self.ui.start,
                     QtCore.SIGNAL("clicked()"), self.shutdown_timeout)
        self.Proc = None
        self.blackout_time = None
        self.timer = QtCore.QTimer()
        self.connect(self.timer, QtCore.SIGNAL("timeout()"), self.update_left_time)
        self.timer.start(1000)


    def __del__(self):
        if self.Proc:
            self.Proc.terminate()

    def shutdown_timeout(self):

        if self.ui.timeEdit.isEnabled():
            now = QtCore.QTime()
            seconds = now.secsTo(self.ui.timeEdit.time())
            self.ui.timeEdit.setEnabled(False)
            self.ui.start.setText('Stop')
            self.blackout(seconds)
            self.blackout_time = QtCore.QTime.currentTime().addSecs(seconds)
        else:
            if self.Proc:
                self.Proc.terminate()
            self.Proc = None
            self.blackout_time = 0
            self.ui.timeEdit.setEnabled(True)
            self.ui.start.setText('Start')

    def blackout(self, seconds):
        if self.Proc:
            self.Proc.terminate()
            self.Proc = None

        cmd = "$(type -P kdesudo) -c 'sleep {:d}" \
              " && /sbin/shutdown -h now'".format(seconds)

        self.Proc = subprocess.Popen(cmd, executable='/bin/bash', shell=True)

    def update_left_time(self):

        if self.Proc and self.Proc.poll():
            self.Proc = None
            self.ui.start.click()

        if self.ui.timeEdit.isEnabled():
            self.ui.blackout_time.setText('00:00')
            self.ui.leftLabel.setText('0 hours 0 minutes')
        else:

            self.ui.blackout_time.setText(self.blackout_time.toString("HH:mm"))
            self.ui.leftLabel.setText('{0} hours {1} minutes'\
                                            .format(*self.time_to_blackout()))

    def time_to_blackout(self):
        left_seconds = QtCore.QTime.currentTime().secsTo(self.blackout_time)
        hours = left_seconds // 3600
        min_ = (left_seconds // 60) % 60
        return hours, min_

    def activate_window(self):
        self.ui.show()
        self.setFocus()
        self.raise_()
        self.activateWindow()

    def on_tray_icon_activated(self, reason):
        if reason == QtGui.QSystemTrayIcon.DoubleClick:
            self.activate_window()
        elif reason == QtGui.QSystemTrayIcon.Trigger and self.blackout_time:
            now_string = self.blackout_time.toString("HH:mm")

            self.trayIcon.showMessage("System Shoutdown",
                                      "System will shutdown at {0}.\n"
                                      "Left {1} hours {2} minutes".format(now_string,
                                                        *self.time_to_blackout()))

    def closeEvent(self, event):
        self.ui.hide()
        event.setAccepted(True)
        event.ignore()

def main():

    app = QtGui.QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
