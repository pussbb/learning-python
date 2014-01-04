# -*- coding: utf-8 -*-

"""
Wrapper for MPlayer.
To get list of supported commands execute
$ mplayer -input cmdlist

all commands from that list are available as functions.
Also :
    - all commands which starts with 'get_' available as readonly properties
     without 'get_' substring
    e.g. get_percent_pos = obj.percent_pos
    - all commands which starts with 'set_' available as properties
     without 'set_' substring
    - send command to Mplayer is simple
        p.volume = [90.0, 1] | p.volume = 90.0, 1 | p.volume(90.0, 1)
all parameters which passing will convert to types which MPlayer expect
if command except Float param will convert to Float etc. Also it controls amount
of params for command. E.g.
seek                 Float [Integer] [Integer]
p.seek() - will raise exception 'Not enough args'
p.seek(34.4, 5, 5, 5) - will raise to many args
"""

__author__ = 'pussbb'

import subprocess
import sys
import time
import pipes

class MPlayerException(Exception):
    pass

class MPlayer(object):

    def __init__(self):
        self.mplayer_exe = MPlayer.get_mplayer_system_path()
        self.__mp_proc = None
        self.__init_mplayer_commands()
        self.__start_mplayer()

    def __del__(self):
        if self.__mp_proc:
            self.quit()

    def __setattr__(self, key, value):
        if hasattr(self, key) and callable(getattr(self, key)):
            self.__set_property(key, value)
        else:
            object.__setattr__(self, key, value)

    @staticmethod
    def __create_proc(*args):
        if len(args) == 1:
            args = args[0]

        if isinstance(args, (list, tuple)):
            cmd = []
            for item in args:
                cmd.append(pipes.quote(item))
            args = " ".join(cmd)

        return subprocess.Popen(args,
                                executable='/bin/bash',
                                shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                stdin=subprocess.PIPE,
                                close_fds=True,
                                universal_newlines=True)

    @staticmethod
    def get_mplayer_system_path():
        if not sys.platform.startswith('linux'):
            raise MPlayerException('Not supported platform')

        proc = MPlayer.__create_proc('type -P mplayer')
        stdout, _ = proc.communicate()
        if proc.returncode != 0:
            raise MPlayerException('Cold not find mplayer')
        return stdout.split()[0]

    def __init_mplayer_commands(self):
        proc = MPlayer.__create_proc(self.mplayer_exe, '-input', 'cmdlist')
        stdout, _ = proc.communicate()
        if proc.returncode != 1:
            raise MPlayerException('Cold not fetch cmdlist')
        types = {
            'String': str,
            'Integer': int,
            'Float': float,
        }
        for cmd_str in stdout.split('\n')[:-2]:
            cmd_name, *args =tuple(cmd_str.split())
            if hasattr(self, cmd_name):
                continue
            required_count = 0
            args_ = []
            for arg in args:
                if not arg.startswith('['):
                    required_count += 1
                args_.append(types[arg.strip('[]')])

            cmd_data = {
                'required_count': required_count,
                'help': cmd_str,
                'args': args_,
            }

            setattr(self, cmd_name, self.__exec_mp_cmd(cmd_name, cmd_data))
            self.__add_property(cmd_name)

    def __add_property(self, name):
        fget = None
        fset = None
        cmd = name
        prop_name = name[4:]
        if name.startswith('get'):
            # fget - readonly
            fget = lambda self: getattr(self, cmd)()
        elif name.startswith('set'):
            fset = lambda self, value: self.__set_property(cmd, value)

        if hasattr(self, prop_name) or (fget is None and fset is None):
            return

        setattr(self.__class__, prop_name, property(fget, fset))


    def __set_property(self, name, value):
        if isinstance(value, (list, tuple)):
            return getattr(self, name)(*value)
        return getattr(self, name)(value)

    def __exec_mp_cmd(self, cmd, cmd_data):
        def wrapper(*args):
            if not self.is_running():
                raise MPlayerException('Mplayer unexpectedly exit')

            if cmd_data['required_count'] > len(args):
                raise MPlayerException("Not enough args."
                                       "\nUsage:{0}".format(cmd_data['help']))

            if len(cmd_data['args']) < len(args):
                raise MPlayerException("Too many args."
                                       "\nUsage:{0}".format(cmd_data['help']))

            cmd_args = []
            for i, arg in enumerate(args):
                cmd_args.append(str(cmd_data['args'][i](arg)))

            cmd_str = '{0:s} {1}\n'.format(cmd, " ".join(cmd_args))

            self.__mp_proc.stdin.write(cmd_str)
            self.__mp_proc.stdin.flush()

            if cmd.startswith('get'):
                while True:
                    try:
                        line = self.__mp_proc.stdout.readline().strip()
                        if line.startswith('ANS'):
                            return line.split('=')[1].strip(' \'')
                    except UnicodeDecodeError as _:
                        pass
        wrapper.__name__ = cmd
        wrapper.__doc__ = cmd_data['help']
        return wrapper

    def __start_mplayer(self):
        args = [
            self.mplayer_exe,
            '-slave',
            '-idle',
            '-nolirc',
            '-nocache',
            '-prefer-ipv4',
            '-quiet',
            '-nocolorkey',
            '-noconsolecontrols',
            '-nofontconfig',
            '-msglevel',
            'all=4',
        ]
        self.__mp_proc = MPlayer.__create_proc(args)
        if not self.is_running():
            raise MPlayerException("Couldnot start mplayer proccess")


    def is_running(self):
        return self.__mp_proc.poll() is None

if __name__ == "__main__":
    p = MPlayer()

    p.loadfile('http://s8-3.pleer.com/0357febeb13357987027cde2cd05b43d90b2a23a'
               '35a5918cfa565c8ead4c9e50b5469a762150ef921c6e83d5246c8e4d5ff861'
               '7d7dee0f0afb779457bf4c9a690c759d36163d4c/9b6db70bc1.mp3')
    #p.quit()
    #print(p.is_running())
    time.sleep(3)
    #print(p.volume)
    p.volume = [30.0, 4]

    #print(p.volume)
    print(p.percent_pos)
    print(p.audio_bitrate)
    time.sleep(3)
    p.volume(90.0, 4)
    print(p.get_time_pos())
    #p.pause()
    time.sleep(4)
    print(p.get_percent_pos())
    #p.pause()
    time.sleep(573)
    p.quit()
    print(p.is_running())
