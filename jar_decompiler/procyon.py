
# -*- coding: utf-8 -*-
"""Procyon decompiler helper script.

Usage:
  procyon.py --dec=<dec> ( --jar=<jar> | --jar_dir=<jar_dir> ) \
  [ --dir=<dir> | --options=<options> ]
  procyon.py (-h | --help)
  procyon.py --version

Options:
  -h --help                     Show this screen.
  --version                     Show version.
  --dec=<dec>                   JAD decompiler
  --jar=<jar>                   Jar file
  --jar_dir=<jar_dir>           Directory with jars
  --dir=<dir>                   Directory to output


"""
#python 2 support
from __future__ import unicode_literals, print_function

import os
import subprocess

from jar_decompiler import *


__author__ = 'pussbb'
__version__ = '0.0.1'
__all__ = ['decompile_class', 'decompile_jar', 'look_for_jars', ]

@decompile_wrapper
def decompile(decompiler, jar, output_dir=None, options=None):
    """

    @param decompiler:
    @param jar:
    @param output_dir:
    @param options:
    @return:
    """

    if not output_dir:
        output_dir = absolute_file_path(jar)

    basename = os.path.basename(jar)
    if not output_dir.endswith(basename):
        output_dir = os.path.join(output_dir, basename)

    command = [
        'java',
        '-jar',
        decompiler,
        '-jar',
        jar,
    ]
    if output_dir:
        command.extend(['-o', output_dir])
    if options:
        command.extend(options)

    subprocess.call(command)

def main(args):
    """

    @param args:
    @return:
    """
    decompiler = os.path.abspath(args['--dec'])
    if not os.path.isfile(decompiler):
        raise SystemError("Procyon decompiler not found")

    jar, jar_dir, output_dir, options = parse_arguments(args)

    if jar:
        decompile(decompiler, jar, output_dir, options)
    elif jar_dir:
        look_for_jars(decompile, decompiler, jar_dir, output_dir, options)
    else:
        raise SystemError("no file('s) provided to decompile ")


if __name__ == '__main__':
    from docopt import docopt
    ARGS = docopt(__doc__, version=__version__)
    main(ARGS)

