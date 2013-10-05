# -*- coding: utf-8 -*-
"""Photo catalog.

Usage:
  jad_decompiler.py --jad=<jad> ( --jar=<jar> | --jar_dir=<jar_dir> )
  jad_decompiler.py [ --dir=<dir> | --jad_options=<jad_options> ]
  jad_decompiler.py (-h | --help)
  jad_decompiler.py --version

Options:
  -h --help                     Show this screen.
  --version                     Show version.
  --jad=<jad>                   JAD decompiler
  --jar=<jar>                   Jar file
  --jar_dir=<jar_dir>           Directory with jars
  --dir=<dir>                   Directory to output
  --jad_options=<jad_options>   Additional options for jad decompiler

"""
#python 2 support
from __future__ import unicode_literals, print_function

__author__ = 'pussbb'
__version__ = '0.0.1'
__all__ = ['decompile_class', 'decompile_jar']

import os
import zipfile
import subprocess

JAD_DECOMPILER = None

def _file_directory(file):
    return os.path.dirname(os.path.realpath(file))

def extract_jar(jar, path=None):
    file = zipfile.ZipFile(jar)
    if not path or not os.path.isdir(path):
        path = _file_directory(jar)
    path = os.path.join(path, os.path.basename(jar))
    file.extractall(path)

def decompile_wrapper(func):
    def real_decorator(jad_app, file, output_dir=None, jad_options=None):
        if not output_dir or not os.path.isdir(output_dir):
            output_dir = _file_directory(jar)
        return func(jad_app, file, output_dir, jad_options)
    return real_decorator

@decompile_wrapper
def decompile_class(jad_app, class_file, output_dir=None, jad_options=None):
    command = [
        jad_app,
        '-o',
        '-sjava',
        '-d{0}'.format(output_dir),
        class_file,
    ]
    subprocess.call(command)
    os.remove(class_file)

@decompile_wrapper
def decompile_jar(jad_app, jar, output_dir=None, jad_options=None):
    extract_jar(jar, output_dir)

    for root, dir_names, files in os.walk(output_dir, followlinks=True):
        for name in files:
            if not name.lower().endswith('.class'):
                continue
            decompile_class(jad_app, os.path.join(root, name), root)


def _look_for_jars(jar_dir, jad_app, output_dir, jad_options):
    for root, dir_names, files in os.walk(jar_dir, followlinks=True):
        for file in files:
            if not file.lower().endswith('.jar'):
                continue
            decompile_jar(jad_app, os.path.join(root, file),
                          output_dir, jad_options)

if __name__ == '__main__':
    from docopt import docopt
    ARGS = docopt(__doc__, version= __version__)

    jad_app = os.path.abspath(ARGS['--jad'])
    if not os.path.isfile(jad_app):
        SystemError("Jad Decompiler not found")

    jar = ARGS['--jar']
    jar_dir = ARGS['--jar_dir']
    output_dir = ARGS['--dir']
    jad_options = ARGS['--jad_options']

    if jar:
        if not output_dir: output_dir = _file_directory(jar)
        decompile_jar(jad_app, jar, output_dir, ARGS['--jad_options'])
    elif jar_dir:
        jar_dir = os.path.abspath(ARGS['--jar_dir'])
        if not output_dir: output_dir = _file_directory(jar_dir)
        _look_for_jars(jar_dir, jad_app, output_dir, jad_options)
    else:
        SystemError("No file('s) provided to decompile ")


