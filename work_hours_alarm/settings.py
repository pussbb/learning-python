__author__ = 'pussbb'

import os
from PyQt5.QtCore import QSettings

class Settings(QSettings):

    def __init__(self, config_name = 'app.cfg'):
        self.config_file = self.absolute_file_path(config_name)
        QSettings.__init__(self, self.config_file, QSettings.IniFormat)

    def absolute_file_path(self, config_file):
        return os.path.join(self.config_path(), config_file)

    def config_path(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(current_dir, 'config')

    def setValue(self, *kargs, **kwargs):
        super().setValue(*kargs, **kwargs)
        self.sync()

