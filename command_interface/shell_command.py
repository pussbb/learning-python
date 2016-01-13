# -*- coding: utf-8 -*-
"""

"""
import asyncio
import io
import shlex
import atexit

_LOOP = asyncio.get_event_loop()
atexit.register(_LOOP.close)


class ShellCommandRuntimeException(Exception):
    """General exception for failed shell commands. Raised when shell command
    returns with nonzero exit code

    """

    def __init__(self, command, exit_code, output):
        self.message = 'External command "{cmd}" failed to execute ended' \
                       ' with exit code {code}'.format(code=exit_code,
                                                       cmd=command)
        super().__init__(self.message)
        self.exit_code = exit_code
        self.output = output
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

    def __repr__(self):
        return "{}{}{}".format(self.input, self.redir, self.out)

    @staticmethod
    def error_to_out():
        """Creates 2>&1 shell redirection

        :return: ShellIORedirection object
        """
        return ShellIORedirection(2, '>&', 1)


def is_quoted(line):
    """Checks if string is surrounded with ' or "

    :param line: string
    :return: True if it escaped otherwise False
    """
    return not set([line[0], line[-1]]) - set(['"', '\'']) and len(line) > 1


def _unify_newlines(s):
    r'''Because all asyncio subprocess output is read in binary mode, we don't
    get universal newlines for free. But it's the right thing to do, because we
    do all our printing with strings in text mode, which translates "\n" back
    into the platform-appropriate line separator. So for example, "\r\n" in a
    string on Windows will become "\r\r\n" when it gets printed.'''

    return s.replace(b'\r\n', b'\n')


class ShellCommand(object):
    """Build shell command

    """

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
    def name(self):
        """Command name

        :return: string
        """
        return self.__command

    @property
    def arguments(self):
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

    def build(self):
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
        :return:
        """
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
        """Executes command and wait's when it finish

        Raises:
                ShellCommandNotFound - when command does not exists
                ShellCommandRuntimeException - if command execution returned
                nonzero exit code

        :param handler: callable
        :return: int command exit code
        """

        _LOOP.run_until_complete(self.run(handler))

        if self.exit_code() == 0:
            return self.exit_code()

        exception = ShellCommandRuntimeException
        if self.exit_code() == 127:
            exception = ShellCommandNotFound
        raise exception(str(self), self.exit_code(), self.output())

    def exit_code(self):
        """Returns exit code

        :return: int
        """
        if not self.__proccess:
            return None
        return self.__proccess.returncode

    def output(self, raw=True):
        """Returns command output

        :param raw: if True will return bytes if False list
        :return: bytes or string
        """
        if raw:
            yield self.__output.getvalue()
        yield from self.__output.getvalue().split(b'\n')
