# -*- coding: utf-8 -*-
"""

"""
import asyncio
import io
import os
import shlex
import atexit

_LOOP = asyncio.get_event_loop()
atexit.register(_LOOP.close)


class ShellCommandRuntimeException(Exception):
    """General exception for failed shell commands. Raised when shell command
    returns with nonzero exit code

    """

    def __init__(self, command, response):
        self.message = 'External command. Failed to execute "{cmd}"' \
                       ' {resp}'.format(resp=response, cmd=command)
        super().__init__(self.message)
        self.result = response
        self.command = command


class ShellCommandNotFound(ShellCommandRuntimeException):
    """Helper exception for exit code 127 - when there are no such command

    """
    pass


class ShellIORedirection(object):
    """Helper class to create IO redirection and append them into ShellCommand

    """

    __slots__ = ('input', 'redir', 'out')

    def __init__(self, in_='', redir='', out=''):
        self.input = in_
        self.redir = redir
        self.out = out

    def __repr__(self) -> str:
        return "{}{}{}".format(self.input, self.redir, self.out)

    @staticmethod
    def error_to_out() -> str:
        """Creates 2>&1 shell redirection

        :return: ShellIORedirection object
        """
        return ShellIORedirection(2, '>&', 1)


def is_quoted(data) -> bool:
    """Checks if string is surrounded with ' or "

    :param data: string
    :return: True if it escaped otherwise False
    """
    return not set([data[0], data[-1]]) - set(['"', '\'']) and len(data) > 1


def _unify_newlines(s) -> bytes:
    r'''Because all asyncio subprocess output is read in binary mode, we don't
    get universal newlines for free. But it's the right thing to do, because we
    do all our printing with strings in text mode, which translates "\n" back
    into the platform-appropriate line separator. So for example, "\r\n" in a
    string on Windows will become "\r\r\n" when it gets printed.'''

    return s.replace(b'\r\n', b'\n')


def using_command_full_path(name, use_which=False) -> str:
    """Dummy function which will wrap command name with extra commands
    which help to determine full path of executable and run it.
    By default it will use command `type -P` to determine executable full path
    because command `which` can be not installed on some systems but
    `type ` is always there. And also `which` has a cache and sometimes it
    needs a time to get path to some executable.

    :param name: string
    :param use_which: boolean if True it will use `which`
    :return:
    """
    command = 'type -P'
    if use_which:
        command = 'which'
    return '$({} {})'.format(command, name)


