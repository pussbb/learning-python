# -*- coding: utf-8 -*-
"""
"""
import os
import re
import sys
from collections import defaultdict, namedtuple
from io import TextIOWrapper
from pprint import pprint
from jinja2 import Environment, FileSystemLoader


BASE_PATH = os.path.dirname(os.path.abspath(__file__))
JINJA_ENV = Environment(loader=FileSystemLoader('templates'))


def read_from_skip_files(name: str):
    return [
        line.strip('\n') for line in open(os.path.join(BASE_PATH, 'skip', name))
    ]


IGNORE_CATEGORIES = read_from_skip_files('categories')
IGNORE_ISSUES = read_from_skip_files('issues')
IGNORE_STATUSES = read_from_skip_files('statuses')
IGNORE_TRACKER = read_from_skip_files('tracker')

Record = namedtuple('Record', [
    'id', 'project', 'tracker', 'parent_task', 'status',
    'priority', 'subject', 'author', 'assignee', 'updated', 'category',
    'target_version', 'start_date', 'due_date', 'estimated_time', 'spent_time',
    'done_percents', 'created', 'closed', 'related_issues', 'legacy_id',
    'operation_system', 'milestone', 'private'

])


def parse_csv_line(line: str):
    for item in re.split(r'''(?:,)(?=(?:[^"]|"[^"]*")*$)''', line):
        yield item.strip('"')


def parse_csv(data: TextIOWrapper):
    if 'Category' not in data.readline().split(','):
        raise SystemExit('CSV file does not contain Category section')

    result = defaultdict(list)
    for line in data:
        try:
            item = Record(*parse_csv_line(line))
        except Exception as _:
            pprint(line)
            raise

        if item.category in IGNORE_CATEGORIES or \
                item.id in IGNORE_ISSUES or \
                item.status in IGNORE_STATUSES or \
                item.tracker in IGNORE_TRACKER:
            continue
        result[item.category].append(item)

    return result


if __name__ == '__main__':
    if len(sys.argv) == 1:
        raise SystemExit('Please specify a csv file')

    items = parse_csv(open(sys.argv[1], 'rt', encoding='utf-8'))
    text = JINJA_ENV.get_template('index.html').render(categories=items)
    open(os.path.join(BASE_PATH, 'result.html'), 'wt').write(text)
