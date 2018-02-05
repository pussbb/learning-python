# -*- coding: utf-8 -*-
"""
"""
import asyncio
import logging

from .producer import TaskProducerService
from ..models.parsers import Parser
from ..models.task import Task

logger = logging.getLogger(__name__)

ADD_TASK_MAX_RETRIES = 3
ON_ERROR_MAX_RETRIES = 2
CALLBACK_MAX_RETRIES = 3


class TaskConsumerService(object):

    def __init__(self, db_engine, task_producer: TaskProducerService,
                 period=5):
        self._db_engine = db_engine
        self._period = period
        self._task_producer = task_producer

    async def run(self):
        while True:
            for item in ['new', 'pending']:
                try:
                    await getattr(self, 'process_{}'.format(item))()
                except Exception as exp:
                    logger.exception(
                        'Processing for {} a task failed'.format(item),
                        exp
                    )
            await asyncio.sleep(self._period)

    async def process_new(self):
        if self._task_producer.new_tasks.empty():
            return

        while not self._task_producer.new_tasks.empty():
            parser = None
            async for parser in Parser.get_available(self._db_engine):
                try:
                    task = await self._task_producer.new_tasks.get()
                    asyncio.ensure_future(self.run_task(task, parser))
                    self._task_producer.new_tasks.task_done()
                except Exception as exp:
                    print(exp)
            #  there are no available parser at this moment
            if parser is None:
                break

    async def process_pending(self):
        while not self._task_producer.pending_queue.empty():
            try:
                task = await self._task_producer.pending_queue.get()

                if task.is_completed():
                    # todo smth
                    # task.parser or parser = await Parser.find(id=task.parser_id)
                    pass
                self._task_producer.pending_queue.task_done()

            except Exception as exp:
                print(exp)

    async def run_task(self, task: Task, parser: Parser):
        try:
            await parser.add_task(task)
        except Exception as exp:
            await task.set_parser_failed(parser.id, exp)
            if task.add_task_retries < ADD_TASK_MAX_RETRIES:
                await self.run_task(task, parser)
            else:
                print('Give up too many retries', task.add_task_retries)
        finally:
            # remove from list
            print('remove from list of known tasks')
            self._task_producer.discard(task)
