
"""Naval Fate.

Usage:
  main.py SOURCE_DIR DESTINATION_DIR
  main.py DESTINATION_DIR 
  main.py (-h | --help)
  main.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.

"""
from __future__ import absolute_import
from __future__ import unicode_literals

from docopt import docopt
import os
from datetime import datetime
import shutil

EXTENTIONS = ['png', 'jpg', 'gif', 'jpeg']

def copy_file(_file, destination_dir):
    mtime = os.path.getmtime(_file)
    ctime = os.path.getmtime(_file)
    timestamp = ctime
    if ctime > mtime:
        timestamp = mtime
    date_time = datetime.fromtimestamp(timestamp)
    path = os.path.join(destination_dir, date_time.strftime('%Y-%m-%d'))
    if not os.path.exists(path) or not os.path.isdir(path):
        os.mkdir(path)
    filename = _file.split(os.path.sep)[-1]
    shutil.copy2(_file, os.path.join(path, filename))

def walk_directory(source_dir, destination_dir):
    print str(source_dir)
    for root, dir_names, files in os.walk(source_dir, followlinks=True):
        print "Scaning %s" % root
        for name in files:
            ext = name.split('.')[-1]
            if ext in EXTENTIONS:
                copy_file(os.path.join(root, name), destination_dir)
        for dir_name in dir_names:
            walk_directory(dir_name, destination_dir)

if __name__ == '__main__':
    arguments = docopt(__doc__, version='1.0')
    SOURCE_DIR = arguments['SOURCE_DIR']
    DESTINATION_DIR= os.path.realpath(arguments['DESTINATION_DIR'])

    if not SOURCE_DIR:
        SOURCE_DIR = os.path.realpath(__file__)

    if not os.path.isdir(DESTINATION_DIR):
        os.mkdir(DESTINATION_DIR)

    if not os.access(DESTINATION_DIR, os.W_OK):
        raise Exception('Folder %s not writable' % DESTINATION_DIR)

    walk_directory(SOURCE_DIR, DESTINATION_DIR)
