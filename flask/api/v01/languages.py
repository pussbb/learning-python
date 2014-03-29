'''


@author: pussbb
'''


from ..models.language import Language
from . import Command

"""
Get Languages
"""

class Languages(Command):
    URI = 'languages'
    ALLOWED_METHODS = ['GET']
    TABLE = Language
