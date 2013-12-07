# -*- coding: utf-8 -*-

"""
for Python 3 only
"""

__author__ = 'pussbb'

import subprocess
import sys
import time
import pipes

class MPlayerException(Exception):
    pass

class MPlayer(object):

    def __init__(self, *args, **kwargs):
        self.mplayer_exe = MPlayer.get_mplayer_system_path()
        self.__mp_proc = None
        self.__init_mplayer_commands()
        self.__start_mplayer()


    def __del__(self):
        if self.__mp_proc:
            self.quit()

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
                                bufsize=-1,
                                universal_newlines=True)

    @staticmethod
    def get_mplayer_system_path():
        if not sys.platform.startswith('linux'):
            raise MPlayerException('Not supported platform')

        proc = MPlayer.__create_proc('type -P mplayer')
        stdout, stderr = proc.communicate()
        if proc.returncode != 0:
            raise MPlayerException('Cold not find mplayer')
        return stdout.split()[0]

    def __init_mplayer_commands(self):
        proc = MPlayer.__create_proc(self.mplayer_exe, '-input', 'cmdlist')
        stdout, stderr = proc.communicate()
        if proc.returncode != 1:
            raise MPlayerException('Cold not fetch cmdlist')
        types = {
            'String': str,
            'Integer': int,
            'Float': float,
        }
        for cmd_str in stdout.split('\n')[:-2]:
            cmd_name, *args = tuple(cmd_str.split())
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
                cmd_args.append(cmd_data['args'][i](arg))

            cmd_str = '{0:s} {1}\n'.format(cmd, " ".join(cmd_args))
            self.__mp_proc.stdin.write(cmd_str)
            self.__mp_proc.stdin.flush()
            print(self.__mp_proc.stdout.newlines)
            if cmd.startswith('get'):
                print(self.__mp_proc.stdout.read())
        return wrapper

    def __start_mplayer(self):
        args = [
            self.mplayer_exe,
            '-slave',
            '-idle',
            '-nolirc',
            '-nocache',
            '-prefer-ipv4',
            #'-really-quiet'
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
               '7d7dee0f0afb779457bf4c9a690c759d36163d4c/9b6db7e4bd.mp3')
    #p.quit()
    #print(p.is_running())
    time.sleep(3)
    p.get_percent_pos()
    #p.pause()
    #time.sleep(4)
    #p.pause()
    #time.sleep(573)
    p.quit()
    print(p.is_running())
