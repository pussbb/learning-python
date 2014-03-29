'''
Created on Jul 7, 2013

@author: pussbb
'''


from ..models.news import News as NewsModel
from . import Command

"""
Get News
"""


class News(Command):
    TABLE = NewsModel
    URI = 'news'
