# -*- coding: utf-8 -*-
"""

"""
import datetime
import collections
import pprint
from bson import ObjectId

from pymongo import MongoClient
import psutil
import time
from psutil._common import sdiskio

connection = MongoClient()


class DeflectToInstance(type):

    def __getattr__(cls, item):
        return getattr(cls(), item)


class Document(object):
    __metaclass__ = DeflectToInstance

    def __init__(self, **kwargs):
        self.__init_collection()
        self._data = {}
        if not getattr(self, 'default_values', None):
            self.default_values = {}

        for item in self.structure:
            self._data[item] = kwargs.get(item, self.default_values.get(item, None))

    def __init_collection(self):
        collection_name = getattr(self, '__collection__', self.__class__.__name__)
        db_name = getattr(self, '__database__', None)
        database =None
        if not db_name:
            database = connection.get_default_database()
        else:
            database = connection.get_database(db_name)

        if collection_name not in database.collection_names():
            database.create_collection(collection_name)

        self.__collection = database.get_collection(collection_name)

    def __getattr__(self, item):
        return self._data.get(item, getattr(self.__collection, item))

    def save(self):
        for item, value in self._data.items():
            if isinstance(value, collections.Callable):
                self._data[item] = value()
        self.__collection.save(self._data)


class DiskIO(Document):
    __database__ = 'server_stats'
    __collection__ = 'disk_ios'

    structure = {
        'read_count': int,
        'write_count': int,
        'read_bytes': int,
        'write_bytes': int,
        'read_time': int,
        'write_time': int,
        'created_at': datetime.datetime,
    }

    default_values = {'created_at': datetime.datetime.utcnow}

class VirtualMemory(Document):
    __database__ = 'server_stats'
    __collection__ = 'memory'

    structure = {
        'total': int,
        'available': int,
        'percent': int,
        'used': int,
        'free': int,
        'active': int,
        'inactive': int,
        'buffers': int,
        'cached': int,
        'created_at': datetime.datetime,
    }

    default_values = {'created_at': datetime.datetime.utcnow}


class CPUUsage(Document):
    __database__ = 'server_stats'
    __collection__ = 'cpu'


    structure = {
        'cpu': dict,
        'total': int,
        'created_at': datetime.datetime,
    }

    default_values = {'created_at': datetime.datetime.utcnow}

def disk_io_counters():
    return psutil.disk_io_counters(perdisk=False)


def disk_io(previuos):
    current = disk_io_counters()
    result = []
    for key, value in enumerate(disk_io_counters()):
        result.append(value - previuos[key])
    return sdiskio(*result), current

def grab_data():
    previous_io_counters = disk_io_counters()
    while True:
        time.sleep(10)
        disk_io_res, previous_io_counters = disk_io(previous_io_counters)
        DiskIO(**disk_io_res._asdict()).save()
        VirtualMemory(**psutil.virtual_memory()._asdict()).save()
        cpu_percent = psutil.cpu_percent(percpu=True)
        cpu = {
            'total': sum(cpu_percent),
            'cpu': {"CPU{0}".format(indx): val for indx, val in enumerate(cpu_percent)}
        }
        CPUUsage(**cpu).save()
        print(disk_io_res)
        print(cpu_percent)

#print(VirtualMemory().find({}))
#for i in VirtualMemory.find():
#    print(i)
grab_data()

"""
sdiskio(read_count=1, write_count=26, read_bytes=131072, write_bytes=507904, read_time=0, write_time=68)
"""

"""
var minDate = new Date(Date.UTC(2015, 1, 10, 11, 25, 30));
var maxDate = new Date(Date.UTC(2015, 11, 10, 11, 25, 35));
var result = db.getCollection('disk_ios').runCommand('aggregate', { pipeline:
[
	{
		$match: {
			"created_at" : {
				$gte: minDate,
				$lt : maxDate
			}
		}
	},
	{
		$project: {
			_id : 0,
			created_at : 1,
			read_count : 1,
                        write_count : 1,
		}
	},
	{
		$group: {
				"_id": {
					"year" : {
						$year : "$created_at"
					},
                    "dayOfYear" : {
						$dayOfYear : "$created_at"
					},
					"hour" : {
						$hour : "$created_at"
					},


				},
				"read_count": {
					$sum: 1
				},
				"read_avg": {
					$avg: "$read_count"
				},
				"read_min": {
					$min: "$read_count"
				},
				"read_max": {
					$max: "$read_count"
				}
			}
	},
	{
		$sort: {
			"_id.year" : 1,
			"_id.dayOfYear" : 1,
			"_id.minute" : 1,
		}
	}
]});

printjson(result)

"""
