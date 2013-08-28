# -*- coding: utf-8 -*-
"""Photo catalog.

Usage:
  photcat.py SOURCE_DIR DESTINATION_DIR [-y]
  photcat.py DESTINATION_DIR [-y]
  photcat.py (-h | --help)
  photcat.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  -y            Split folders by year.

"""

from __future__ import unicode_literals, print_function

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
    ''' Human readable file size '''
    for x in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0 and num > -1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0
    return "%3.1f %s" % (num, 'TB')

def copy_file(origin_file, destination_dir):
    ''' Copy file into folder '''
    global TOTAL
    mtime = os.path.getmtime(origin_file)
    ctime = os.path.getmtime(origin_file)
    timestamp = ctime
    if ctime > mtime:
        timestamp = mtime
    date_time = datetime.fromtimestamp(timestamp)

    path = os.path.join(destination_dir, date_time.strftime('%Y-%m'))

    if (SPLIT_BY_YEAR):
        path = os.path.join(destination_dir, date_time.strftime('%Y'),
                             date_time.strftime('%m'))

    if not os.path.exists(path) or not os.path.isdir(path):
        os.makedirs(path)

    filename = origin_file.split(os.path.sep)[-1]
    destination_file = os.path.join(path, filename)

    index = 1
    while os.path.exists(destination_file):
        parts = filename.decode('utf-8').split('.')
        parts[-2] += "(%s)" % index
        destination_file = os.path.join(path, '.'.join(parts))
        index += 1

    print("Copying file: %s (%s)" % (filename.decode('UTF-8'),
                                   sizeof_fmt(os.path.getsize(origin_file))))
    TOTAL += 1
    shutil.copy2(origin_file, destination_file)

def walk_directory(source_dir, destination_dir):
    ''' Recursively walk through directory'''
    for root, dir_names, files in os.walk(source_dir, followlinks=True):
        print("Scaning %s" % root.decode('UTF-8'))
        for name in files:
            ext = name.decode('UTF-8').split('.')[-1]
            if ext.lower() in EXTENTIONS:
                copy_file(os.path.join(root, name), destination_dir)
        for dir_name in dir_names:
            walk_directory(dir_name, destination_dir)

if __name__ == '__main__':
    arguments = docopt(__doc__, version= __version__)
    SOURCE_DIR = arguments['SOURCE_DIR']
    DESTINATION_DIR = os.path.realpath(arguments['DESTINATION_DIR'])
    SPLIT_BY_YEAR = arguments['-y']

    if not SOURCE_DIR:
        SOURCE_DIR = os.path.realpath(__file__)

    if not os.path.isdir(DESTINATION_DIR):
        os.mkdir(DESTINATION_DIR)

    if not os.access(DESTINATION_DIR, os.W_OK):
        raise Exception('Folder %s not writable' % DESTINATION_DIR)

    walk_directory(SOURCE_DIR, DESTINATION_DIR)

    print('%s files were copied' % TOTAL)
    print('Done!')
