__author__ = 'pussbb'

__all__ = ['decompile_wrapper', 'absolute_file_path', 'parse_arguments',
           'look_for_jars',]

import os

def absolute_file_path(file_name):
    """ Return absolute file path

    @param file_name:
    @return:string
    """
    return os.path.dirname(os.path.realpath(file_name))


def decompile_wrapper(func):
    """

    @param func:
    @return:
    """

    def real_decorator(app, file_, output_dir=None, options=None):
        """

        @param jad_app:
        @param file_:
        @param output_dir:
        @param jad_options:
        @return:
        """
        if not output_dir or not os.path.isdir(output_dir):
            output_dir = absolute_file_path(file_)
        if options and isinstance(options, basestring):
            options = options.split(',')
        return func(app, file_, output_dir, options)

    return real_decorator


def look_for_jars(func, app, directory, output_dir, options):
    """

    @param jad_app:
    @param directory:
    @param output_dir:
    @param jad_options:
    @return:
    """
    print(output_dir)
    for root, _, files in os.walk(directory, followlinks=True):
        for file_name in files:
            if not file_name.lower().endswith('.jar'):
                continue
            func(app, os.path.join(root, file_name),
                          output_dir, options)


def parse_arguments(args):
    jar = args['--jar']
    jar_dir = args['--jar_dir']
    output_dir = args['--dir']
    options = args['--options']

    if options and isinstance(options, basestring):
        options = options.split(',')

    if jar and not output_dir:
        output_dir = absolute_file_path(jar)

    if jar_dir:
        jar_dir = os.path.abspath(jar_dir)
        if not output_dir:
            output_dir = jar_dir

    return (jar, jar_dir, output_dir, options)
