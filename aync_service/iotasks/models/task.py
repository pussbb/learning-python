# -*- coding: utf-8 -*-
"""
"""

from typing import List

from sqlalchemy import null, false
from sqlalchemy.dialects.postgresql import JSONB, UUID

from . import sa, metadata, BaseModel

tasks = sa.Table(
    'main_task',
    metadata,
    sa.Column('id', UUID(), primary_key=True),
    sa.Column('ext_id', sa.Integer),
    sa.Column('name', sa.String(200), nullable=False),
    sa.Column('params', JSONB, default=dict, nullable=False),
    sa.Column('status', sa.Integer, nullable=False),
    sa.Column('result', JSONB, default=dict, nullable=False),
    sa.Column('completed_at', sa.DateTime),
    sa.Column('parser_id', sa.Integer, sa.ForeignKey('main_parser.id')),
    sa.Column('callback', sa.String(500), nullable=True),
    sa.Column('callback_done', sa.Boolean, nullable=False, default=False),
    sa.Column('callback_http_status', sa.Integer, nullable=True),
    sa.Column('add_task_retries', sa.Integer, default=0),
    sa.Column('callback_retries', sa.Integer, default=0),
    sa.Column('on_error_retries', sa.Integer, default=0),
)


class Task(BaseModel):
    table = tasks

    STATUS_NEW = 1
    STATUS_RUNNING = 2
    STATUS_PENDING = 3
    STATUS_COMPLETED = 4
    STATUS_ERROR = 5

    @classmethod
    async def by_status(cls, engine, status, limit=10, exclude=None) \
            -> List['Task']:
        query = Task.select_query()
        if isinstance(status, (bytearray, bytes, str)):
            query = query.where(tasks.c.status == status)
        else:
            query = query.where(tasks.c.status.in_(status))
            if Task.STATUS_COMPLETED in status:
                query = query.where(tasks.c.callback != null())\
                    .where(tasks.c.callback_done == false())
        if exclude:
            query = query.where(tasks.c.id.notin_(exclude))
        query = query.order_by(tasks.c.created_at.desc()).limit(limit)
        async for task in cls.find_all(engine, query):
            yield task

    def is_new(self):
        return self.status == Task.STATUS_NEW

    def is_completed(self):
        return self.status == Task.STATUS_COMPLETED

    def is_pending(self):
        return self.status == Task.STATUS_PENDING

    async def set_parser(self, parser_id, ext_id):
        await self._update(parser_id=parser_id,
                           status=Task.STATUS_RUNNING,
                           ext_id=ext_id)

    async def set_parser_failed(self, parser_id, exception):
        await self._update(parser_id=parser_id,
                           status=Task.STATUS_ERROR,
                           parser_status=str(exception),
                           add_task_retries=self.add_task_retries + 1)

