# -*- coding: utf-8 -*-
"""

"""

from __future__ import unicode_literals, print_function, absolute_import, \
    division

import collections
import os


PosixStatResultBase = collections.namedtuple(
    'PosixStatResult',
    ['st_mode', 'st_ino', 'st_dev', 'st_nlink', 'st_uid', 'st_gid', 'st_size',
     'st_atime', 'st_mtime', 'st_ctime']
)

TailResults = collections.namedtuple('TailResults', ['lines', 'last_position'])


class PosixStatResult(PosixStatResultBase):
    def __getattr__(self, item):
        return getattr(self, "st_{0}".format(item))

    def __iter__(self):
        for field in self._fields:
            yield field.replace('st_', ''), getattr(self, field)

    @classmethod
    def stats(cls, absolute_file_name):
        return cls(*os.stat(absolute_file_name))


def tail(file_name, last=10, last_pos=0):
    result = []
    if PosixStatResult.stats(file_name).size == 0:
        return TailResults(result, 0)
    with open(file_name, 'r') as fd:
        if last_pos:
            fd.seek(last_pos)
            result = fd.readlines()
            return TailResults(result, fd.tell())
        else:
            fd.seek(0, 2)
            pos = fd.tell()
            while True:
                pos -= pos // last
                if pos < last or pos < 0:
                    pos = fd.tell()
                fd.seek(0 - pos, 2)
                result = fd.readlines()
                if len(result) >= last or pos == fd.tell():
                    break
        file_pos = fd.tell()

    index = len(result) - last
    if index < 0:
        index = 0
    return TailResults(result[index:], file_pos)


def test():
    import random
    import subprocess

    for dir_path, _, files in os.walk('/var/log/'):
        for __ in range(5):
            file_ = os.path.join(dir_path, random.choice(files))
            line_num = random.randint(10, 120)
            print('Checking ', file_)
            assert b''.join(tail(file_, line_num).lines) == subprocess\
                .check_output(['tail', '-{0}'.format(line_num), file_])

        break


def test2(filename):
    """ tail -f

    :return:
    """
    last_pos = 0
    while True:
        result = tail(filename, last_pos=last_pos)
        last_pos = result.last_position
        if result.lines:
            print(''.join(result.lines), end='')

if __name__ == '__main__':
    test2('/var/log/syslog')
    test()
