# -*- coding: utf-8 -*-


from __future__ import print_function

import sys
import os
from PyQt4 import QtGui, QtCore, uic
from datetime import datetime
import shutil

EXTENTIONS = ['png', 'jpg', 'gif', 'jpeg', 'mpeg', 'mp4']

def current_directory():
    return os.path.dirname(os.path.realpath(__file__))

def sizeof_fmt(num):
    """ Human readable file size """
    for label in ['bytes', 'KB', 'MB', 'GB']:
        if 1024.0 > num > -1024.0:
            return "%3.1f %s" % (num, label)
        num /= 1024.0
    return "%3.1f %s" % (num, 'TB')

class PhotoCat(QtGui.QMainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.ui = uic.loadUi(os.path.join(current_directory(), 'mainwindow.ui'))
        self.ui.setWindowTitle("PhotoCat")
        self.ui.show()

        self.ui.Close.triggered.connect(QtGui.qApp.quit)
        self.connect(self.ui.chooseSorceFolder,
                     QtCore.SIGNAL("clicked()"), self.choose_source_folder)

        self.connect(self.ui.chooseDestDir,
                     QtCore.SIGNAL("clicked()"), self.choose_destination_folder)

        self.connect(self.ui.destFolder,
                     QtCore.SIGNAL("textChanged(QString)"),
                     self.folders_changed)
        self.connect(self.ui.sourceFolder,
                     QtCore.SIGNAL("textChanged(QString)"),
                     self.folders_changed)

        self.connect(self.ui.start, QtCore.SIGNAL("clicked()"), self.start)

    def get_folder(self, title, mode=os.R_OK):
        options_ = QtGui.QFileDialog.ShowDirsOnly
        user_folder =  QtGui.QFileDialog.getExistingDirectory(self,
                                                              title,
                                                              '/home',
                                                              options=options_)

        if user_folder and not os.access(user_folder, mode):
            message = "Somthing wrong with folder {0}".format(user_folder)
            if mode == os.R_OK:
                message = "Folder {0} is not readable.".format(user_folder)
            elif mode == os.W_OK:
                message = "Folder {0} is not writtable.".format(user_folder)
            QtGui.QMessageBox.critical(self, "Photocat", message)
            user_folder = None
        return user_folder

    def choose_source_folder(self):
        source_folder = self.get_folder("Choose source directory")
        if source_folder:
            self.ui.sourceFolder.setText(source_folder)

    def choose_destination_folder(self):
        destination_folder = self.get_folder("Choose destination directory",
                                             mode=os.W_OK)
        if destination_folder:
            self.ui.destFolder.setText(destination_folder)

    def folders_changed(self, _):
        enabled = True
        if not self.ui.sourceFolder.text() or not self.ui.destFolder.text():
            enabled = False
        self.ui.start.setEnabled(enabled)

    def start(self):
        self.ui.start.setEnabled(False)
        self.ui.chooseDestDir.setEnabled(False)
        self.ui.chooseSorceFolder.setEnabled(False)
        self.ui.progressBar.setMaximum(0)
        self.ui.progressBar.setMinimum(0)
        self.ui.filesCount.setText("0")
        for root, _, files in os.walk(str(self.ui.sourceFolder.text()),
                                      followlinks=True):
            files_count = self.ui.filesCount.text().toInt()[0]
            files_count += len(files)
            self.ui.progressBar.setMaximum(files_count)
            self.ui.filesCount.setText(str(files_count))
            for name in files:
                self.ui.progressBar.setValue(self.ui.progressBar.value() + 1)
                ext = name.split('.')[-1]
                if ext.lower() in EXTENTIONS:
                    self.copy_file(os.path.join(root, name))

        self.ui.start.setEnabled(True)
        self.ui.chooseDestDir.setEnabled(True)
        self.ui.chooseSorceFolder.setEnabled(True)


    def copy_file(self, file_):
        destination_dir = str(self.ui.destFolder.text())
        mtime = os.path.getmtime(file_)
        ctime = os.path.getctime(file_)
        timestamp = ctime
        if ctime > mtime:
            timestamp = mtime
        date_time = datetime.fromtimestamp(timestamp)

        path = os.path.join(destination_dir,
                            date_time.strftime('%Y-%m'))

        if self.ui.splitByYear.isChecked():
            path = os.path.join(destination_dir, date_time.strftime('%Y'),
                                 date_time.strftime('%m'))

        if not os.path.exists(path) or not os.path.isdir(path):
            os.makedirs(path)

        filename = file_.split(os.path.sep)[-1]
        destination_file = os.path.join(path, filename)

        index = 1
        while os.path.exists(destination_file):
            parts = filename.split('.')
            parts[-2] += "(%s)" % index
            destination_file = os.path.join(path, '.'.join(parts))
            index += 1

        self.ui.statusBar.showMessage("Copying file: %s (%s)" % (filename,
                                   sizeof_fmt(os.path.getsize(file_))),
                                    2000)

        shutil.copy2(file_, destination_file)

def main():
    app = QtGui.QApplication(sys.argv)
    photocat = PhotoCat()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
