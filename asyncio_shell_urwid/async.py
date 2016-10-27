# -*- coding: utf-8 -*-

import asyncio
import urwid

from shell_command import _LOOP, ShellCommand

#_LOOP.set_debug(True)

cmd = ShellCommand('sudo', 'apt', 'install', 'aptitude')


class ScrollableList(urwid.ListBox):

    auto_focus = True

    def __init__(self, container=None):
        if not container:
            container = []
        self.walker = urwid.SimpleFocusListWalker(container)
        super().__init__(self.walker)
        urwid.connect_signal(self.walker, 'modified', self.modified)

    def modified(self):
        pass

    def append(self, item):
        assert isinstance(item, (bytearray, bytes)), 'Item must be byte or bytearray object'
        text_widget = urwid.Text(item)
        self.walker.append(text_widget)
        if self.auto_focus:
            self.focus_next()
        return text_widget

    def focus_next(self):
        widget, pos = self.walker.get_focus()
        widget, pos = self.walker.get_next(pos)
        if widget:
            self.set_focus(pos)

    def unhandled_keypress(self, key):
        if urwid.is_mouse_event(key):
            if int(key[1]) == 4:
                self._keypress_page_up(key[2:])
            if int(key[1]) == 5:
                self._keypress_page_down(key[2:])
        return key

    def __len__(self):
        return len(self.walker)

    def __iter__(self):
        yield from self.walker


class CommandWidget(ScrollableList):

    __cmd = None
    __proc = None
    __loop = None
    __last_item = None
    exit_code = None

    def __init__(self, command, loop):
        super().__init__()
        self.__cmd = command
        self.__loop = loop
        self.append(str(self.__cmd).encode())
        self.__new_element()

    def render(self, size, focus=False):
        w = super().render(size, focus)
        if not self.__proc:
            self.__loop.call_later(0.3, self._run)
        return w

    def _run(self):
        if self.__proc:
            return
        asyncio.wait(asyncio.ensure_future(self.execute()))

    @asyncio.coroutine
    def _read_stream(self, stream):
        while not stream.at_eof():
            data = yield from stream.read(1)
            if b'\n' == data:
                self.__new_element()
            else:
                self.__last_item_update_text(data)

    async def execute(self):
        self.__proc = await asyncio.create_subprocess_shell(
            str(self.__cmd),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
            executable='/bin/bash',
        )

        await self._read_stream(self.__proc.stdout)

        self.exit_code = await self.__proc.wait()
        self.append('Exited with:{}'.format(self.exit_code).encode())

    def unhandled_keypress(self, key):
        if len(key) == 1:
            self.__send_to_stdin(key)
        if key == 'enter':
            self.__send_to_stdin(b'\n')
            self.__new_element()

        return super().unhandled_keypress(key)

    def __new_element(self):
        self.__last_item = self.append(b'+# ')

    def __last_item_update_text(self, text):
        if self.__last_item.text.endswith(b'\r'):
            text = b'+# ' + text
        else:
            text = self.__last_item.text + text
        self.__last_item.set_text(text)

    def __send_to_stdin(self, key):
        if self.__proc.stdin and not self.__proc.stdin.at_eof():
            self.__proc.stdin.write(key)
            self.__proc.stdin.flush()


out_widget = CommandWidget(cmd, _LOOP)

main_widget = urwid.Frame(
    body=out_widget,
    focus_part='body'
)

urwid_loop = urwid.MainLoop(
    main_widget,
    unhandled_input=out_widget.unhandled_keypress,
    event_loop=urwid.AsyncioEventLoop(loop=_LOOP),
)
urwid_loop.run()
