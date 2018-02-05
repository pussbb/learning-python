# -*- coding: utf-8 -*-
"""
"""
import asyncio
import logging

from ..models.task import Task

logger = logging.getLogger(__name__)


class TaskProducerService(object):

    def __init__(self, db_engine, max_size, period: int=5):
        self.__max_size = max_size
        self._queue = asyncio.Queue()
        self._pending_queue = asyncio.Queue()
        self._db_engine = db_engine
        self._period = period
        self._in_progress = set()

    @property
    def new_tasks(self) -> asyncio.Queue:
        return self._queue

    @property
    def pending_queue(self) -> asyncio.Queue:
        return self._pending_queue

    async def run(self):
        while True:
            for item in ['new', 'pending']:
                try:
                    await getattr(self, 'check_{}_queue'.format(item))()
                except Exception as exp:
                    logger.exception(
                        'Checking for {} a task failed'.format(item),
                        exp
                    )
            await asyncio.sleep(self._period)

    async def get_tasks(self, status, limit=0):
        exclude = None
        if self._in_progress:
            exclude = [(yield item.id) for item in self._in_progress]
        async for task in Task.by_status(self._db_engine, status, limit,
                                         exclude):
            yield task

    async def check_new_queue(self):
        needed = self.__max_size - self._queue.qsize()
        if needed <= 0:
            return
        async for task in self.get_tasks(Task.STATUS_NEW, needed):
            self._in_progress.add(task)
            await self._queue.put(task)

    async def check_pending_queue(self):
        statuses = [Task.STATUS_PENDING, Task.STATUS_COMPLETED]
        async for task in self.get_tasks(statuses, 100):
            self._in_progress.add(task)
            await self._pending_queue.put(task)

    def discard(self, task: Task):
        self._in_progress.discard(task)
