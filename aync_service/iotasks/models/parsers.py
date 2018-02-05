# -*- coding: utf-8 -*-
"""
"""
from typing import List

from sqlalchemy import true

from .task import Task
from ..aparser_client import AParserClient, ApiError
from . import sa, metadata, BaseModel

parsers = sa.Table('main_parser', metadata,
                   sa.Column('id', sa.Integer, primary_key=True),
                   sa.Column('url', sa.String(200), nullable=False),
                   sa.Column('password', sa.String(200), nullable=False),
                   sa.Column('is_active', sa.Boolean, nullable=False),
                   sa.Column('status', sa.Integer, nullable=False),
                   sa.Column('slots_number', sa.Integer),
                   )


class Parser(BaseModel, AParserClient):

    table = parsers

    def __init__(self, engine, **kwargs):
        BaseModel.__init__(self, engine=engine, **kwargs)
        AParserClient.__init__(self, self.url, self.password)

    async def is_available(self):
        if not self.is_active:
            return False
        try:
            info = await self.info()
        except ApiError as _:
            return False
        else:
            return (self.slots_number - info['tasksInQueue']) > 0

    async def add_task(self, task: Task):
        await task.set_parser(self.id, await super().add_task(task.id))
        return task

    @staticmethod
    async def get_active(engine) -> List['Parser']:
        query = Parser.select_query().where(parsers.c.is_active == true())
        query = query.order_by(parsers.c.slots_number.desc())
        async for parser in Parser.find_all(engine, query):
            yield parser

    @staticmethod
    async def get_available(engine) -> List['Parser']:
        async for parser in Parser.get_active(engine):
            if not await parser.is_available():
                continue
            yield parser
