# -*- coding: utf-8 -*-
"""

"""
import asyncio
import io
import shlex
from asyncio.subprocess import PIPE
from contextlib import closing

import atexit

atexit.register(asyncio.get_event_loop().close)


class ShellIORedirection(object):

    __slots__ = ('input', 'redir', 'out')

    def __init__(self, in_='', redir='', out=''):
        self.input = in_
        self.redir = redir
        self.out = out

    def __repr__(self):
        return "{}{}{}".format(self.input, self.redir, self.out)

    @staticmethod
    def error_to_out():
        return ShellIORedirection(2, '>&', 1)


def is_quoted(line):
    return not set([line[0], line[-1]]) - set(['"', '\'']) and len(line) > 1


def _unify_newlines(s):
    r'''Because all asyncio subprocess output is read in binary mode, we don't
    get universal newlines for free. But it's the right thing to do, because we
    do all our printing with strings in text mode, which translates "\n" back
    into the platform-appropriate line separator. So for example, "\r\n" in a
    string on Windows will become "\r\r\n" when it gets printed.'''

    return s.replace(b'\r\n', b'\n')


class ShellCommand(object):

    __slots__ = ('__command', '__command_args', '__proccess', '__output')

    def __init__(self, command, *args, full_path=True, **kwargs):
        if full_path:
            command = '$(type -P {0})'.format(command)
        self.__command = command
        self.__command_args = []
        self.__append_arguments(*args, **kwargs)
        self.__proccess = None
        self.__output = io.BytesIO()

    def __append_arguments(self, *args, **kwargs):
        for item in args:
            if not isinstance(item, ShellIORedirection):
                item = str(item)
                if not is_quoted(item):
                    item = shlex.quote(str(item))
            self.__command_args.append(item)

        for key, value in kwargs.items():
            self.__command_args.append("{}={}".format(key, value))

    @property
    def name(self):
        return self.__command

    @property
    def arguments(self):
        return self.__command_args

    def extend(self, *args, **kwargs):
        self.__append_arguments(*args, **kwargs)

    def __gt__(self, other):
        self.__command_args.extend(['>', str(other)])
        return self

    def __rshift__(self, other):
        self.__command_args.extend(['>>', str(other)])
        return self

    def __or__(self, other):
        if not isinstance(other, ShellCommand):
            raise RuntimeError('Object is not instance of ShellCommand')
        self.__command_args.extend(['||', str(other)])
        return self

    def __and__(self, other):
        if not isinstance(other, ShellCommand):
            raise RuntimeError('Object is not instance of ShellCommand')
        self.__command_args.extend(['&&', str(other)])
        return self

    def __add__(self, other):
        if not isinstance(other, (ShellCommand, ShellIORedirection)):
            raise RuntimeError('Object is not instance of ShellCommand')
        if isinstance(other, ShellIORedirection):
            self.__command_args.extend([str(other)])
        else:
            self.__command_args.extend(['|', str(other)])
        return self

    def __eq__(self, other):
        return str(self) == str(other)

    def build(self):
        args = ' '.join([str(item) for item in self.__command_args])
        return "{} {}".format(self.__command, args).strip()

    def __repr__(self):
        return self.build()

    async def run(self, handler=None):
        self.__proccess = await asyncio.create_subprocess_shell(
                str(self),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
                executable='/bin/bash',
        )

        self.__output = io.BytesIO()
        async for line in self.__proccess.stdout:
            line = _unify_newlines(line)
            self.__output.write(line)
            if handler:
                handler(line)

        return await self.__proccess.wait()

    def execute(self, handler=None):
        with closing(asyncio.get_event_loop()) as loop:
            loop.run_until_complete(self.run(handler))

    def returncode(self):
        return self.__proccess.returncode

    def output(self):
        return self.__output.getvalue().split(b'\n')

ss = ShellCommand('cat', '/opt/Exchange_Protocols/[MS-ASAIRS].pdf')

def hh(line):
    print('got line', line)
ss.execute(handler=hh)

print(ss.returncode())
print(ss.output())
