# -*- coding: utf-8 -*-
"""
"""
import uuid
from typing import Any

import aiopg
import sqlalchemy as sa
from sqlalchemy.sql import TableClause
metadata = sa.MetaData()


class RecordNotFount(Exception):
    pass


class BaseModel(object):

    table = None

    _engine = None
    _data = {}
    _hash = 0

    def __init__(self, engine: 'aiopg._EngineContextManager', *args, **kwargs):
        self._engine = engine
        if 'id' not in kwargs:
            kwargs['id'] = str(uuid.uuid4())
        self._data = kwargs
        if isinstance(kwargs['id'], (bytes, bytearray, str)):
            self._hash = sum(map(ord, kwargs['id']))
        else:
            self._hash = int(kwargs['id'])

    async def _execute(self, query):
        assert self._engine
        async with self._engine.acquire() as conn:
            return await conn.execute(query)

    async def _update(self, **kwargs):
        query = self.__class__.update_query(values=kwargs)\
            .where(self.table.c.id == self.id)
        res = await self._execute(query)
        self._data.update(kwargs)
        return res

    def __getattr__(self, item):
        return self._data[item]

    def __setattr__(self, key, value):
        if key in self._data:
            self._data[key] = value
        else:
            super().__setattr__(key, value)

    def __getitem__(self, item):
        return self.__dict__.get(item, self._data[item])

    def __eq__(self, other):
        return self.id == getattr(other, 'id')

    def __hash__(self):
        return self._hash

    def __repr__(self):
        return '{}'.format(self._data)

    @classmethod
    def table(cls) -> 'sa.Table':
        return cls.table

    @classmethod
    def columns(cls) -> 'sa.Table.columns':
        return cls.table.columns

    @classmethod
    def select_query(cls, *args, **kwargs)\
            -> 'sqlalchemy.sql.selectable.Select':
        return cls.table.select(*args, **kwargs)

    @classmethod
    def update_query(cls, *args, **kwargs):
        return cls.table.update(*args, **kwargs)

    @classmethod
    def insert_query(cls, *args, **kwargs):
        return cls.table.insert(*args, **kwargs)

    @classmethod
    async def find_all(cls, engine: 'aiopg._EngineContextManager',
                       query: 'TableClause'=None):
        if query is None:
            query = cls.select_query()
        async with engine.acquire() as conn:
            async for item in conn.execute(query):
                yield cls(engine, **item)

    @classmethod
    async def find(cls, engine: 'aiopg._EngineContextManager', id: Any):
        query = cls.select_query().where(cls.table.c.id == id)
        async with engine.acquire() as conn:
            item = await (await conn.execute(query)).first()
            if not item:
                raise RecordNotFount('by id {}'.format(id))
            return cls(engine, **item)
