import asyncio
import json
import logging
from enum import Enum
from typing import AnyStr

import aiohttp


logger = logging.getLogger(__name__)


class ApiTaskStatus(Enum):
    """ Enumeration with all possible(supported) api statuses

    """
    STARTING = 'starting'
    PAUSING = 'pausing'
    STOPPING = 'stopping'
    DELETING = 'deleting'
    DELETED = 'deleted'
    COMPLETED = 'completed'
    ERROR = 'error'


class ApiTaskDirection(Enum):
    """Task execution priority . Yes???

    """
    START = 'start'
    END = 'end'
    UP = 'up'
    DOWN = 'down'


class ApiError(Exception):
    """Generic AParser API client Exception

    """
    def __init__(self, message, http_status=None):
        self.http_status = http_status
        self.message = message
        super(ApiError, self).__init__(message)

    def __repr__(self):
        return "{}, HTTP status code: {}".format(self.message, self.http_status)


class ApiClientError(ApiError):
    """ Exception for handling  HTTP client error's
    (connection/request/response errors) or 4xx HTTP response status
    from server.

    """


class ApiServerError(ApiError):
    """Exception for handling  5xx HTTP response status from server,
    or some error at parser side (parser responded with 'success'!= 1 )

    """


class RequestData(dict):
    """Print request data safety

    """
    def __repr__(self):
        def __inner():
            for key, value in self.items():
                if key == 'password':
                    yield key, '*'*8
                else:
                    if key == 'data':
                        if isinstance(value, dict):
                            queries = value.get('queries')
                            if queries:
                                value['queries'] = value['queries'][:3]
                    yield key, value
        return repr(dict(__inner()))


class AParserClient:
    """
    AParser User API client.
    Asyncio port of https://github.com/EitherSoft/PyAParser
     # FIXME import api calls description from url to docstring
    API docs: http://a-parser.com/wiki/user-api/

    """
    _api_url = None
    _password = None
    _session = None

    def __init__(self, api_url, password, loop=None, **kwargs):
        if not loop:
            loop = asyncio.get_event_loop()
        self._api_url = api_url
        self._password = password
        self._session = aiohttp.ClientSession(loop=loop)

    def __del__(self):
        if not self._session:
            try:
                self._session.close()
            except Exception as _:
                pass

    def __log_debug_entry(self, line: AnyStr, *args, url: AnyStr=None):
        logger.debug(line, url, *args)

    async def __request(self, method, *args, url: AnyStr=None, **kwargs):
        if not url:
            url = self._api_url
        self.__log_debug_entry("API request to url : %s data: %s", kwargs,
                               url=url)

        async with method(url, *args, **kwargs) as resp:
            self.__log_debug_entry("API response url: %s status: %s",
                                   resp.status, url=url)
            return resp.status, await resp.text()

    async def _do_request(self, action, **kwargs):
        request_data = RequestData({
            'password': self._password,
            'action': action,
            'data': kwargs,
        })

        try:
            async with self._session as client:
                http_status, response = await self.__request(
                    client.post,
                    data=json.dumps(request_data)
                )

        except aiohttp.ClientError as e:
            logger.exception("HTTP Error")
            raise ApiClientError(str(e))
        # not sure if needed for your case but here also must be 302 http
        # status code
        if http_status not in [200, 302, 304]:
            if http_status < 500:
                raise ApiClientError(response, http_status)
            else:
                raise ApiServerError(response, http_status)

        try:
            response = json.loads(response)
        except Exception as _:
            logger.exception("Can't parse server response: %s", response)
            raise ApiServerError(response, http_status)

        if response.get('success', False):
            return response.get('data')
        else:
            logger.error("API response fail: %s %s success: %s",
                         self._api_url, request_data, response)
            raise ApiServerError(response, http_status)

    async def ping(self) -> AnyStr:
        """Simple Ping/Pong call. Check if server is working
        :return: AnyStr
        """
        return await self._do_request('ping')

    async def info(self):
        return await self._do_request('info')

    async def get_parser_info(self, parser):
        return await self._do_request('getParserInfo', parser=parser)

    async def get_proxies(self):
        return await self._do_request('getProxies')

    async def get_parser_preset(self, parser, preset):
        return await self._do_request('getParserPreset',
                                      parser=parser, preset=preset)

    async def one_request(self, parser, preset, query, **kwargs):
        data = {
            'parser': parser,
            'preset': preset,
            'query': query
        }
        return await self._do_request('oneRequest', **{**kwargs, **data})

    async def bulk_request(self, parser, preset, threads, queries, **kwargs):
        data = {
            'parser': parser,
            'preset': preset,
            'queries': queries,
            'threads': threads
        }
        return await self._do_request('bulkRequest', **{**kwargs, **data})

    async def add_task(self, config_preset, preset, queries_from, queries,
                       **kwargs):
        data = {
            'configPreset': config_preset,
            'preset': preset,
            'queriesFrom': queries_from,
        }
        queries_key = 'queriesFile'
        if queries_from in ('text', b'text'):
            queries_key = 'queries'
        data[queries_key] = queries
        return await self._do_request('addTask', **{**kwargs, **data})

    async def get_tasks_list(self, completed=0):
        return await self._do_request('getTasksList', completed=completed)

    async def get_task_state(self, task_id: AnyStr):
        return await self._do_request('getTaskState', taskUid=task_id)

    async def get_task_conf(self, task_id: AnyStr):
        return await self._do_request('getTaskConf', taskUid=task_id)

    async def change_task_status(self, task_id: AnyStr, status: ApiTaskStatus):
        return await self._do_request('changeTaskStatus', taskUid=task_id,
                                      toStatus=status.value)

    async def move_task(self, task_id: AnyStr, direction: ApiTaskDirection):
        return await self._do_request('moveTask', taskUid=task_id,
                                      direction=direction.value)

    async def set_proxy_checker_preset(self, preset):
        return await self._do_request('setProxyCheckerPreset', preset=preset)

    async def get_task_result_file(self, task_id: AnyStr):
        return await self._do_request('getTaskResultsFile', taskUid=task_id)

    async def delete_task_result_file(self, task_id: AnyStr):
        # ??? action same as get_task_result_file which is getTaskResultsFile
        return await self._do_request('getTaskResultsFile', taskUid=task_id)

    async def wait_for_task(self, task_id: AnyStr, interval=5) -> ApiTaskStatus:
        while True:
            # ? ApiServerException or ApiClientException ?????
            state = await self.get_task_state(task_id)
            if not state:
                #  assume that it was deleted
                return ApiTaskStatus.DELETED
            state = ApiTaskStatus(state)
            if state == ApiTaskStatus.COMPLETED:
                return state
            asyncio.sleep(interval)

    async def get_task_result(self, task_id: AnyStr):
        # check if task completed or exists
        task_status = await self.wait_for_task(task_id)
        if task_status == ApiTaskStatus.DELETED:
            raise ApiError('Illegal access error task {} was '
                           ' deleted'.format(task_id))
        async with self._session as client:
            http_status, response = self.__request(
                client.get,
                url=await self.get_task_result_file(task_id)
            )
        return json.loads(response)
