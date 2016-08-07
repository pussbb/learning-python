# -*- coding: utf-8 -*-
"""

"""
import asyncio
import time

import atexit
from flask import Flask
from flask import Response
from flask import render_template
from flask import stream_with_context

from shell_command import ShellCommand

APP = Flask(__name__)

LOOP = asyncio.get_event_loop()
asyncio.set_event_loop(LOOP)
atexit.register(LOOP.close)
cmd = ShellCommand('tail', '/var/log/syslog')
cmd.execute()


@APP.route('/shell')
def shell():
    def events():
        ll = []

        def handler(item):
            ll.append(item)

        cmd = ShellCommand('cat', '/var/log/syslog')

        yield 'event: ping\n'
        yield 'data: Executing "{}"\n\n'.format(cmd)

        asyncio.set_event_loop(LOOP)
        future = asyncio.ensure_future(cmd.run(handler), loop=LOOP)

        while LOOP.run_until_complete(future):
            while ll:
                yield 'event: ping\n'
                yield 'data: {}\n\n'.format(ll.pop(0))
            else:
                if future.done():
                    break
            asyncio.sleep(.1)

        yield 'event: close\n'
        yield 'data: Done! Command {cmd}. Exit Code {exit_code}\n\n'.format(
            cmd=cmd, exit_code=future.result().exit_code
        )
    return Response(events(), content_type='text/event-stream')


@APP.route('/event')
def event():

    def events():
        for i in range(1, 100):
            yield 'event: ping\n'
            yield 'data: {}\n\n'.format(i)
            time.sleep(.4)
        yield 'event: close\n'
        yield 'data: Done!\n\n'

    return Response(stream_with_context(events()),
                    content_type='text/event-stream')


@APP.route('/')
def index():
    return render_template('index.html')


APP.run(port=8080, debug=False, threaded=True)

