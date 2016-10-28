# -*- coding: utf-8 -*-

import asyncio
from typing import Any, Iterable

import urwid

from shell_command import _LOOP, ShellCommand

_LOOP.set_debug(True)

cmd = ShellCommand('sudo', '-S', 'apt', 'install', 'aptitude')


class ScrollableList(urwid.ListBox):
    """

    """

    auto_focus = True

    def __init__(self, container=None):
        if not container:
            container = []
        self.walker = urwid.SimpleFocusListWalker(container)
        super().__init__(self.walker)
        urwid.connect_signal(self.walker, 'modified', self.modified)

    def modified(self) -> Any:
        """ Callback on list modified event

        :return:
        """
        pass

    def append(self, item: bytes) -> urwid.Text:
        """

        :param item: bytes
        :return:urwid.Text
        """
        assert isinstance(item, (bytearray, bytes)), 'Item must be byte or bytearray object'
        text_widget = urwid.Text(item)
        self.walker.append(text_widget)
        if self.auto_focus:
            self.focus_next()
        return text_widget

    def focus_next(self) -> None:
        """ Focus next element in list

        :return:
        """
        widget, pos = self.walker.get_focus()
        widget, pos = self.walker.get_next(pos)
        if widget:
            self.set_focus(pos)

    def unhandled_keypress(self, key: Any) -> Any:
        """Scroll page down Page Up on mouse scroll

        :param key:
        :return:
        """
        if urwid.is_mouse_event(key):
            if int(key[1]) == 4:
                self._keypress_page_up(key[2:])
            if int(key[1]) == 5:
                self._keypress_page_down(key[2:])
        return key

    def __len__(self) -> int:
        return len(self.walker)

    def __iter__(self) -> Iterable:
        yield from self.walker


class CommandWidget(ScrollableList, metaclass=urwid.signals.MetaSignals):
    """

    """

    signals = ['starting', 'finished']

    def __init__(self, command, loop):
        self.__cmd = command
        self.__loop = loop
        self.__proc = None
        self.__task = None
        self.__exit_code = None
        self.__last_item = None
        super().__init__()

    def render(self, size, focus=False) -> urwid.canvas.CanvasCombine:
        """ see :meth:`urwid.ListBox.render` for details
        :param size:
        :param focus:
        :return: urwid.canvas.CanvasCombine
        """
        canvas = super().render(size, focus)
        if not self.__task:
            self.__loop.call_soon(self._run)
        return canvas

    def _run(self) -> None:
        self.__task = asyncio.wait(asyncio.ensure_future(self.execute()))

    @property
    def exit_code(self) -> int:
        return self.__exit_code

    @property
    def output(self) -> Iterable:
        for item in self:
            yield item.text

    @asyncio.coroutine
    def _read_stream(self, stream: asyncio.StreamReader) -> None:
        """

        :param stream: asyncio.StreamReader
        :return: None
        """
        while not stream.at_eof():
            data = yield from stream.read(1)
            if data == b'\n':
                self.__new_element()
            else:
                self.__update_last_item_text(data)

    async def execute(self) -> None:
        """ Executes command

        :return: None
        """
        urwid.signals.emit_signal(self, 'starting', bytes(self.__cmd))
        self.__new_element()
        self.__proc = await self.__cmd.get_process()
        await self._read_stream(self.__proc.stdout)
        self.__exit_code = await self.__proc.wait()
        urwid.signals.emit_signal(self, 'finished', self.__exit_code)

    def unhandled_keypress(self, key: Any) -> Any:
        """

        :param key:
        :return:
        """
        if len(key) == 1:
            self.__forward_key(key)
        if key == 'enter':
            self.__forward_key(b'\n')
            self.__new_element()

        return super().unhandled_keypress(key)

    def __new_element(self):
        """ Creates new Text widget

        :return: None
        """
        self.__last_item = self.append(b'+# ')

    def __update_last_item_text(self, text: bytes) -> None:
        """ Append new text to the last Text widget

        :param text: bytes
        :return: None
        """
        if self.__last_item.text.endswith(b'\r'):
            text = b'+# ' + text
        else:
            text = self.__last_item.text + text
        self.__last_item.set_text(text)

    def __forward_key(self, key: bytes) -> None:
        """ Send key to process stdin pipe

        :param key: bytes
        :return: None
        """
        if not self.__proc:
            return
        if self.__proc.stdin and not self.__proc.stdin.at_eof():
            self.__proc.stdin.write(key)
            self.__proc.stdin.flush()


out_widget = CommandWidget(cmd, _LOOP)


def finished(x):
    out_widget.append(b'%# Exit code: ')
    for item in out_widget.output:
        print(item)


urwid.connect_signal(out_widget, 'starting', lambda x: out_widget.append(b'%# Starting ' + x))
urwid.connect_signal(out_widget, 'finished', finished)

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
