# -*- coding: utf-8 -*-
"""
"""
from aiohttp import web

from iotasks.models.parsers import Parser
from iotasks.models.task import Task


async def index(request):
    parser = await Parser.find(request.app.db_engine, 1)
    print(parser)
    async for task in Task.find_all(request.app.db_engine):
        print(task)

    return web.Response(text='Hello Aiohttp!')
