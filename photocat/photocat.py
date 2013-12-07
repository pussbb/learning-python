# -*- coding: utf-8 -*-
"""Photo catalog.

Usage:
  photocat.py gui
  photocat.py SOURCE_DIR DESTINATION_DIR [-y]
  photocat.py DESTINATION_DIR [-y]
  photocat.py (-h | --help)
  photocat.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  -y            Split folders by year.

"""

from __future__ import unicode_literals, print_function

import sys

if sys.version_info[0] < 3:
    import imp
    imp.reload(sys)
    sys.setdefaultencoding("UTF-8")

from docopt import docopt
import os
from datetime import datetime
import shutil

__version__ = '0.0.1'
__all__ = ('walk_directory', 'SPLIT_BY_YEAR', 'copy_file')


EXTENTIONS = ['png', 'jpg', 'gif', 'jpeg', 'mpeg']
SPLIT_BY_YEAR = False
TOTAL = 0


def sizeof_fmt(num):
    """ Human readable file size """
    for label in ['bytes', 'KB', 'MB', 'GB']:
        if 1024.0 > num > -1024.0:
            return "%3.1f %s" % (num, label)
        num /= 1024.0
    return "%3.1f %s" % (num, 'TB')

def copy_file(origin_file, destination_dir):
    """ Copy file into folder """
    global TOTAL
    mtime = os.path.getmtime(origin_file)
    ctime = os.path.getctime(origin_file)
    timestamp = ctime
    if ctime > mtime:
        timestamp = mtime
    date_time = datetime.fromtimestamp(timestamp)

    path = os.path.join(destination_dir, date_time.strftime('%Y-%m'))

    if SPLIT_BY_YEAR:
        path = os.path.join(destination_dir, date_time.strftime('%Y'),
                             date_time.strftime('%m'))

    if not os.path.exists(path) or not os.path.isdir(path):
        os.makedirs(path)

    filename = origin_file.split(os.path.sep)[-1]
    destination_file = os.path.join(path, filename)

    index = 1
    while os.path.exists(destination_file):
        parts = filename.split('.')
        parts[-2] += "(%s)" % index
        destination_file = os.path.join(path, '.'.join(parts))
        index += 1

    print("Copying file: %s (%s)" % (filename,
                                   sizeof_fmt(os.path.getsize(origin_file))))
    TOTAL += 1
    shutil.copy2(origin_file, destination_file)

def walk_directory(source_dir, destination_dir):
    """ Recursively walk through directory"""
    for root, dir_names, files in os.walk(source_dir, followlinks=True):
        print("Scaning %s" % root)
        for name in files:
            ext = name.split('.')[-1]
            if ext.lower() in EXTENTIONS:
                copy_file(os.path.join(root, name), destination_dir)

if __name__ == '__main__':
    ARGS = docopt(__doc__, version= __version__)
    SOURCE_DIR = ARGS['SOURCE_DIR']
    DESTINATION_DIR = ARGS['DESTINATION_DIR']

    SPLIT_BY_YEAR = ARGS['-y']

    if not SOURCE_DIR:
        SOURCE_DIR = os.path.dirname(os.path.realpath(__file__))

    if DESTINATION_DIR:
        DESTINATION_DIR = os.path.realpath(DESTINATION_DIR)
        if not os.path.isdir(DESTINATION_DIR):
            os.mkdir(DESTINATION_DIR)

        if not os.access(DESTINATION_DIR, os.W_OK):
            raise Exception('Folder %s not writable' % DESTINATION_DIR)

    if ARGS['gui'] or sys.platform.startswith('win'):
        import ui.app
        ui.app.main()
    else:
        walk_directory(SOURCE_DIR, DESTINATION_DIR)
        print('%s files were copied' % TOTAL)
        print('Done!')
