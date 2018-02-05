# -*- coding: utf-8 -*-
"""
"""
from aiopg import sa as aiopg_sa
from aiohttp import web

from iotasks.services.consumer import TaskConsumerService
from .services.producer import TaskProducerService
from .routes import setup_routes


class ServiceWebApplication(web.Application):
    """just to be happy

    """
    def __getattr__(self, key):
        return self[key]


APP = ServiceWebApplication()
setup_routes(APP)


async def init_pg(local_app):
    local_app['db_engine'] = await aiopg_sa.create_engine(
        'postgres://dbuser:@localhost/apm'
    )


async def close_pg(local_app):
    local_app.db_engine.close()
    await local_app.db_engine.wait_closed()


async def init_task_services(local_app):
    producer = TaskProducerService(local_app.db_engine, 10)
    consumer = TaskConsumerService(local_app.db_engine, producer)
    local_app['task_producer'] = local_app.loop.create_task(producer.run())
    local_app['task_consumer'] = local_app.loop.create_task(consumer.run())


async def close_task_services(local_app):
    for item in ['task_producer', 'task_consumer']:
        try:
            local_app[item].cancel()
            await local_app[item]
        except Exception as _:
            pass


def run():
    APP.on_startup.append(init_pg)
    APP.on_startup.append(init_task_services)
    APP.on_cleanup.append(close_pg)
    APP.on_cleanup.append(close_task_services)
    web.run_app(APP, host='127.0.0.1', port=8080)
