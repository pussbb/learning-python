# -*- coding: utf-8 -*-
"""Jad decompiler helper script

Usage:
  jad.py --jad=<jad> ( --jar=<jar> | --jar_dir=<jar_dir> ) \
  [ --dir=<dir> | --options=<options> ]
  jad.py (-h | --help)
  jad.py --version

Options:
  -h --help                     Show this screen.
  --version                     Show version.
  --jad=<jad>                   JAD decompiler
  --jar=<jar>                   Jar file
  --jar_dir=<jar_dir>           Directory with jars
  --dir=<dir>                   Directory to output
  --options=<options>   Additional options for jad decompiler
                                (comma separated)

"""
#python 2 support
from __future__ import unicode_literals, print_function

__author__ = 'pussbb'
__version__ = '0.0.1'
__all__ = ['decompile_class', 'decompile_jar',
           'LOGGER', ]

import os
import zipfile
import subprocess

from jar_decompiler import *

LOGGER = None
#DEBUG = False

def log_wrapper(func):
    """

    @param func:
    @return:
    """

    def real_wrapper(msg):
        """

        @param msg:
        @return:
        """
        if LOGGER:
            return func(msg)

    return real_wrapper


@log_wrapper
def audit_info(msg):
    """

    @param msg:
    @return:
    """
    LOGGER.info(msg)


@log_wrapper
def audit_warning(msg):
    """

    @param msg:
    @return:
    """
    LOGGER.warning(msg)


@log_wrapper
def audit_debug(msg):
    """

    @param msg:
    @return:
    """
    LOGGER.debug(msg)


def extract_jar(jar, path=None):
    """ Unpack jar file

    @param jar:
    @param path:
    """
    jar_file = zipfile.ZipFile(jar)
    if not path or not os.path.isdir(path):
        path = absolute_file_path(jar)
    path = os.path.join(path, os.path.basename(jar))
    jar_file.extractall(path)


@decompile_wrapper
def decompile_class(jad_app, class_file, output_dir=None, jad_options=None):
    """ Decompile class into java source file and remove compiled file

    @param jad_app:
    @param class_file:
    @param output_dir:
    @param jad_options:
    """
    command = [
        jad_app,
        '-o',
        '-sjava',
        '-d{0}'.format(output_dir),
        class_file,
    ]

    if isinstance(jad_options, list):
        command.extend(jad_options)

    audit_debug("Run command {0}".format(' '.join(command)))

    process = subprocess.Popen(command, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               universal_newlines=True)
    stdout, stderr = process.communicate()

    audit_info(stdout)
    audit_warning(stderr)

    os.remove(class_file)


@decompile_wrapper
def decompile_jar(jad_app, jar, output_dir=None, jad_options=None):
    """ Uncompress jar file and decompile all classes

    @param jad_app:
    @param jar:
    @param output_dir:
    @param jad_options:
    """
    extract_jar(jar, output_dir)

    for root, _, files in os.walk(output_dir, followlinks=True):
        for name in files:
            if not name.lower().endswith('.class'):
                continue
            decompile_class(jad_app, os.path.join(root, name),
                            root, jad_options)


def main(args):
    """

    @param args:
    @return:
    """
    jad_app = os.path.abspath(args['--jad'])
    if not os.path.isfile(jad_app):
        raise SystemError("jad decompiler not found")

    jar, jar_dir, output_dir, options = parse_arguments(args)

    if jar:
        decompile_jar(jad_app, jar, output_dir, options)
    elif jar_dir:
        look_for_jars(decompile_jar, jad_app, jar_dir, output_dir, options)
    else:
        raise SystemError("no file('s) provided to decompile ")


if __name__ == '__main__':
    from docopt import docopt

    ARGS = docopt(__doc__, version=__version__)

    import logging

    LOGGER = logging.getLogger('jar_decompiler')
    LOGGER.addHandler(logging.FileHandler('jar_decompiler.log'))
    LOGGER.setLevel(logging.DEBUG)

    main(ARGS)