class ShellCommand(object):
    """Build shell command

    """

    __slots__ = ('__command', '__command_args',)

    class Response(object):
        """Helper class to represent results of executed command

        """

        __slots__ = ('__exit_code', '__response')

        def __init__(self, exit_code, response):
            self.__exit_code = exit_code
            self.__response = response

        @property
        def exit_code(self) -> int:
            """Returns command exit code

            :return: int
            """
            return self.__exit_code

        @property
        def response(self) -> bytes:
            """Returns command output

            :return: bytes
            """
            return self.__response.getvalue()

        def __iter__(self):
            yield from self.__response.getvalue().split(b'\n')

        def __repr__(self) -> str:
            return 'Command exit code {}. Response: {}'.format(
                    self.__exit_code, self.response)

    def __init__(self, command, *args, **kwargs):
        self.__command = command
        self.__command_args = []
        self.__append_arguments(*args, **kwargs)

    def __append_arguments(self, *args, **kwargs):
        """Append arguments into command

        :param args: list
        :param kwargs: dict
        :return:
        """
        for item in args:
            if not isinstance(item, ShellIORedirection):
                item = str(item)
                if not is_quoted(item):
                    item = shlex.quote(str(item))
            self.__command_args.append(item)

        for key, value in kwargs.items():
            self.__command_args.append("{}={}".format(key, value))

    @property
    def name(self) -> str:
        """Command name

        :return: string
        """
        return os.path.basename(self.__command)

    @property
    def basename(self) -> str:
        """Command base nname

        :return: string
        """
        return os.path.basename(self.__command)

    @property
    def arguments(self) -> list:
        """Command arguments

        :return: list
        """
        return self.__command_args

    def extend(self, *args, **kwargs):
        """Add extra command arguments

        :param args:
        :param kwargs:
        :return: None
        """
        self.__append_arguments(*args, **kwargs)

    def __gt__(self, other):
        """Creates shell IO redirection '>'

        :param other:
        :return: self
        """
        self.__command_args.extend(['>', str(other)])
        return self

    def __lt__(self, other):
        """Creates shell IO redirection '<'

        :param other:
        :return: self
        """
        self.__command_args.extend(['<', str(other)])
        return self

    def __rshift__(self, other):
        """Creates shell IO redirection '>>'

        :param other:
        :return: self
        """
        self.__command_args.extend(['>>', str(other)])
        return self

    def __or__(self, other):
        """Adds new command with logical || into existing command

        :param other:
        :return: self
        """
        if not isinstance(other, ShellCommand):
            raise RuntimeError('Object is not instance of ShellCommand')
        self.__command_args.extend(['||', str(other)])
        return self

    def __and__(self, other):
        """Adds new command with logical && into existing command

        :param other:
        :return: self
        """
        if not isinstance(other, ShellCommand):
            raise RuntimeError('Object is not instance of ShellCommand')
        self.__command_args.extend(['&&', str(other)])
        return self

    def __add__(self, other):
        """Creates shell PIPE for another command by adding | before other
        command. If other is instance of ShellIORedirection it just appends it.

        :param other:
        :return:
        """
        if not isinstance(other, (ShellCommand, ShellIORedirection)):
            raise RuntimeError('Object is not instance of ShellCommand')
        if isinstance(other, ShellIORedirection):
            self.__command_args.extend([str(other)])
        else:
            self.__command_args.extend(['|', str(other)])
        return self

    def __eq__(self, other):
        """Just compare

        :param other:
        :return:
        """
        return str(self) == str(other)

    def __call__(self, handler=None):
        """Call class as a function
        Raises:
                ShellCommandNotFound - when command does not exists
                ShellCommandRuntimeException - if command execution returned
                nonzero exit code

        :param handler: callback function
        :return: ShellCommand.Response object
        """
        return self.execute(handler=handler)

    def build(self) -> str:
        """Builds command with all known arguments

        :return: string
        """
        args = ' '.join([str(item) for item in self.__command_args])
        return "{} {}".format(self.__command, args).strip()

    def __repr__(self):
        return self.build()

    async def run(self, handler=None):
        """Executes command asynchronously.

        :param handler: callable
        :return: ShellCommand.Response object
        """
        proc = await asyncio.create_subprocess_shell(
                str(self),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
                executable='/bin/bash',
        )

        if not handler:
            def dummy(_): pass
            handler = dummy
        response = io.BytesIO()
        async for line in proc.stdout:
            line = _unify_newlines(line)
            response.write(line)
            handler(line)

        exit_code = await proc.wait()
        del proc
        return ShellCommand.Response(exit_code, response)

    def execute(self, handler=None):
        """Executes command and wait's when it finish

        Raises:
                ShellCommandNotFound - when command does not exists
                ShellCommandRuntimeException - if command execution returned
                nonzero exit code

        :param handler: callable
        :return: ShellCommand.Response object
        """
        res = _LOOP.run_until_complete(self.run(handler))

        if res.exit_code == 0:
            return res

        exception = ShellCommandRuntimeException
        if res.exit_code == 127:
            exception = ShellCommandNotFound
        raise exception(str(self), res)


if __name__ == '__main__':
    import sys
    cmd = ShellCommand(sys.executable, '-h')
    print(cmd)
    print(cmd.basename)
    print(cmd())
    result = cmd.execute()
    print(result)
    print('*'*80)
    print('result.exit_code: ', result.exit_code)
    print('result.response: ', result.response)
    print('as list: ', list(result))
    print('lets iterate throw it: ', [line for line in result])
